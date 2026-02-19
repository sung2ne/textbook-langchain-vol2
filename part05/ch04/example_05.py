from langchain_core.documents import Document
from typing import Optional
import hashlib
import json
from pathlib import Path


class CachedImageDescriber:
    """캐시된 이미지 설명기"""

    def __init__(self, cache_dir: str = ".image_cache"):
        self.cache_dir = Path(cache_dir)
        self.cache_dir.mkdir(exist_ok=True)

    def _get_image_hash(self, image_path: str) -> str:
        """이미지 해시 생성"""
        with open(image_path, "rb") as f:
            return hashlib.md5(f.read()).hexdigest()

    def _get_cache_path(self, image_hash: str) -> Path:
        """캐시 파일 경로"""
        return self.cache_dir / f"{image_hash}.json"

    def get_description(self, image_path: str) -> Optional[str]:
        """캐시된 설명 조회"""
        image_hash = self._get_image_hash(image_path)
        cache_path = self._get_cache_path(image_hash)

        if cache_path.exists():
            with open(cache_path, "r", encoding="utf-8") as f:
                data = json.load(f)
                return data.get("description")

        return None

    def save_description(self, image_path: str, description: str):
        """설명 캐싱"""
        image_hash = self._get_image_hash(image_path)
        cache_path = self._get_cache_path(image_hash)

        data = {
            "source": image_path,
            "description": description,
            "hash": image_hash
        }

        with open(cache_path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

    def describe(self, image_path: str, force: bool = False) -> str:
        """이미지 설명 (캐시 우선)"""
        if not force:
            cached = self.get_description(image_path)
            if cached:
                return cached

        # 새로 생성 (실제로는 비전 모델 호출)
        description = self._generate_description(image_path)

        # 캐싱
        self.save_description(image_path, description)

        return description

    def _generate_description(self, image_path: str) -> str:
        """설명 생성 (실제 구현)"""
        # 비전 모델 호출
        return f"이미지 {image_path}에 대한 상세 설명"


# 사용
describer = CachedImageDescriber()

# 첫 호출: 생성 + 캐싱
# desc1 = describer.describe("image.png")

# 두 번째 호출: 캐시에서 로드
# desc2 = describer.describe("image.png")
