def check_environment():
    """환경 확인"""
    checks = []

    # Python 버전
    import sys
    py_version = sys.version_info
    checks.append(("Python 3.10+", py_version >= (3, 10)))

    # LangChain
    try:
        import langchain
        checks.append(("LangChain", True))
    except ImportError:
        checks.append(("LangChain", False))

    # Ollama 임베딩
    try:
        from langchain_ollama import OllamaEmbeddings
        emb = OllamaEmbeddings(model="nomic-embed-text")
        emb.embed_query("test")
        checks.append(("Ollama 임베딩", True))
    except Exception as e:
        checks.append(("Ollama 임베딩", False))

    # ChromaDB
    try:
        import chromadb
        checks.append(("ChromaDB", True))
    except ImportError:
        checks.append(("ChromaDB", False))

    # FAISS
    try:
        import faiss
        checks.append(("FAISS", True))
    except ImportError:
        checks.append(("FAISS", False))

    # FastAPI
    try:
        import fastapi
        checks.append(("FastAPI", True))
    except ImportError:
        checks.append(("FastAPI", False))

    # 결과 출력
    print("=== 환경 확인 ===")
    all_pass = True
    for name, passed in checks:
        status = "✅" if passed else "❌"
        print(f"{status} {name}")
        if not passed:
            all_pass = False

    if all_pass:
        print("\n🎉 모든 환경이 준비되었습니다!")
    else:
        print("\n⚠️ 일부 항목을 설치해주세요.")


if __name__ == "__main__":
    check_environment()
