# 소설처럼 읽는 LangChain과 생성형 AI 2권 - 실습 코드

[iBetter Books 교재](https://text.ibetter.kr/langchain-vol2)의 실습 코드 저장소입니다.

임베딩, 벡터 데이터베이스, RAG(검색 증강 생성)를 활용한 생성형 AI 심화 과정으로, 문서 기반 QA 시스템부터 프로덕션 배포까지 단계별로 학습합니다.

## 사용 방법

원하는 챕터의 브랜치를 체크아웃하면 해당 시점까지의 완성된 프로젝트를 받을 수 있습니다.

```bash
# 저장소 클론
git clone https://github.com/sung2ne/textbook-langchain-vol2.git
cd textbook-langchain-vol2

# 가상환경 생성 및 활성화
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate

# 의존성 설치
pip install -r requirements.txt

# 원하는 챕터로 이동
git checkout part03/chapter-04   # PART 03의 04장까지 완성된 코드
```

## 브랜치 목록

각 브랜치는 해당 챕터까지의 코드가 누적 적용되어 독립적으로 실행 가능합니다. 총 **41개** 브랜치가 제공됩니다.

### PART 00. 2권 시작

| 브랜치 | 내용 |
|--------|------|
| `part00/chapter-01` | 1권 복습 |
| `part00/chapter-02` | RAG란 무엇인가 |
| `part00/chapter-03` | 2권 환경 설정 |

### PART 01. 임베딩의 세계

| 브랜치 | 내용 |
|--------|------|
| `part01/chapter-01` | 임베딩이란 |
| `part01/chapter-02` | 유사도 계산 |
| `part01/chapter-03` | 임베딩 모델 비교 |
| `part01/chapter-04` | LangChain에서 임베딩 활용 |

### PART 02. 벡터 데이터베이스

| 브랜치 | 내용 |
|--------|------|
| `part02/chapter-01` | ChromaDB 시작하기 |
| `part02/chapter-02` | LangChain과 ChromaDB |
| `part02/chapter-03` | FAISS 벡터 검색 |
| `part02/chapter-04` | 벡터 DB 비교와 선택 |

### PART 03. RAG 기초

| 브랜치 | 내용 |
|--------|------|
| `part03/chapter-01` | 문서 로딩 |
| `part03/chapter-02` | 문서 분할 |
| `part03/chapter-03` | Retriever 활용 |
| `part03/chapter-04` | RetrievalQA 체인 |

### PART 04. 검색 최적화

| 브랜치 | 내용 |
|--------|------|
| `part04/chapter-01` | 쿼리 변환 |
| `part04/chapter-02` | 하이브리드 검색 |
| `part04/chapter-03` | 리랭킹 |
| `part04/chapter-04` | 검색 파이프라인 설계 |

### PART 05. 문서 처리 고급

| 브랜치 | 내용 |
|--------|------|
| `part05/chapter-01` | 메타데이터 활용 |
| `part05/chapter-02` | 계층적 청킹 |
| `part05/chapter-03` | 표와 이미지 처리 |
| `part05/chapter-04` | 멀티모달 RAG |

### PART 06. 평가와 개선

| 브랜치 | 내용 |
|--------|------|
| `part06/chapter-01` | RAG 평가 지표 |
| `part06/chapter-02` | 테스트셋 구축 |
| `part06/chapter-03` | 자동화된 평가 |
| `part06/chapter-04` | 개선 전략 |

### PART 07. 웹 인터페이스 고급

| 브랜치 | 내용 |
|--------|------|
| `part07/chapter-01` | Streamlit 고급 기능 |
| `part07/chapter-02` | FastAPI 백엔드 |
| `part07/chapter-03` | 프론트엔드 분리 |
| `part07/chapter-04` | 실시간 스트리밍 |

### PART 08. 두 번째 프로젝트

| 브랜치 | 내용 |
|--------|------|
| `part08/chapter-01` | 프로젝트 구조 설계 |
| `part08/chapter-02` | 백엔드 API 구현 |
| `part08/chapter-03` | RAG 파이프라인 구축 |
| `part08/chapter-04` | 프론트엔드 개발 |
| `part08/chapter-05` | 통합 및 테스트 |

### PART 09. 클라우드 배포

| 브랜치 | 내용 |
|--------|------|
| `part09/chapter-01` | Docker 컨테이너화 |
| `part09/chapter-02` | 클라우드 배포 옵션 |
| `part09/chapter-04` | 모니터링과 로깅 |

### PART 10. 3권 준비

| 브랜치 | 내용 |
|--------|------|
| `part10/chapter-01` | 2권 내용 복습 |
| `part10/chapter-02` | 3권 미리보기 |

## 기술 스택

- **언어**: Python 3.11+
- **LLM 프레임워크**: LangChain 0.3.x
- **벡터 데이터베이스**: ChromaDB, FAISS
- **임베딩 모델**: sentence-transformers, OpenAI Embeddings
- **로컬 LLM**: Ollama
- **클라우드 LLM**: OpenAI GPT-4o-mini
- **웹 UI**: Streamlit
- **API 서버**: FastAPI + Uvicorn
- **문서 처리**: pypdf

## 실행 방법

```bash
# 의존성 설치
pip install -r requirements.txt

# OpenAI API 키 설정
cp .env.example .env
# .env 파일에 OPENAI_API_KEY 입력

# Ollama 설치 및 모델 다운로드 (로컬 LLM 사용 시)
ollama pull llama4

# 예제 실행
python example_01.py

# FastAPI 서버 실행 (PART 07 이후)
uvicorn main:app --reload
```

## 라이선스

이 저장소는 [소설처럼 읽는 LangChain과 생성형 AI 2권](https://text.ibetter.kr/langchain-vol2) 교재의 실습 코드입니다.
