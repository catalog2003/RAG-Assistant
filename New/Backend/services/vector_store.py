import os
import pickle
import faiss
import numpy as np
from typing import List, Dict

from New.Backend.config import (
    STORAGE_DIR,
    INDEX_PATH,
    METADATA_PATH
)


class VectorStore:

    def __init__(self, dimension: int):
        self.dimension = dimension

        self.index = faiss.IndexFlatIP(
            dimension
        )

        self.metadata: List[Dict] = []

    def add(
        self,
        embeddings: np.ndarray,
        metadata: List[Dict]
    ):
        if embeddings.shape[0] != len(metadata):
            raise ValueError(
                "Mismatch between embeddings and metadata"
            )

        self.index.add(embeddings)
        self.metadata.extend(metadata)

    def search(
        self,
        query_embedding: np.ndarray,
        k: int
    ):
        scores, indices = self.index.search(
            query_embedding,
            k
        )

        return scores[0], indices[0]

    def save(self):
        os.makedirs(STORAGE_DIR, exist_ok=True)

        faiss.write_index(
            self.index,
            INDEX_PATH
        )

        with open(
            METADATA_PATH,
            "wb"
        ) as f:
            pickle.dump(self.metadata, f)

    @classmethod
    def load(cls, dimension):
        obj = cls(dimension)

        obj.index = faiss.read_index(
            INDEX_PATH
        )

        with open(
            METADATA_PATH,
            "rb"
        ) as f:
            obj.metadata = pickle.load(f)

        return obj