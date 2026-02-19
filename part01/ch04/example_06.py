import asyncio
from langchain_ollama import OllamaEmbeddings


async def async_embed_documents(embeddings, texts):
    """비동기 임베딩"""
    # aembed_documents 메서드 사용
    vectors = await embeddings.aembed_documents(texts)
    return vectors


async def async_embed_query(embeddings, query):
    """비동기 질문 임베딩"""
    vector = await embeddings.aembed_query(query)
    return vector


# 여러 작업 동시 실행
async def main():
    embeddings = OllamaEmbeddings(model="nomic-embed-text")

    # 병렬 실행
    tasks = [
        async_embed_query(embeddings, "질문 1"),
        async_embed_query(embeddings, "질문 2"),
        async_embed_query(embeddings, "질문 3"),
    ]

    results = await asyncio.gather(*tasks)
    print(f"병렬 처리 완료: {len(results)}개")


# 실행
asyncio.run(main())
