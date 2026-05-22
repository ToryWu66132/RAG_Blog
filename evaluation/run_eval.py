from rag.embedder import Embedder
from rag.retriever import Retriever
from rag.reranker import Reranker
from rag.chunker import chunk_text
from evaluation.evaluator import compare_retrieval

# 初始化
embedder = Embedder()
reranker = Reranker()

# 模拟数据
text = open("data/sample.txt").read()

chunks = chunk_text(text)
embeddings = embedder.encode(chunks)

retriever = Retriever(len(embeddings[0]))
retriever.add(embeddings, chunks)

# 测试问题
queries = [
    "什么是RAG？",
    "如何提高检索准确性？",
    "embedding有什么作用？"
]

for q in queries:
    result = compare_retrieval(q, retriever, reranker, embedder)

    print("\n==== Query ====")
    print(result["query"])

    print("\n--- Base ---")
    for d in result["base"]:
        print("-", d[:100])

    print("\n--- Rerank ---")
    for d in result["rerank"]:
        print("-", d[:100])