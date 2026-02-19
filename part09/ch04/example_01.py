# app/utils/logging.py
import logging
import sys
from datetime import datetime
import json
from typing import Any


class JSONFormatter(logging.Formatter):
    """JSON 로그 포매터"""

    def format(self, record: logging.LogRecord) -> str:
        log_data = {
            "timestamp": datetime.utcnow().isoformat(),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
            "module": record.module,
            "function": record.funcName,
            "line": record.lineno
        }

        # 추가 필드
        if hasattr(record, "extra"):
            log_data.update(record.extra)

        # 예외 정보
        if record.exc_info:
            log_data["exception"] = self.formatException(record.exc_info)

        return json.dumps(log_data, ensure_ascii=False)


def setup_logging(level: str = "INFO"):
    """로깅 설정"""
    # 루트 로거
    root_logger = logging.getLogger()
    root_logger.setLevel(level)

    # 핸들러 제거
    for handler in root_logger.handlers[:]:
        root_logger.removeHandler(handler)

    # 콘솔 핸들러
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(JSONFormatter())
    root_logger.addHandler(console_handler)

    # 애플리케이션 로거
    app_logger = logging.getLogger("app")
    app_logger.setLevel(level)

    return app_logger


# 로거 인스턴스
logger = setup_logging()


class LoggerAdapter(logging.LoggerAdapter):
    """컨텍스트 추가 어댑터"""

    def process(self, msg: str, kwargs: dict) -> tuple:
        extra = kwargs.get("extra", {})
        extra.update(self.extra)
        kwargs["extra"] = extra
        return msg, kwargs


def get_logger(name: str, **context) -> LoggerAdapter:
    """컨텍스트 로거 생성"""
    base_logger = logging.getLogger(name)
    return LoggerAdapter(base_logger, context)
