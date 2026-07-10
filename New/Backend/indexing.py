import os
import glob

from New.Backend.config import (
    DATA_DIR,
    CHUNK_SIZE,
    CHUNK_OVERLAP
)

from New.Backend.services.pdf_loader import load_pdf
from New.Backend.services.text_splitter import chunk_pages
from New.Backend.services.embeddings import EmbeddingModel
from New.Backend.services.vector_store import VectorStore


def index_all_pdfs(embed_model=None):

    all_chunks = []

    pdf_files = glob.glob(
        os.path.join(DATA_DIR, "*.pdf")
    )

    if embed_model is None:
        embed_model = EmbeddingModel()

    if not pdf_files:
        print("No PDFs found.")
        return None, embed_model

    for pdf_path in pdf_files:

        print(f"Processing {pdf_path}")

        pages = load_pdf(pdf_path)

        doc_name = os.path.basename(pdf_path)

        chunks = chunk_pages(
            pages,
            CHUNK_SIZE,
            CHUNK_OVERLAP,
            doc_name
        )

        all_chunks.extend(chunks)

    texts = [
        chunk["text"]
        for chunk in all_chunks
    ]

    embeddings = embed_model.encode(texts)

    vector_store = VectorStore(
        embeddings.shape[1]
    )

    vector_store.add(
        embeddings,
        all_chunks
    )

    vector_store.save()

    return vector_store, embed_model