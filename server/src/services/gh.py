import asyncio
import os

import httpx
from src.dao.repos import ReposDAO
from src.models.repo import Repos


class GitHubService:
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.baseURL = "https://api.github.com"
        self.headers = {
            "Accept": "application/vnd.github.v3+json",
            "X-GitHub-Api-Version": "2022-11-28",
            "Authorization": f"Bearer {self.api_key}",
        }
        self.dao = ReposDAO(os.environ.get("DYNAMO_TABLE_NAME", "default_table_name"))

    @staticmethod
    def _get_repo_language_url(url: str, username: str) -> str:
        return f"{url}/repos/{username}/languages"

    async def _get_languages(self, repos: list[Repos]) -> list[Repos]:
        async with httpx.AsyncClient() as client:
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

    async def get_repos(self, username: str) -> list[Repos]:
        request_url = f"{self.baseURL}/users/{username}/repos?sort=created&per_page=100"

        if saved_repos := self.dao.get_user_repos(username):
            return saved_repos

        async with httpx.AsyncClient() as client:
            response = await client.get(
                request_url,
                headers=self.headers,
            )
            response.raise_for_status()

            repos = [
                Repos.from_dict(repo) for repo in response.json() if repo["size"] >= 100
            ]

            self.dao.save_user_repos(username, repos)

            return await self._get_languages(repos)
