# app/services/token_service.py

from datetime import datetime, timedelta, timezone
from typing import Optional

import jwt
from jwt.exceptions import InvalidTokenError

from app.core.config import settings
from app.core.logger import get_logger
from app.schemas.token import TokenData
from app.utils import exceptions

logger = get_logger(__name__)


class TokenService:
    def create_access_token(self, data: dict, expires_delta: Optional[timedelta] = None) -> str:
        expire = datetime.now(timezone.utc) + (expires_delta or timedelta(minutes=15))
        payload = {**data, "exp": int(expire.timestamp())}

        token = jwt.encode(payload, settings.jwt_secret, algorithm=settings.jwt_algorithm)
        logger.debug(f"Access token created for subject='{data.get('sub')}', expires={expire.isoformat()}")
        return token

    def decode_token(self, token: str) -> TokenData:
        try:
            payload = jwt.decode(token, settings.jwt_secret, algorithms=[settings.jwt_algorithm])

            username: Optional[str] = payload.get("sub")
            exp: Optional[int] = payload.get("exp")

            if not username:
                logger.warning("JWT decode failed: 'sub' claim missing.")
                raise exceptions.unauthorized("Invalid token: missing subject")

            if not exp:
                logger.warning("JWT decode failed: 'exp' claim missing.")
                raise exceptions.unauthorized("Invalid token: missing expiration")

            expiry_time = datetime.fromtimestamp(exp, tz=timezone.utc)
            if datetime.now(timezone.utc) > expiry_time:
                logger.info("Access token expired.")
                raise exceptions.unauthorized("Token has expired")

            logger.debug(f"JWT successfully decoded for subject='{username}'")
            return TokenData(username=username)

        except InvalidTokenError as error:
            logger.warning(f"JWT decode error: {error}")
            raise exceptions.unauthorized("Invalid token") from error

def get_token_service() -> TokenService:
    return TokenService()