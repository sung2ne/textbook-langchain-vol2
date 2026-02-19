# app/utils/text_processing.py
import re
from typing import List


def clean_text(text: str) -> str:
    """텍스트 정리"""
    # 연속 공백 제거
    text = re.sub(r'\s+', ' ', text)

    # 특수문자 정리
    text = re.sub(r'[\x00-\x08\x0b\x0c\x0e-\x1f\x7f-\x9f]', '', text)

    return text.strip()


def extract_sentences(text: str) -> List[str]:
    """문장 추출"""
    # 간단한 문장 분리
    sentences = re.split(r'(?<=[.!?])\s+', text)
    return [s.strip() for s in sentences if s.strip()]


def estimate_tokens(text: str) -> int:
    """토큰 수 추정"""
    # 대략적인 추정 (한국어 포함)
    words = text.split()
    return int(len(words) * 1.3)


def truncate_text(text: str, max_length: int = 500,
                 suffix: str = "...") -> str:
    """텍스트 자르기"""
    if len(text) <= max_length:
        return text

    return text[:max_length - len(suffix)] + suffix
