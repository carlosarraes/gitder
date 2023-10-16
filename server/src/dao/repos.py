from typing import Any

import boto3
from src.models.repo import Repos


class ReposDAO:
    def __init__(self, table_name: str):
        self.dynamodb: Any = boto3.resource("dynamodb")
        self.table: Any = self.dynamodb.Table(table_name)

    def _repo_to_dict(self, repo: Repos) -> dict[str, Any]:
        return {
            "full_name": repo.full_name,
            "description": repo.description,
            "language": repo.language,
            "created_at": repo.created_at,
            "updated_at": repo.updated_at,
            "size": repo.size,
            "stargazers_count": repo.stargazers_count,
            "watchers_count": repo.watchers_count,
            "forks_count": repo.forks_count,
            "languages": repo.languages,
        }

    def save_user_repos(self, username: str, repos: list[Repos]) -> None:
        self.table.put_item(
            Item={
                "username": username,
                "repos": [self._repo_to_dict(repo) for repo in repos],
            }
        )

    def get_user_repos(self, username: str) -> list[Repos]:
        repos_data = response.get("Item", {}).get("repos", [])
            response = self.table.get_item(Key={"username": username})

        return [Repos.from_dict(repo_dict) for repo_dict in repos_data]
