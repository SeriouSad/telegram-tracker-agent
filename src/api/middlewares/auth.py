import logging
import secrets
from typing import Optional, Tuple

from fastapi import FastAPI, HTTPException, status
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import JSONResponse

from src.settings import settings

logger = logging.Logger("Fastapi Middleware", level=logging.INFO)


class BasicAuthMiddleware(BaseHTTPMiddleware):
    """
    Middleware for basic authentication to protect against DDOS attacks.
    It checks for API key authentication in the headers.
    Authentication is skipped entirely if no API key is set in settings.
    """

    def __init__(self, app: FastAPI):
        super().__init__(app)
        self.api_key = settings.api_key
        self.skip_auth_entirely = not self.api_key

        if self.skip_auth_entirely:
            logger.warning("No API key set in settings - authentication is DISABLED!")

    async def dispatch(self, request: Request, call_next):
        if self.skip_auth_entirely:
            return await call_next(request)

        auth_success, error_response = self._check_auth(request)
        if not auth_success:
            return JSONResponse(
                status_code=error_response.status_code,
                content={"detail": error_response.detail},
                headers=error_response.headers,
            )

        try:
            return await call_next(request)
        except Exception as e:
            logger.error(f"Exception in {request.url.path}: {e}", exc_info=True)
            raise

    def _check_auth(self, request: Request) -> Tuple[bool, Optional[HTTPException]]:
        """
        Check if the request has valid authentication.
        Returns (True, None) if authentication passes,
        otherwise (False, HTTPException) with appropriate error response.
        """
        api_key = request.headers.get("X-API-Key") or request.headers.get(
            "Authorization"
        )

        if not api_key:
            return False, HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Missing API key",
                headers={"WWW-Authenticate": "Bearer"},
            )

        is_valid_key = secrets.compare_digest(api_key, self.api_key)

        if not is_valid_key:
            client_host = request.client.host if request.client else "unknown"
            logger.warning(f"Failed authentication attempt from {client_host}")

            return False, HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid API key",
                headers={"WWW-Authenticate": "Bearer"},
            )

        return True, None
