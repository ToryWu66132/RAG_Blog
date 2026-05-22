from sentence_transformers import CrossEncoder


class Reranker:
    def __init__(self):
        # 加载模型
        self.model = CrossEncoder("cross-encoder/ms-marco-MiniLM-L-6-v2")

    def rerank(self, query, docs, top_k=3):
        # 构建输入对
        pairs = [(query, doc) for doc in docs]

        # 打分
        scores = self.model.predict(pairs)

        # 将打分进行压缩
        scored_docs = list(zip(docs, scores))

        # 按分数排序
        ranked = sorted(scored_docs, key=lambda x: x[1], reverse=True)

        return [doc for doc, _ in ranked[:top_k]]
