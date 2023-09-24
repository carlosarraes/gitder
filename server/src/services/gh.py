import asyncio

import httpx
from src.models.repo import Repos


class GitHubService:
    def __init__(self):
        self.baseURL = "https://api.github.com"
        self.headers = {
            "Accept": "application/vnd.github.v3+json",
            "X-GitHub-Api-Version": "2022-11-28",
        }

    @staticmethod
    def _get_repo_language_url(url: str, full_name: str) -> str:
        return f"{url}/repos/{full_name}/languages"

    async def get_repos(self, username: str) -> list[Repos]:
        request_url = f"{self.baseURL}/users/{username}/repos?sort=created&per_page=100"

        async with httpx.AsyncClient() as client:
            response = await client.get(
                request_url,
                headers=self.headers,
            )
            response.raise_for_status()

            repos = [
                Repos.from_dict(repo) for repo in response.json() if repo["size"] >= 100
            ]

            language_responses = await asyncio.gather(
                *[
                    client.get(
                        self._get_repo_language_url(self.baseURL, repo.full_name),
                        headers=self.headers,
                    )
                    for repo in repos
                ],
            )

            for repo, language_response in zip(repos, language_responses):
                language_response.raise_for_status()
                repo.languages = language_response.json()

            return repos
