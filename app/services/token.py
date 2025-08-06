# app/services/token.py

from datetime import datetime, timedelta, timezone
from typing import Optional

import jwt
from jwt.exceptions import InvalidTokenError

from ..core.logger import get_logger
from ..core.settings import settings
from ..schemas.token import TokenData
from ..utils import exceptions

logger = get_logger(__name__)


class TokenService:
    def create_access_token(
        self, data: dict, expires_delta: Optional[timedelta] = None
    ) -> str:
        expire = datetime.now(timezone.utc) + (expires_delta or timedelta(minutes=15))
        payload = {**data, "exp": expire}

        token = jwt.encode(
            payload, settings.jwt_secret, algorithm=settings.jwt_algorithm
        )
        logger.debug(
            f"Access token created for: {data.get('sub')} with expiry: {expire.isoformat()}"
        )
        return token

    def decode_token(self, token: str) -> TokenData:
        try:
            payload = jwt.decode(
                token, settings.jwt_secret, algorithms=[settings.jwt_algorithm]
            )
            username = payload.get("sub")
            exp = payload.get("exp")

            if not username:
                logger.warning("JWT decode failed: 'sub' claim missing.")
                raise exceptions.unauthorized("Invalid token: missing subject")

            if not exp:
                logger.warning("JWT decode failed: 'exp' claim missing.")
                raise exceptions.unauthorized("Invalid token: missing expiration")

            if datetime.now(timezone.utc) > datetime.fromtimestamp(
                exp, tz=timezone.utc
            ):
                logger.info("Access token expired.")
                raise exceptions.unauthorized("Token has expired")

            return TokenData(username=username)

        except InvalidTokenError as error:
            logger.warning(f"JWT decode error: {error}")
            raise exceptions.unauthorized("Invalid token") from error


# Dependency injector
def get_token_service() -> TokenService:
    return TokenService()
