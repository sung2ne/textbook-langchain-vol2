from langchain.chains import RetrievalQA
from langchain_community.vectorstores import Chroma
from langchain_ollama import OllamaEmbeddings
from langchain_ollama import OllamaLLM
from langchain.prompts import PromptTemplate
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_core.documents import Document


class RAGSystem:
    """완전한 RAG 시스템"""

    def __init__(self, persist_dir="./rag_db"):
        self.embeddings = OllamaEmbeddings(model="nomic-embed-text")
        self.llm = OllamaLLM(model="llama4")
        self.persist_dir = persist_dir
        self.vectorstore = None
        self.qa_chain = None

        self.splitter = RecursiveCharacterTextSplitter(
            chunk_size=500,
            chunk_overlap=50
        )

        self.prompt = PromptTemplate(
            template="""당신은 친절한 AI 어시스턴트입니다.
주어진 문맥을 바탕으로 질문에 답하세요.
문맥에 답이 없으면 솔직히 모른다고 말하세요.

문맥:
{context}

질문: {question}

답변:""",
            input_variables=["context", "question"]
        )

    def load_documents(self, documents):
        """문서 로드 및 인덱싱"""
        # 분할
        split_docs = self.splitter.split_documents(documents)
        print(f"원본: {len(documents)}개 → 분할: {len(split_docs)}개")

        # 벡터 저장소 생성
        self.vectorstore = Chroma.from_documents(
            split_docs,
            self.embeddings,
            persist_directory=self.persist_dir
        )

        # QA 체인 생성
        self._create_qa_chain()

        print("인덱싱 완료")

    def load_from_disk(self):
        """디스크에서 로드"""
        self.vectorstore = Chroma(
            persist_directory=self.persist_dir,
            embedding_function=self.embeddings
        )
        self._create_qa_chain()
        print(f"로드 완료: {self.vectorstore._collection.count()}개 문서")

    def _create_qa_chain(self):
        """QA 체인 생성"""
        retriever = self.vectorstore.as_retriever(
            search_type="mmr",
            search_kwargs={"k": 3, "fetch_k": 10}
        )

        self.qa_chain = RetrievalQA.from_chain_type(
            llm=self.llm,
            chain_type="stuff",
            retriever=retriever,
            return_source_documents=True,
            chain_type_kwargs={"prompt": self.prompt}
        )

    def ask(self, question):
        """질문에 답변"""
        if self.qa_chain is None:
            raise ValueError("먼저 문서를 로드하세요")

        result = self.qa_chain.invoke(question)

        return {
            "answer": result["result"],
            "sources": [
                {
                    "content": doc.page_content[:100] + "...",
                    "metadata": doc.metadata
                }
                for doc in result["source_documents"]
            ]
        }

    def search(self, query, k=5):
        """문서 검색만"""
        if self.vectorstore is None:
            raise ValueError("먼저 문서를 로드하세요")

        return self.vectorstore.similarity_search(query, k=k)


# 사용
rag = RAGSystem()

# 샘플 문서
documents = [
    Document(
        page_content="""LangChain은 대규모 언어 모델(LLM)을 활용한 애플리케이션을
        개발하기 위한 프레임워크입니다. 2022년 10월에 처음 출시되었으며,
        체인, 에이전트, 메모리 등의 개념을 제공합니다.

        LangChain의 주요 구성 요소:
        - 체인(Chains): 여러 LLM 호출을 연결
        - 에이전트(Agents): 도구를 사용하는 자율적 LLM
        - 메모리(Memory): 대화 기록 저장
        - 검색(Retrieval): 외부 데이터 검색""",
        metadata={"source": "langchain_docs", "topic": "overview"}
    ),
    Document(
        page_content="""RAG(Retrieval-Augmented Generation)는 검색 증강 생성으로,
        LLM의 한계를 극복하는 기술입니다.

        RAG의 작동 방식:
        1. 사용자 질문을 임베딩으로 변환
        2. 벡터 데이터베이스에서 유사한 문서 검색
        3. 검색된 문서를 컨텍스트로 LLM에 전달
        4. LLM이 컨텍스트를 참고하여 답변 생성

        장점: 최신 정보 활용, 할루시네이션 감소, 출처 제공 가능""",
        metadata={"source": "rag_tutorial", "topic": "rag"}
    ),
    Document(
        page_content="""벡터 데이터베이스는 임베딩 벡터를 저장하고
        유사도 검색을 수행하는 특수한 데이터베이스입니다.

        주요 벡터 데이터베이스:
        - ChromaDB: 쉬운 시작, 로컬 개발에 적합
        - FAISS: 고성능, 대규모 데이터
        - Pinecone: 관리형 서비스
        - Milvus: 분산 처리, 기업용""",
        metadata={"source": "vectordb_guide", "topic": "database"}
    ),
]

# 문서 로드
rag.load_documents(documents)

# 질문
print("\n=== Q&A ===")
questions = [
    "LangChain의 주요 구성 요소는?",
    "RAG는 어떻게 작동해?",
    "벡터 데이터베이스 종류를 알려줘",
]

for q in questions:
    print(f"\nQ: {q}")
    result = rag.ask(q)
    print(f"A: {result['answer']}")
    print(f"출처: {result['sources'][0]['metadata'].get('source', 'unknown')}")
