from typing import List, Dict


def split_text(text, chunk_size=500, overlap=75):
    words = text.split()

    chunks = []
    current = []
    current_len = 0

    for word in words:
        if current_len + len(word) + 1 <= chunk_size:
            current.append(word)
            current_len += len(word) + 1
        else:
            chunks.append(" ".join(current))

            overlap_words = current[-15:] if len(current) > 15 else current

            current = overlap_words + [word]
            current_len = len(" ".join(current))

    if current:
        chunks.append(" ".join(current))

    return chunks


def chunk_pages(
    pages: List[Dict],
    chunk_size: int,
    overlap: int,
    doc_name: str
):
    chunks = []
    chunk_id = 0

    for page in pages:
        page_num = page["page"]
        page_text = page["text"]

        page_text = page_text.replace("\n", " ")
        page_text = " ".join(page_text.split())

        split_chunks = split_text(
            page_text,
            chunk_size,
            overlap
        )

        for chunk_text in split_chunks:
            if chunk_text.strip():
                chunks.append({
                    "chunk_id": chunk_id,
                    "document": doc_name,
                    "page": page_num,
                    "text": chunk_text.strip()
                })

                chunk_id += 1

    return chunks