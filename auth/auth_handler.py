# This file is responsible for signing , encoding , decoding and returning JWTS
import time
from typing import Dict

import jwt
from decouple import config

JWT_ALGORITHM = config("algorithm")
ACCESS_TOKEN_EXPIRE_SECONDS = 30 * 60  # 30 minutes
REFRESH_TOKEN_EXPIRE_SECONDS = 60 * 60 * 24 * 1  # 1 day
JWT_ACCESS_SECRET_KEY = config('JWT_ACCESS_SECRET_KEY')
JWT_REFRESH_SECRET_KEY = config('JWT_REFRESH_SECRET_KEY')


def token_response(access_token: str, refresh_token: str):
    return {
        "access_token": access_token,
        "refresh_token": refresh_token
    }


# function used for signing the JWT string
def CreateAccessRefreshToken(username: str) -> Dict[str, str]:
    access_token_payload = {
        "username": username,
        "expires": time.time() + ACCESS_TOKEN_EXPIRE_SECONDS
    }

    refresh_token_payload = {
        "username": username,
        "expires": time.time() + REFRESH_TOKEN_EXPIRE_SECONDS
    }
    access_token = jwt.encode(access_token_payload, JWT_ACCESS_SECRET_KEY, algorithm=JWT_ALGORITHM)
    refresh_token = jwt.encode(refresh_token_payload, JWT_REFRESH_SECRET_KEY, algorithm=JWT_ALGORITHM)

    return token_response(access_token, refresh_token)


def decodeJWT(token: str) -> dict:
    try:
        decoded_token = jwt.decode(token, JWT_ACCESS_SECRET_KEY, algorithms=[JWT_ALGORITHM])
        return decoded_token if decoded_token["expires"] >= time.time() else None
    except Exception as e:
        print(e)
        return {}
