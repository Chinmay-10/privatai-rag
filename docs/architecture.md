# System Architecture

PrivatAI-RAG is a privacy-preserving Retrieval-Augmented Generation (RAG) system
that enables users to query their documents using a locally hosted LLM.

---

## High-Level Architecture

```

User (Browser)
|
v
Frontend (React + Nginx)
|
v
Backend (FastAPI)
|        |
v        v
Qdrant   Ollama (Local LLM)

```

---

## Components

### Frontend
- Built with React and Tailwind CSS
- Handles authentication, document upload, and querying
- Communicates with backend via REST APIs

### Backend
- Built using FastAPI
- Manages authentication, document ingestion, embeddings, and querying
- Acts as the orchestrator between Qdrant and Ollama

### Qdrant
- Vector database for semantic search
- Stores document embeddings
- Returns top-k relevant chunks during queries

### Ollama
- Runs local LLM (`phi`) on CPU
- Generates answers using retrieved context
- Ensures no data leaves the local system

---

## Privacy & Security
- No external API calls
- Local-only LLM inference
- JWT-based authentication
- Documents never leave the host machine