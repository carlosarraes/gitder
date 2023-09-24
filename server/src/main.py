import requests
from deps.get_api_key import get_api_key
from fastapi import Depends, FastAPI
from mangum import Mangum

app = FastAPI()

baseURL = "https://api.github.com"


@app.get("/")
def root():
    return {"message": "Hello World"}


@app.get("/users/{user}")
def entry(user: str, api_key: str = Depends(get_api_key)):
    request_url = f"{baseURL}/users/{user}"

    response = requests.get(request_url)

    return response.json()


handler = Mangum(app)
