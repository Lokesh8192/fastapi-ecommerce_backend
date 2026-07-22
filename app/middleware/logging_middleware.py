import time

from starlette.middleware.base import BaseHTTPMiddleware

from app.utils.logger import logger


class LoggingMiddleware(BaseHTTPMiddleware):

    async def dispatch(self, request, call_next):

        start = time.perf_counter()

        response = await call_next(request)

        duration = round(
            time.perf_counter() - start,
            3,
        )

        logger.info(
            "request_id=%s method=%s path=%s status=%s duration=%.3fs",
            request.state.request_id,
            request.method,
            request.url.path,
            response.status_code,
            duration,
        )

        return response