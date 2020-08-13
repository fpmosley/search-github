#!/usr/bin/env python

import csv
from collections import OrderedDict
from operator import itemgetter
import click
from colorama import init, Fore, Style
from queries import GitHubRepoLanguagesDependencyGraph

def output_results(results):
    """Output results"""

    output_list = []
    for result in results:
        if result.get('isArchived') or result.get('isDisabled'):
            continue

        primary_language = "None"
        if result.get('primaryLanguage'):
            primary_language = result.get('primaryLanguage').get('name')

        all_languages = ""
        if result.get('languages'):
            for language in result.get('languages').get('nodes'):
                all_languages += f"{language['name']}\r\n"

        if result.get('dependencyGraphManifests'):
            dependency_graph_enabled = bool(result.get('dependencyGraphManifests').get('totalCount') > 0)

        row = OrderedDict([
            ("Name", result.get('name')),
            ("Name with Owner", result.get('nameWithOwner')),
            ("URL", result.get('url')),
            ("Description", result.get('description')),
            ("Primary Language", primary_language),
            ("All Languages", all_languages),
            ("isPrivate", result.get('isPrivate')),
            ("Last Updated", result.get('updatedAt')),
            ("Dependency Graph Enabled", dependency_graph_enabled),
            ("Has Package File", result.get("has_package_file", False)),
            ("Package Files", result.get("package_formats"))
        ])
        output_list.append(row)

    print("Writing results to 'results.csv'")
    with open('results.csv', 'w', newline='') as csvfile:
        keys = output_list[0].keys()
        writer = csv.DictWriter(csvfile, keys)
        writer.writeheader()
        writer.writerows(output_list)

def search_for_dependency_graph_files(repos):
    """Search for package formats that are supported by GitHub Dependency Graph."""

    print("Searching for supported package file formats")
    supported_package_ecosystems = {
        "java": ["pom.xml"],
        "scala": ["pom.xml"],
        "javascript": ["package-lock.json", "package.json"],
        "c#": [".csproj", ".vbproj", ".nuspec", ".vcxproj", ".fsproj", "packages.config"],
        "c++": [".csproj", ".vbproj", ".nuspec", ".vcxproj", ".fsproj", "packages.config"],
        "f#": [".csproj", ".vbproj", ".nuspec", ".vcxproj", ".fsproj", "packages.config"],
        "vb": [".csproj", ".vbproj", ".nuspec", ".vcxproj", ".fsproj", "packages.config"],
        "python": ["requirements.txt", "pipfile.lock", "setup.py"],
        "ruby": ["Gemfile.lock", "Gemfile"],
        "PHP": ["composer.json", "composer.lock"]
    }

    for idx, repo in enumerate(repos):
        repo_name = repo['nameWithOwner']

        try:
            primary_language = repo['primaryLanguage']['name'].lower()
        except:
            print(Fore.RED + f"No primary language defined for repo: {repo_name}" + Style.RESET_ALL)
            continue

        try:
            package_formats = supported_package_ecosystems[primary_language]
        except KeyError:
            print(Fore.RED + f"Primary language '{primary_language}' is not supported for repo: {repo_name}" + Style.RESET_ALL)
            continue

        try:
            files = list(map(itemgetter('name'), repo['defaultBranchRef']['target']['tree']['entries']))
        except KeyError:
            print(Fore.RED + f"There is no list of files in the default branch for repo: {repo_name}" + Style.RESET_ALL)
            continue

        # Build the list of supported formats in a repo
        repo['package_formats'] = ""
        for package_format in package_formats:
            if package_format in files:
                print(Fore.WHITE + f"Found package file '{package_format}' in '{repo_name}'" + Style.RESET_ALL)
                repo['package_formats'] += f"{package_format}\r\n"
                repo['has_package_file'] = True
                repos[idx] = repo

    return repos

@click.group()
@click.version_option()
def cli():
    """Program that queries the GitHub API V4 (GraphQL)."""

@cli.command("repos", help="Query for all repositories, languages and dependencies of each one.")
@click.option('-o', '--org', 'org', required=True, type=str, help="Name of the GitHub organization")
@click.option('--token', 'token', envvar='GITHUB_TOKEN', required=True, type=str, help="GitHub token")
@click.option('--output', required=False, is_flag=True, help="Set this flag to output to 'results.csv'")
def query_repos_languages_dependencies(org, token, output):
    """Query the GitHub GraphQL V4 API for organization repos, and their languages and dependencies."""

    init()

    click.echo(f"Starting query of '{org}' organization for GitHub repos, languages and dependencies.")
    repos = list()
    query = GitHubRepoLanguagesDependencyGraph(org, token)
    repos = query.iterator()
    click.echo(f"Total number of repositories: {len(repos)}")

    search_for_dependency_graph_files(repos)

    if output:
        output_results(repos)
