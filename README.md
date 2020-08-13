# search-github
 
This tool is used to query the [GitHub GraphQL API](https://docs.github.com/en/graphql) to identify the languages, if dependency graph is enabled, and the supported package files in the repositories within a GitHub organization. The GraphQL API is v4 of the GitHub API and GraphQL is a data query language. You can read more about GitHub's GraphQL API and GraphQL [here](https://docs.github.com/en/graphql/overview/about-the-graphql-api).

## Usage

```
Usage: github_query repos [OPTIONS]

  Query for all repositories, along with languages and dependencies of each one for a GitHub organization.

Options:
  -o, --org TEXT  Name of the GitHub organization  [required]
  --token TEXT    GitHub token  [required]
  --output        Set this flag to output to 'results.csv'
  --help          Show this message and exit.
``` 

A GitHub token is required to use this tool. Read "[Creating a personal access token](https://docs.github.com/en/github/authenticating-to-github/creating-a-personal-access-token)" to learn how to create a token.

## Installation

This tool makes use of [Click](https://click.palletsprojects.com/en/7.x/) for creating the command line interface. To install the tool and the required packages run the following command*:

```
pip install --editable .
```

\* You may choose to run this command inside of a virtual environment.

## Queries

The [query](https://github.com/fpmosley/search-github/blob/master/queries/repos_languages_dependencies.py#L5-L50) used in this tool was created using [GitHub's GraphQL Explorer](https://developer.github.com/v4/explorer/). 

The API has a limit of 100 items/request. To help with navigating that limit the [code](https://github.com/fpmosley/search-github/blob/master/github_api.py#L54-L66) uses a [Python Generator](https://wiki.python.org/moin/Generators) to behave like an iterator to loop through all of the pages of items.

