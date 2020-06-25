from github_api import GitHubGraphQLQuery

class GitHubRepoLanguagesDependencyGraph(GitHubGraphQLQuery):

    QUERY = """
        query($org: String!, $after: String) {
            organization(login: $org) {
                repositories(first: 100, after: $after) {
                    pageInfo {
                        hasNextPage
                        endCursor
                    }
                    totalCount
                    nodes {
                        name
                        nameWithOwner
                        url
                        description
                        primaryLanguage {
                            name
                        }
                        languages(first: 20) {
                            totalCount
                            nodes {
                                name
                            }
                        }
                        dependencyGraphManifests(first: 100) {
                            totalCount
                        }
                        isArchived
                        isDisabled
                        isPrivate
                        updatedAt
                        defaultBranchRef {
                            target {
                                ... on Commit {
                                    tree {
                                        entries {
                                            name
                                        }
                                    }
                                }
                            }
                        }
                    }
                }
            }
        }
    """
    ADDITIONAL_HEADERS = dict(Accept="application/vnd.github.hawkgirl-preview+json")

    def __init__(self, organization_name, token):
        super(GitHubRepoLanguagesDependencyGraph, self).__init__(
            token=token,
            query=GitHubRepoLanguagesDependencyGraph.QUERY,
            variables=dict(org=organization_name, after=None),
            additional_headers=GitHubRepoLanguagesDependencyGraph.ADDITIONAL_HEADERS,
        )

    def iterator(self):
        generator = self.generator()
        hasNextPage = True
        repos_languages_dependencies = list()
        print("Getting results. Page", end="")
        count = 1
        while hasNextPage:
            print(f".{count}.", end="", flush=True)
            response = next(generator)
            endCursor = response["data"]["organization"]["repositories"]["pageInfo"]["endCursor"]
            self._variables["after"] = endCursor
            repos_languages_dependencies.extend(
                response["data"]["organization"]["repositories"]["nodes"]
            )
            hasNextPage = response["data"]["organization"]["repositories"]["pageInfo"]["hasNextPage"]
            count += 1
        print()
        f'Total number of repos: {len(repos_languages_dependencies)}'
        return repos_languages_dependencies
