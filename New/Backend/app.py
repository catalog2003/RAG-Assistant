import time
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from New.Backend.api.routes import ask, history
from New.Backend.config import API_TITLE, API_VERSION, INDEX_PATH, METADATA_PATH
from New.Backend.api.routes import upload
from New.Backend.services.embeddings import EmbeddingModel
from New.Backend.services.vector_store import VectorStore
from New.Backend.services.retriever import Retriever
from New.Backend.indexing import index_all_pdfs
import os

embed_model = None
vector_store = None
retriever = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    global embed_model, vector_store, retriever
    print("Starting RAG Assistant API...")

    embed_model = EmbeddingModel()

    if os.path.exists(INDEX_PATH) and os.path.exists(METADATA_PATH):
        print("Loading existing index...")
        dim = embed_model.encode(["dummy"]).shape[1]
        vector_store = VectorStore.load(dim)
        print(f"Loaded index with {len(vector_store.metadata)} chunks")
    else:
        print("Building new index from PDFs...")
        vector_store, embed_model = index_all_pdfs(embed_model)
        if vector_store:
            print(f"Built index with {len(vector_store.metadata)} chunks")
        else:
            print("No PDFs found. upload some PDFs to get started!")
            dim = embed_model.encode(["dummy"]).shape[1]
            vector_store = VectorStore(dim)
    
    retriever = Retriever(vector_store, embed_model)
    upload.initialize_upload_router(embed_model, vector_store)
    ask.initialize_ask_router(retriever)
    print("api ready")
    yield
    print("shutting down")

app = FastAPI(
    title=API_TITLE,
    version=API_VERSION,
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=True,
)
    
app.include_router(upload.router)
app.include_router(ask.router)
app.include_router(history.router)

@app.get("/health", tags=["System"])
async def health_check():
    return {
        "status": "healthy",
        "version": API_VERSION,
        "index_loaded": vector_store is not None,
        "total_chunks": len(vector_store.metadata) if vector_store else 0,
        "embedding_model": embed_model.model_name if embed_model else None
    }

@app.get("/", tags=["System"])
async def root():
     return {
        "message": "RAG Assistant API",
        "version": API_VERSION,
        "endpoints": {
            "upload": "POST /upload/",
            "ask": "POST /ask/",
            "history": "GET /history/{session_id}",
            "docs": "/docs"
        }
    }

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={
            "status": "error",
            "message": str(exc),
            "path": request.url.path
        }
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app:app",
        host="0.0.0.0",
        port=8000,
        reload=False,
        log_level="info"
    )
