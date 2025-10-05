# app/auth/auth_bearer.py
from fastapi import Request, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from .auth_handler import decode_token

class JWTBearer(HTTPBearer):
    async def __call__(self, request: Request):
        credentials: HTTPAuthorizationCredentials = await super().__call__(request)
        if credentials:
            token = credentials.credentials
            user = decode_token(token)
            if not user:
                raise HTTPException(status_code=403, detail="Invalid or expired token")
            return user
        raise HTTPException(status_code=403, detail="Invalid authorization header")
