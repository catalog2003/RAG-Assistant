import os

from New.Backend.config import (
    INDEX_PATH,
    METADATA_PATH
)

from project.services.embeddings import EmbeddingModel
from project.services.vector_store import VectorStore
from project.services.retriever import Retriever
from New.Backend.indexing import index_all_pdfs
from project.utils import remove_duplicates
from project.services.llm import (
    build_prompt,
    ask_hf_llm
)


def load_or_create_index():

    if (
        os.path.exists(INDEX_PATH)
        and os.path.exists(METADATA_PATH)
    ):
        print("Loading existing index...")

        embed_model = EmbeddingModel()

        dim = embed_model.encode(
            ["dummy"]
        ).shape[1]

        vector_store = VectorStore.load(dim)

        return vector_store, embed_model

    print("Building new index...")

    return index_all_pdfs()


def ask_question(retriever):

    query = input(
        "\n❓ Your question: "
    ).strip()

    if not query:
        return

    contexts = retriever.retrieve(query)

    contexts = remove_duplicates(
        contexts
    )

    print("\nRetrieved Sources:\n")

    for ctx in contexts:
        print(
            f"{ctx['document']} | "
            f"Page {ctx['page']} | "
            f"Score {ctx['score']:.3f}"
        )

    prompt = build_prompt(
        query,
        contexts
    )

    answer = ask_hf_llm(prompt)

    print("\nAnswer:\n")
    print(answer)


if __name__ == "__main__":

    vector_store, embed_model = (
        load_or_create_index()
    )

    retriever = Retriever(
        vector_store,
        embed_model
    )

    while True:
        ask_question(retriever)