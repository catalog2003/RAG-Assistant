import os
import shutil
from fastapi import APIRouter, UploadFile, File, HTTPException
from New.Backend.config import DATA_DIR, CHUNK_SIZE, CHUNK_OVERLAP, MAX_UPLOAD_SIZE

from New.Backend.services.pdf_loader import load_pdf
from New.Backend.services.text_splitter import chunk_pages
from New.Backend.services.embeddings import EmbeddingModel
from New.Backend.services.vector_store import VectorStore
from New.Backend.api.models.schemas import UploadResponse

router = APIRouter(prefix="/upload", tags=["Upload"])

embed_model = None
vector_store = None

def initialize_upload_router(emb_model, vec_store):
    global embed_model, vector_store
    embed_model = emb_model
    vector_store = vec_store

@router.post("/", response_model=UploadResponse)
async def upload_pdf(file: UploadFile = File(...)):

    if not file.filename.endswith(".pdf"):
        raise HTTPException(400, "only PDF files are allowed")
    
    content = await file.read()
    if len(content) > MAX_UPLOAD_SIZE:
        raise HTTPException(400, f"file too large. Max {MAX_UPLOAD_SIZE/1024/1024}MB")
    
    os.makedirs(DATA_DIR, exist_ok=True)
    file_path = os.path.join(DATA_DIR, file.filename)

    with open(file_path, "wb") as f:
        f.write(content)
    try:
        pages = load_pdf(file_path)

        if not pages:
            raise HTTPException(400, "No text extracted from PDF")
        
        chunks = chunk_pages(pages,CHUNK_SIZE, CHUNK_OVERLAP, file.filename)

        if not chunks:
            raise HTTPException(400, "Failed to create chunks from PDF")
        
        chunks_texts = [c["text"] for c in chunks]
        new_embeddings = embed_model.encode(chunks_texts)

        vector_store.add(new_embeddings, chunks)
        vector_store.save()

        return UploadResponse(
            status="success",
            document=file.filename,
            chunks_created=len(chunks),
            message= f"Successfully indexed {len(chunks)} chunks"
        )
    except Exception as e:
        if os.path.exists(file_path):
            os.remove(file_path)
        raise HTTPException(500, f"Error processing PDF: {str(e)}")

@router.get("/list")
async def list_documents():
    if not vector_store:
        raise HTTPException(500, "Vector store not initialized")
    documents = set()
    for metadata in vector_store.metadata:
        documents.add(metadata["document"])
    return {"documents": sorted(list(documents)),
            "total_documents": len(documents),
            "total_chunks": len(vector_store.metadata)}

@router.delete("/{document_name}")
async def delete_document(document_name: str):
    if not vector_store:
        raise HTTPException(500, "Vector store not initialized")
    
    chunks_to_keep = []
    indices_to_keep = []

    for i, meta in enumerate(vector_store.metadata):
        if meta["document"] != document_name:
            chunks_to_keep.append(meta)
            indices_to_keep.append(i)
    
    if len(chunks_to_keep) == len(vector_store.metadata):
        raise HTTPException(404, f"Document {document_name} not found in index")
    
    dim = vector_store.dimension
    new_vector_store = VectorStore(dim)

    if chunks_to_keep:
        text_to_keep = [c["text"] for c in chunks_to_keep]
        embeddings_to_keep = embed_model.encode(text_to_keep)
        new_vector_store.add(embeddings_to_keep, chunks_to_keep)
    
    vector_store_index = new_vector_store.index
    vector_store.metadata = new_vector_store.metadata
    vector_store.save()

    pdf_path = os.path.join(DATA_DIR, document_name)
    if os.path.exists(pdf_path):
        os.remove(pdf_path)
    
    return {
        "status": "success",
        "message": f"Document '{document_name}' deleted successfully"
    }




    

