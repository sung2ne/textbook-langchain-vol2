from langchain_community.vectorstores import Chroma
from langchain_ollama import OllamaEmbeddings
from langchain_community.retrievers import BM25Retriever
from langchain.retrievers import EnsembleRetriever
from langchain_ollama import OllamaLLM
from langchain.prompts import PromptTemplate
from langchain_core.documents import Document
from sentence_transformers import CrossEncoder
from typing import List, Tuple, Optional
from dataclasses import dataclass


@dataclass
class SearchResult:
    documents: List[Tuple[Document, float]]
    query_analysis: QueryAnalysis
    strategy: SearchStrategy
    expanded_queries: Optional[List[str]] = None


class SearchPipeline:
    """통합 검색 파이프라인"""

    def __init__(self, documents: List[Document]):
        self.documents = documents

        # 컴포넌트 초기화
        self.embeddings = OllamaEmbeddings(model="nomic-embed-text")
        self.llm = OllamaLLM(model="llama4")
        self.vectorstore = Chroma.from_documents(documents, self.embeddings)
        self.bm25_retriever = BM25Retriever.from_documents(documents)
        self.reranker = CrossEncoder("cross-encoder/ms-marco-MiniLM-L-6-v2")

        # 분석기, 전략 선택기
        self.analyzer = QueryAnalyzer()
        self.selector = StrategySelector()

    def search(self, query: str) -> SearchResult:
        """검색 실행"""
        # 1. 쿼리 분석
        analysis = self.analyzer.analyze(query)

        # 2. 전략 선택
        strategy = self.selector.select(analysis)

        # 3. 쿼리 확장 (필요시)
        queries = [query]
        if strategy.use_query_expansion:
            expanded = self._expand_query(query)
            queries.extend(expanded)

        # 4. 초기 검색
        initial_results = self._initial_search(queries, strategy)

        # 5. 리랭킹
        if strategy.use_reranking and initial_results:
            final_results = self._rerank(query, initial_results, strategy.final_k)
        else:
            final_results = [(doc, 1.0) for doc in initial_results[:strategy.final_k]]

        return SearchResult(
            documents=final_results,
            query_analysis=analysis,
            strategy=strategy,
            expanded_queries=queries if len(queries) > 1 else None
        )

    def _expand_query(self, query: str) -> List[str]:
        """쿼리 확장"""
        prompt = PromptTemplate(
            template="다음 질문을 2개의 다른 표현으로 작성 (줄바꿈 구분): {query}\n확장:",
            input_variables=["query"]
        )

        chain = prompt | self.llm
        result = chain.invoke({"query": query})

        return [q.strip() for q in result.strip().split("\n") if q.strip()][:2]

    def _initial_search(self, queries: List[str], strategy: SearchStrategy) -> List[Document]:
        """초기 검색"""
        all_results = []
        seen_contents = set()

        for q in queries:
            if strategy.use_hybrid:
                self.bm25_retriever.k = strategy.initial_k // len(queries)
                vector_retriever = self.vectorstore.as_retriever(
                    search_kwargs={"k": strategy.initial_k // len(queries)}
                )

                ensemble = EnsembleRetriever(
                    retrievers=[self.bm25_retriever, vector_retriever],
                    weights=[strategy.bm25_weight, 1 - strategy.bm25_weight]
                )
                results = ensemble.invoke(q)
            else:
                results = self.vectorstore.similarity_search(
                    q, k=strategy.initial_k // len(queries)
                )

            for doc in results:
                if doc.page_content not in seen_contents:
                    seen_contents.add(doc.page_content)
                    all_results.append(doc)

        return all_results

    def _rerank(self, query: str, documents: List[Document],
                top_k: int) -> List[Tuple[Document, float]]:
        """리랭킹"""
        pairs = [[query, doc.page_content] for doc in documents]
        scores = self.reranker.predict(pairs)

        doc_scores = list(zip(documents, scores))
        doc_scores.sort(key=lambda x: x[1], reverse=True)

        return doc_scores[:top_k]


# 사용
documents = [
    Document(page_content="LangChain은 LLM 앱 개발 프레임워크입니다. 체인과 에이전트를 제공합니다."),
    Document(page_content="LlamaIndex는 데이터 인덱싱에 특화된 프레임워크입니다."),
    Document(page_content="RAG는 검색 증강 생성으로 외부 지식을 활용합니다."),
    Document(page_content="벡터 DB는 임베딩을 저장하고 유사도 검색을 수행합니다."),
    Document(page_content="ChromaDB는 사용하기 쉬운 벡터 데이터베이스입니다."),
    Document(page_content="Python은 AI 개발에 많이 사용되는 언어입니다."),
]

pipeline = SearchPipeline(documents)

# 검색 테스트
queries = [
    "LangChain이 뭐야?",
    "LangChain과 LlamaIndex 비교",
    "RAG 시스템 어떻게 구축해?",
]

for q in queries:
    print(f"\n{'='*50}")
    print(f"쿼리: {q}")

    result = pipeline.search(q)

    print(f"타입: {result.query_analysis.query_type.value}")
    print(f"전략: 하이브리드={result.strategy.use_hybrid}, BM25={result.strategy.bm25_weight}")

    if result.expanded_queries:
        print(f"확장: {result.expanded_queries}")

    print("\n검색 결과:")
    for doc, score in result.documents:
        print(f"  [{score:.4f}] {doc.page_content[:50]}...")
