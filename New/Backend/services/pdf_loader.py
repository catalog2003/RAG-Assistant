import fitz
from typing import List, Dict


def load_pdf(pdf_path: str) -> List[Dict]:
    pages = []

    doc = fitz.open(pdf_path)

    for page_num, page in enumerate(doc, start=1):
        text = page.get_text("text")
        text = " ".join(text.split())

        if text:
            pages.append({
                "page": page_num,
                "text": text
            })

    return pages