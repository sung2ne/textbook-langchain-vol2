# app/middleware/logging.py
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
import time
import uuid
from app.utils.logging import get_logger


class LoggingMiddleware(BaseHTTPMiddleware):
    """요청/응답 로깅 미들웨어"""

    async def dispatch(self, request: Request, call_next):
        # 요청 ID 생성
        request_id = str(uuid.uuid4())[:8]
        logger = get_logger("api", request_id=request_id)

        # 요청 로깅
        start_time = time.time()
        logger.info(
            f"Request started",
            extra={
                "method": request.method,
                "path": request.url.path,
                "client_ip": request.client.host
            }
        )

        try:
            response = await call_next(request)
            duration_ms = (time.time() - start_time) * 1000

            # 응답 로깅
            logger.info(
                f"Request completed",
                extra={
                    "status_code": response.status_code,
                    "duration_ms": round(duration_ms, 2)
                }
            )

            # 응답 헤더에 요청 ID 추가
            response.headers["X-Request-ID"] = request_id

            return response

        except Exception as e:
            duration_ms = (time.time() - start_time) * 1000
            logger.error(
                f"Request failed: {str(e)}",
                extra={
                    "error": str(e),
                    "duration_ms": round(duration_ms, 2)
                },
                exc_info=True
            )
            raise


# main.py에 추가
# app.add_middleware(LoggingMiddleware)
