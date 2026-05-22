from sentence_transformers import SentenceTransformer
import numpy as np


class Embedder:
    def __init__(self):
        """
        使用更适合中文语义检索的 embedding 模型
        BGE 在中文检索任务上明显优于 MiniLM
        """

        self.model = SentenceTransformer(
            "BAAI/bge-small-zh-v1.5",
            cache_folder="./models"  # 本地缓存目录（推荐）
        )

    def encode(self, texts):
        """
        将文本列表转为向量列表

        参数:
            texts: List[str]

        返回:
            numpy.ndarray
        """

        embeddings = self.model.encode(
            texts,
            batch_size=32,                 # 批处理，加速
            normalize_embeddings=True,     # 非常重要！
            convert_to_numpy=True,         # 更适合 FAISS
            show_progress_bar=False
        )

        return embeddings
