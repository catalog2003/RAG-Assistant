from New.Backend.config import TOP_K


class Retriever:

    def __init__(
        self,
        vector_store,
        embed_model
    ):
        self.vector_store = vector_store
        self.embed_model = embed_model

    def retrieve(
        self,
        query,
        top_k=TOP_K
    ):
        query_vec = self.embed_model.encode(
            [query]
        )

        scores, indices = self.vector_store.search(
            query_vec,
            top_k
        )

        results = []

        for idx, score in zip(indices, scores):

            if idx != -1:
                chunk = self.vector_store.metadata[idx].copy()

                chunk["score"] = float(score)

                results.append(chunk)

        return results