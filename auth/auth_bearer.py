# The goal of this file is to check whether the reques tis authorized or not [ verification of the proteced route]

from fastapi import Request, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from models import User
from .auth_handler import decodeJWT
from database import session
from decouple import config
import jwt

JWT_ALGORITHM = config("algorithm")
JWT_ACCESS_SECRET_KEY = config('JWT_ACCESS_SECRET_KEY')


class JWTBearer(HTTPBearer):
    def __init__(self, auto_error: bool = True):
        super(JWTBearer, self).__init__(auto_error=auto_error)

    async def __call__(self, request: Request):
        credentials: HTTPAuthorizationCredentials = await super(JWTBearer, self).__call__(request)
        if credentials:
            if not credentials.scheme == "Bearer":
                raise HTTPException(status_code=403, detail="Invalid authentication scheme.")
            if not self.verify_jwt(credentials.credentials):
                raise HTTPException(status_code=403, detail="Invalid token or expired token.")
            return credentials.credentials
        else:
            raise HTTPException(status_code=403, detail="Invalid authorization code.")

    def verify_jwt(self, jwtoken: str) -> bool:
        isTokenValid: bool = False

        try:
            payload = decodeJWT(jwtoken)
        except:
            payload = None
        if payload:
            isTokenValid = True
        return isTokenValid


def get_current_user(jwtoken: str) -> dict:
    decoded_token = jwt.decode(jwtoken, JWT_ACCESS_SECRET_KEY, algorithms=[JWT_ALGORITHM])
    return session.query(User).filter(User.username == decoded_token.get('username')).first()
