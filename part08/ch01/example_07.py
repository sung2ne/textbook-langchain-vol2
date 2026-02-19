# setup.py
import os
from pathlib import Path


def setup_project():
    """프로젝트 초기 설정"""

    # 디렉토리 생성
    dirs = [
        "app/api/routes",
        "app/services",
        "app/models",
        "app/utils",
        "frontend",
        "tests",
        "data/vectorstore",
        "data/uploads"
    ]

    for d in dirs:
        Path(d).mkdir(parents=True, exist_ok=True)

        # __init__.py 생성
        if d.startswith("app") or d.startswith("tests"):
            init_file = Path(d) / "__init__.py"
            if not init_file.exists():
                init_file.touch()

    # .env 파일 생성
    env_content = """# 환경 설정
DEBUG=true
LLM_MODEL=llama4
EMBEDDING_MODEL=nomic-embed-text
CHUNK_SIZE=500
TOP_K=5
"""

    env_file = Path(".env")
    if not env_file.exists():
        env_file.write_text(env_content)

    print("✓ 프로젝트 구조 생성 완료")


if __name__ == "__main__":
    setup_project()
