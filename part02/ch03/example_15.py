from langchain_community.vectorstores import FAISS
from langchain_ollama import OllamaEmbeddings
from langchain_core.documents import Document
import time


class FastDocumentSearch:
    """FAISS 기반 고속 문서 검색"""

    def __init__(self, persist_path="./faiss_db"):
        self.embeddings = OllamaEmbeddings(model="nomic-embed-text")
        self.persist_path = persist_path
        self.vectorstore = None

    def create_index(self, documents):
        """인덱스 생성"""
        start = time.time()
        self.vectorstore = FAISS.from_documents(documents, self.embeddings)
        elapsed = time.time() - start
        print(f"인덱스 생성 완료: {len(documents)}개 문서, {elapsed:.2f}초")

    def add_documents(self, documents):
        """문서 추가"""
        if self.vectorstore is None:
            self.create_index(documents)
        else:
            new_store = FAISS.from_documents(documents, self.embeddings)
            self.vectorstore.merge_from(new_store)

    def search(self, query, k=5):
        """검색"""
        start = time.time()
        results = self.vectorstore.similarity_search_with_score(query, k=k)
        elapsed = time.time() - start

        print(f"검색 완료: {elapsed*1000:.2f}ms")
        return results

    def save(self):
        """저장"""
        self.vectorstore.save_local(self.persist_path)
        print(f"저장 완료: {self.persist_path}")

    def load(self):
        """로드"""
        self.vectorstore = FAISS.load_local(
            self.persist_path,
            self.embeddings,
            allow_dangerous_deserialization=True
        )
        print(f"로드 완료: {self.vectorstore.index.ntotal}개 벡터")


# 사용
search = FastDocumentSearch()

# 문서 생성
docs = [
    Document(
        page_content="파이썬은 간결하고 읽기 쉬운 프로그래밍 언어입니다.",
        metadata={"topic": "python"}
    ),
    Document(
        page_content="LangChain은 LLM 애플리케이션 개발을 돕는 프레임워크입니다.",
        metadata={"topic": "langchain"}
    ),
    Document(
        page_content="FAISS는 Facebook에서 만든 벡터 검색 라이브러리입니다.",
        metadata={"topic": "faiss"}
    ),
    Document(
        page_content="RAG는 검색과 생성을 결합한 기술입니다.",
        metadata={"topic": "rag"}
    ),
]

# 인덱스 생성
search.create_index(docs)

# 검색
print("\n검색: 'AI 개발 도구'")
results = search.search("AI 개발 도구", k=3)
for doc, score in results:
    print(f"[{score:.4f}] {doc.page_content[:40]}...")

# 저장
search.save()

# 나중에 로드
new_search = FastDocumentSearch()
new_search.load()
results = new_search.search("프로그래밍", k=2)
