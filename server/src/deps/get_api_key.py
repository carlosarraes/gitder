import json

import boto3
from fastapi import HTTPException


def get_api_key():
    try:
        client = boto3.client("secretsmanager")
        secret_name = "GITHUB_KEY"
        response = client.get_secret_value(SecretId=secret_name)
        secret = json.loads(response["SecretString"])

        return secret["GITHUB_KEY"]
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail="Internal Server Error")
