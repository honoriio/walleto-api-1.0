from fastapi import Request
from slowapi.errors import RateLimitExceeded
from fastapi.responses import JSONResponse
import logging

logger = logging.getLogger(__name__)


async def rate_limit_handler(request: Request, exc: RateLimitExceeded):
    ip = request.client.host if request.client else "unknown"

    logger.warning(
        "Rate limit excedido - ip=%s - path=%s - method=%s",
        ip,
        request.url.path,
        request.method
    )

    return JSONResponse(
        status_code=429,
        content={"detail": "Muitas requisições. Tente novamente mais tarde."},
    )   