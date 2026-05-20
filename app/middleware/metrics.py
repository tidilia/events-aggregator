import time

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request

from app.metrics import http_request_duration_seconds, http_requests_total


class MetricsMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        start = time.monotonic()

        response = await call_next(request)

        duration = time.monotonic() - start

        method = request.method
        endpoint = request.url.path
        status = str(response.status_code)

        http_requests_total.labels(
            method=method,
            endpoint=endpoint,
            status=status,
        ).inc()

        http_request_duration_seconds.labels(
            method=method,
            endpoint=endpoint,
        ).observe(duration)

        return response
