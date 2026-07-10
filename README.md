# 📚 RAG Assistant - Retrieval-Augmented Generation Application

A full-stack web application that combines a powerful **Retrieval-Augmented Generation (RAG)** system with an intuitive user interface. Upload your PDF documents and get intelligent answers based on your knowledge base using advanced embedding models and language models.

![Python](https://img.shields.io/badge/Python-3.8+-blue?logo=python)
![React](https://img.shields.io/badge/React-19.2+-blue?logo=react)
![FastAPI](https://img.shields.io/badge/FastAPI-latest-green?logo=fastapi)
![License](https://img.shields.io/badge/License-MIT-green)

---

## ✨ Features

- **📤 PDF Upload & Processing** - Upload multiple PDF documents and automatically extract and index content
- **🔍 Smart Retrieval** - Uses FAISS vector store with semantic search to find relevant documents
- **🤖 AI-Powered Responses** - Generates contextual answers using Microsoft Phi-3 mini LLM
- **💬 Chat History** - Maintains conversation history for better context awareness
- **⚡ Fast & Responsive UI** - React frontend with smooth animations and real-time updates
- **🔐 API-First Architecture** - RESTful FastAPI backend for easy integration
- **🧠 Advanced Embeddings** - Uses intfloat/e5-large-v2 for high-quality semantic embeddings

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    Frontend (React + Vite)              │
│          ChatWindow | UploadBox | ChatHistory           │
└────────────────────────┬────────────────────────────────┘
                         │ HTTP/REST
                         ▼
┌─────────────────────────────────────────────────────────┐
│                  Backend (FastAPI)                       │
│  ┌─────────────┐  ┌──────────────┐  ┌──────────────┐   │
│  │   Upload    │  │     Ask      │  │   History    │   │
│  │    Route    │  │    Route     │  │    Route     │   │
│  └──────┬──────┘  └──────┬───────┘  └──────┬───────┘   │
│         │                │                  │            │
│  ┌──────▼────────────────▼──────────────────▼────────┐  │
│  │              Services Layer                       │  │
│  │  Embeddings | Retriever | LLM | PDF Loader      │  │
│  └──────┬───────────────────────────────────┬────────┘  │
│         │                                   │            │
│  ┌──────▼─────────────────┐  ┌─────────────▼────────┐  │
│  │  Vector Store (FAISS)  │  │  Chat History (JSON) │  │
│  └────────────────────────┘  └──────────────────────┘  │
└─────────────────────────────────────────────────────────┘
```

---

## 🚀 Quick Start

### Prerequisites
- **Python 3.8+**
- **Node.js 16+** and npm/yarn
- **Git**

### Backend Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/rag-assistant.git
   cd rag-assistant/Backend
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment variables** (create `.env` file if needed)
   ```
   # Optional configuration for LLM models and API settings
   ```

5. **Run the backend server**
   ```bash
   python app.py
   ```
   Server will start at `http://localhost:8000`

### Frontend Setup

1. **Navigate to frontend directory**
   ```bash
   cd ../Frontend
   ```

2. **Install dependencies**
   ```bash
   npm install
   ```

3. **Start development server**
   ```bash
   npm run dev
   ```
   Frontend will be available at `http://localhost:5173`

---

## 📖 API Endpoints

### Upload Documents
**POST** `/upload`
- Upload PDF files to the knowledge base
- **Request**: Form data with `files` field containing PDF files
- **Response**: Status and number of chunks created

```bash
curl -X POST -F "files=@document.pdf" http://localhost:8000/upload
```

### Ask Questions
**POST** `/ask`
- Query the knowledge base with a question
- **Request Body**:
  ```json
  {
    "question": "What is the main topic?",
    "session_id": "user-session-123"
  }
  ```
- **Response**:
  ```json
  {
    "answer": "Generated answer based on documents...",
    "sources": ["doc1.pdf", "doc2.pdf"],
    "session_id": "user-session-123"
  }
  ```

### Chat History
**GET** `/history/{session_id}`
- Retrieve conversation history for a session

**DELETE** `/history/{session_id}`
- Clear conversation history for a session

---

## 🛠️ Project Structure

```
rag-assistant/
├── Backend/
│   ├── app.py                      # FastAPI application entry point
│   ├── config.py                   # Configuration settings
│   ├── requirements.txt            # Python dependencies
│   ├── indexing.py                 # PDF indexing logic
│   ├── main.py                     # Alternative entry point
│   ├── utils.py                    # Utility functions
│   │
│   ├── api/
│   │   ├── models/
│   │   │   └── schemas.py          # Pydantic request/response schemas
│   │   └── routes/
│   │       ├── ask.py              # Question answering endpoint
│   │       ├── history.py          # Chat history endpoint
│   │       └── upload.py           # PDF upload endpoint
│   │
│   ├── services/
│   │   ├── embeddings.py           # Embedding model service
│   │   ├── retriever.py            # Document retrieval logic
│   │   ├── llm.py                  # Language model service
│   │   ├── pdf_loader.py           # PDF processing
│   │   ├── text_splitter.py        # Text chunking
│   │   ├── vector_store.py         # FAISS vector store
│   │   └── history.py              # Chat history management
│   │
│   └── storage/
│       ├── faiss.index             # Vector index file
│       ├── metadata.pkl            # Document metadata
│       ├── chat_history.json       # Conversation history
│       └── pdfs/                   # Uploaded PDF directory
│
├── Frontend/
│   ├── index.html                  # HTML entry point
│   ├── package.json                # NPM dependencies
│   ├── vite.config.js              # Vite configuration
│   │
│   ├── src/
│   │   ├── main.jsx                # React entry point
│   │   ├── App.jsx                 # Main App component
│   │   ├── App.css                 # Global styles
│   │   │
│   │   ├── components/
│   │   │   ├── ChatWindow.jsx      # Main chat interface
│   │   │   ├── Message.jsx         # Individual message component
│   │   │   └── UploadBox.jsx       # PDF upload component
│   │   │
│   │   ├── pages/
│   │   │   └── ChatPage.jsx        # Chat page container
│   │   │
│   │   └── services/
│   │       └── api.js              # API client (Axios)
│   │
│   └── public/                     # Static assets
│
├── RAG.ipynb                       # Jupyter notebook for experimentation
├── data/                           # Data directory
└── README.md                       # This file
```

---

## 📦 Technology Stack

### Backend
- **FastAPI** - Modern, fast web framework for building APIs
- **Uvicorn** - ASGI web server
- **PyMuPDF** - PDF processing and text extraction
- **Sentence-Transformers** - High-quality embeddings (e5-large-v2)
- **FAISS** - Efficient similarity search and clustering
- **Transformers** - Hugging Face transformers for LLM (Phi-3-mini)
- **NumPy & SciPy** - Numerical computing

### Frontend
- **React 19** - UI library
- **Vite** - Fast build tool and dev server
- **Tailwind CSS** - Utility-first CSS framework
- **Axios** - HTTP client
- **Framer Motion** - Animation library
- **React Markdown** - Markdown renderer

---

## 🔧 Configuration

Edit [Backend/config.py](Backend/config.py) to customize:

| Setting | Default | Description |
|---------|---------|-------------|
| `CHUNK_SIZE` | 300 | Text chunk size for splitting |
| `CHUNK_OVERLAP` | 50 | Overlap between chunks |
| `EMBEDDING_MODEL` | intfloat/e5-large-v2 | Sentence transformer model |
| `LLM_MODEL_NAME` | microsoft/Phi-3-mini-4k-instruct | Language model to use |
| `TOP_K` | 3 | Number of documents to retrieve |
| `MAX_UPLOAD_SIZE` | 10MB | Maximum file upload size |

---

## 💾 Data Flow

### Document Upload Flow
1. User uploads PDF via frontend
2. Backend receives file and extracts text using PyMuPDF
3. Text is split into chunks (300 tokens with 50-token overlap)
4. Chunks are embedded using e5-large-v2 model
5. Embeddings stored in FAISS index with metadata
6. Metadata saved to disk for persistence

### Question Answering Flow
1. User asks a question via chat interface
2. Question is embedded using the same model
3. FAISS retrieves top-3 most similar document chunks
4. Retrieved context + question sent to Phi-3 LLM
5. LLM generates contextual answer
6. Response sent back to frontend with source documents
7. Conversation saved to chat history

---

## 🚦 Running Tests

```bash
# Backend API testing
cd Backend
python test_api.py
```

---

## 📝 Usage Examples

### Upload Documents via API
```python
import requests

files = [('files', open('document.pdf', 'rb'))]
response = requests.post('http://localhost:8000/upload', files=files)
print(response.json())
```

### Query the System
```python
import requests

payload = {
    "question": "What are the main topics covered?",
    "session_id": "user-123"
}
response = requests.post('http://localhost:8000/ask', json=payload)
print(response.json()['answer'])
```

---

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## ⚠️ Known Limitations

- PDF extraction works best with text-based PDFs (not scanned images)
- Large documents may require more processing time
- Model inference speed depends on hardware (GPU recommended)
- Currently stores data in local storage (not distributed)

---

## 🚀 Future Enhancements

- [ ] Add user authentication and multi-user support
- [ ] Implement streaming responses for real-time updates
- [ ] Add support for more document formats (DOCX, TXT, etc.)
- [ ] Database persistence (PostgreSQL/MongoDB)
- [ ] Advanced filtering and document management UI
- [ ] GPU optimization and model quantization
- [ ] Docker containerization for easy deployment

---

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

---

## 🤖 About RAG

**Retrieval-Augmented Generation (RAG)** combines:
- **Retrieval**: Finding relevant information from your knowledge base
- **Augmentation**: Adding context from retrieved documents
- **Generation**: Using a language model to generate answers based on context

This approach allows the AI to provide accurate, grounded answers without needing to retrain the model for each new knowledge base.

---

## 📞 Support & Contact

For issues, questions, or suggestions:
- Open an issue on GitHub
- Check existing discussions
- Submit a pull request with improvements

---

## 🙏 Acknowledgments

- [Hugging Face](https://huggingface.co/) - For pre-trained models
- [FastAPI](https://fastapi.tiangolo.com/) - For the excellent web framework
- [FAISS](https://github.com/facebookresearch/faiss) - For efficient similarity search

---

**Built with ❤️ | Made with Python & React**
