# PrivatAI-RAG 

A **Privacy-Preserving, Zero-Trust Retrieval-Augmented Generation (RAG) System**  
built using **FastAPI, React, Qdrant, and Ollama**.

This project enables secure document upload, vector-based retrieval, and
local LLM-powered question answering without sharing data with external APIs.

---

##  Features

- JWT-based authentication (Signup / Login)
- Secure document upload & storage
-  Vector search using Qdrant
- Local LLM inference via Ollama (no cloud dependency)
-  Audit-ready architecture
-  Fully Dockerized (Frontend + Backend + Qdrant + Ollama)

---

##  Architecture Overview

```

Frontend (React + Nginx)
|
v
Backend (FastAPI)
|
+--> Qdrant (Vector DB)
|
+--> Ollama (Local LLM)

````

---

## 🛠️ Tech Stack

### Backend
- FastAPI
- SQLAlchemy (SQLite)
- Qdrant
- Ollama
- JWT Authentication

### Frontend
- React (Vite)
- Tailwind CSS
- Axios
- Nginx (production)

### LLM
- Ollama
- Model: `phi` (CPU-friendly)

---

## Setup Instructions

###  Prerequisites
- Docker & Docker Compose
- 8 GB RAM recommended (CPU-based inference)

---

### Clone the Repository

```bash
git clone https://github.com/your-username/privatai-rag.git
cd privatai-rag
````

---

### Start the System

```bash
docker compose up -d
```

>>First startup may take **1–2 minutes** due to model loading.

---

### Access Services

| Service     | URL                                                                |
| ----------- | ------------------------------------------------------------------ |
| Frontend    | [http://localhost:3000](http://localhost:3000)                     |
| Backend API | [http://localhost:8000](http://localhost:8000)                     |
| Swagger UI  | [http://localhost:8000/docs](http://localhost:8000/docs)           |
| Qdrant UI   | [http://localhost:6333/dashboard](http://localhost:6333/dashboard) |

---

## Authentication Flow

1. Sign up via frontend or Swagger
2. Login to receive JWT token
3. Token is stored in browser storage
4. Token is sent in `Authorization: Bearer <token>` header

---

## Using the System

1. Login
2. Upload documents (PDF / text)
3. Go to Query page
4. Ask questions about uploaded documents

 For faster responses on CPU:

* Use `top_k = 3`
* Ask concise questions

---

## Performance Notes

* LLM runs **locally on CPU**
* First query may be slow due to model warm-up
* Subsequent queries are faster
* Large `top_k` values increase latency

---

##  Documentation

- `docs/architecture.md` — System design and data flow
- `docs/api.md` — REST API endpoints and examples

---

##  License

This project is for academic and research purposes


---


## Author

**Chinmay Patil**  


