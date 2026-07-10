import torch
import numpy as np
from sentence_transformers import SentenceTransformer

from New.Backend.config import EMBEDDING_MODEL


class EmbeddingModel:

    def __init__(self):
        self.device = (
            "cuda"
            if torch.cuda.is_available()
            else "cpu"
        )

        self.model = SentenceTransformer(
            EMBEDDING_MODEL,
            device=self.device
        )
        self.model_name = EMBEDDING_MODEL

        print(
            f"Embedding model running on {self.device}"
        )

    def encode(self, texts):
        embeddings = self.model.encode(
            texts,
            batch_size=64,
            convert_to_numpy=True,
            normalize_embeddings=True,
            show_progress_bar=True
        )

        return embeddings.astype(np.float32)