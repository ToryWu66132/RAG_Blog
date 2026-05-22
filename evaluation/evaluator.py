def compare_retrieval(query, retriever, reranker, embedder):
    query_emb = embedder.encode([query])[0]

    # 原始检索
    base_docs = retriever.search(query_emb, k=3)

    # rerank检索
    candidates = retriever.search(query_emb, k=10)
    rerank_docs = reranker.rerank(query, candidates, top_k=3)

    return {
        "query": query,
        "base": base_docs,
        "rerank": rerank_docs
    }