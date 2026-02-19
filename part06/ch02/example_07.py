from pathlib import Path
from typing import Dict, List, Optional
import json
from datetime import datetime


class TestSetManager:
    """테스트셋 관리자"""

    def __init__(self, base_dir: str = "./test_sets"):
        self.base_dir = Path(base_dir)
        self.base_dir.mkdir(exist_ok=True)
        self.registry_path = self.base_dir / "registry.json"

    def _load_registry(self) -> Dict:
        """레지스트리 로드"""
        if self.registry_path.exists():
            with open(self.registry_path, "r", encoding="utf-8") as f:
                return json.load(f)
        return {"test_sets": {}}

    def _save_registry(self, registry: Dict):
        """레지스트리 저장"""
        with open(self.registry_path, "w", encoding="utf-8") as f:
            json.dump(registry, f, ensure_ascii=False, indent=2)

    def register(self, name: str, version: str, description: str,
                files: Dict[str, str], metadata: Dict = None):
        """테스트셋 등록"""
        registry = self._load_registry()

        if name not in registry["test_sets"]:
            registry["test_sets"][name] = {"versions": {}}

        registry["test_sets"][name]["versions"][version] = {
            "description": description,
            "files": files,
            "metadata": metadata or {},
            "created_at": datetime.now().isoformat()
        }

        self._save_registry(registry)
        print(f"등록됨: {name} v{version}")

    def get(self, name: str, version: str = "latest") -> Optional[Dict]:
        """테스트셋 조회"""
        registry = self._load_registry()

        if name not in registry["test_sets"]:
            return None

        versions = registry["test_sets"][name]["versions"]

        if version == "latest":
            # 최신 버전
            if not versions:
                return None
            version = sorted(versions.keys())[-1]

        return versions.get(version)

    def list_all(self) -> List[Dict]:
        """모든 테스트셋 목록"""
        registry = self._load_registry()
        result = []

        for name, data in registry["test_sets"].items():
            versions = list(data["versions"].keys())
            latest = versions[-1] if versions else None

            result.append({
                "name": name,
                "versions": versions,
                "latest": latest
            })

        return result

    def load_split(self, name: str, split: str,
                  version: str = "latest") -> List[Dict]:
        """분할 데이터 로드"""
        test_set = self.get(name, version)

        if not test_set:
            raise ValueError(f"테스트셋 없음: {name}")

        file_path = test_set["files"].get(split)
        if not file_path:
            raise ValueError(f"분할 없음: {split}")

        path = self.base_dir / file_path

        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)


# 사용
manager = TestSetManager()

# 등록
manager.register(
    name="langchain_qa",
    version="1.0",
    description="LangChain 기초 Q&A 테스트셋",
    files={
        "train": "langchain_test_train.json",
        "val": "langchain_test_val.json",
        "test": "langchain_test_test.json"
    },
    metadata={"num_questions": 100, "source": "synthetic"}
)

# 목록 조회
for ts in manager.list_all():
    print(f"{ts['name']}: {ts['versions']}")

# 데이터 로드
# test_data = manager.load_split("langchain_qa", "test")
