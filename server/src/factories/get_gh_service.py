from typing import Iterable

from src.services.gh import GitHubService


def get_gh_service() -> Iterable[GitHubService]:
    try:
        yield GitHubService()
    except Exception as e:
        raise e
