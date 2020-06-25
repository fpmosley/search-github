from requests import exceptions, request

class GitHubSearchQuery:
    """Search the GitHub Search API with the given query string."""

    BASE_URL = "https://api.github.com/search/code"

    def __init__(self, token, query, additional_headers=None):
        self._token = token
        self._query = query
        self._additional_headers = additional_headers or dict()

    @property
    def headers(self):
        default_headers = dict(Authorization="token {}".format(self._token))
        return dict(**default_headers, **self._additional_headers)

    def run(self):
        total_count = None
        try:
            resp = request(
                "get",
                GitHubSearchQuery.BASE_URL,
                headers=self.headers,
                params=self._query,
            )
            print(f"Request Headers: {resp.request.headers}")
            print(f"Request URL: {resp.request.url}")
            print(f"Response: {resp.json()}")
            total_count = resp.json().get("total_count")
        except exceptions.HTTPError as http_err:
            raise http_err
        except Exception as err:
            raise err

        return total_count if total_count and total_count > 0 else 0

class GitHubGraphQLQuery:
    """Search the GitHub GraphQL API with the given query."""

    BASE_URL = "https://api.github.com/graphql"

    def __init__(self, token, query, variables=None, additional_headers=None):
        self._token = token
        self._query = query
        self._variables = variables or dict()
        self._additional_headers = additional_headers or dict()

    @property
    def headers(self):
        default_headers = dict(Authorization="token {}".format(self._token))
        return dict(**default_headers, **self._additional_headers)

    def generator(self):
        while True:
            try:
                yield request(
                    "post",
                    GitHubGraphQLQuery.BASE_URL,
                    headers=self.headers,
                    json={"query": self._query, "variables": self._variables},
                ).json()
            except exceptions.HTTPError as http_err:
                raise http_err
            except Exception as err:
                raise err

    def iterator(self):
        pass
