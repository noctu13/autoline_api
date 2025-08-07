from datetime import datetime, timedelta, timezone
from jose import JWTError, jwt

from app.core.config import settings
from app.core.exceptions import (TokenExpiredException, 
    TokenInvalidClaimsException, TokenInvalidException)
from app.domain.services.token_service import TokenService


class JWTTokenService(TokenService):
    def create_token(self, data: dict) -> str:
        to_encode = data.copy()
        expire = datetime.now(timezone.utc) + timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        to_encode.update({"exp": expire})
        return jwt.encode(
            to_encode, 
            settings.SECRET_KEY, 
            algorithm=settings.ALGORITHM
        )

    def verify_token(self, token: str) -> dict:
        try:
            payload = jwt.decode(
                token,
                settings.SECRET_KEY,
                settings.ALGORITHM
            )
            if not {"sub", "exp", "type"}.issubset(payload.keys()):
                raise TokenInvalidClaimsException
            return payload
        except jwt.ExpiredSignatureError:
            raise TokenExpiredException
        except JWTError:
            raise TokenInvalidException