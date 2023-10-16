from typing import Iterable

from fastapi import Depends
from src.deps.get_api_key import get_api_key
from src.services.gh import GitHubService


def get_gh_service(
    api_key: str = Depends(get_api_key),
) -> Iterable[GitHubService]:
    try:
        yield GitHubService(api_key)
    except Exception as e:
        raise e
