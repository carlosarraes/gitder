from fastapi import Depends, FastAPI
from mangum import Mangum
from src.factories.get_gh_service import get_gh_service
from src.services.gh import GitHubService

app = FastAPI()


@app.get("/")
def root():
    return {"message": "Hello World"}


@app.get("/users/{username}")
async def entry(
    username: str,
    service: GitHubService = Depends(get_gh_service),
):
    return await service.get_repos(username)


handler = Mangum(app)
