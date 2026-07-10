import os
from dotenv import load_dotenv

load_dotenv()

# Paths
DATA_DIR = "storage/pdfs"
STORAGE_DIR = "storage"
INDEX_PATH = os.path.join(STORAGE_DIR, "faiss.index")
METADATA_PATH = os.path.join(STORAGE_DIR, "metadata.pkl")
HISTORY_PATH = os.path.join(STORAGE_DIR, "chat_history.json")

# Chunking
CHUNK_SIZE = 300
CHUNK_OVERLAP = 50

# Embedding
EMBEDDING_MODEL = "intfloat/e5-large-v2"

# Retrieval
TOP_K = 3

# LLM (Hugging Face)
LLM_MODEL_NAME = "microsoft/Phi-3-mini-4k-instruct"

# API Settings
API_TITLE = "RAG Assistant API"
API_VERSION = "2.0.0"
MAX_UPLOAD_SIZE = 10 * 1024 * 1024  # 10MB