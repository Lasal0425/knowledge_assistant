# RAG Pipeline — Implementation Plan (Open-Source Stack)

Build a modular RAG assistant using **100% free, open-source tools** — no paid API keys needed.

---

## Tech Stack (Updated)

| Component | Tool | Why |
|-----------|------|-----|
| LLM | **Ollama** (`llama3`) | Free, runs locally |
| Embeddings | **Ollama** (`nomic-embed-text`) | Free, runs locally |
| Vector DB | **PostgreSQL + pgvector** | Production-grade vector search |
| Framework | **LangChain** | Orchestrates the RAG pipeline |
| API | **FastAPI** | Modern Python REST API |

---

## Prerequisites (Do These First)

### 1. Install Ollama
- Download from [ollama.com](https://ollama.com)
- After install, pull the two models you need:
```bash
ollama pull llama3
ollama pull nomic-embed-text
```

### 2. Install PostgreSQL + pgvector
- Download PostgreSQL 15+ from [postgresql.org](https://www.postgresql.org/download/)
- After install, enable the pgvector extension:
```sql
CREATE DATABASE rag_db;
\c rag_db
CREATE EXTENSION IF NOT EXISTS vector;
```

### 3. Install Python dependencies
Already done — but you'll also need:
```bash
pip install python-dotenv langchain-ollama
```

---

## Step-by-Step Build Guide

Below is every file you need to create, **in the order you should create them.** Each step explains *what* the file does, *why* it exists, and *what to code*.

---

### Step 1 — Project skeleton & config

Create these files at the project root (`c:\Users\ASUS\Desktop\Knowledge Assistant\`):

#### 📄 `.env`
> Stores your database connection string. No API keys needed since everything is local.

```env
DATABASE_URL=postgresql+psycopg2://postgres:yourpassword@localhost:5432/rag_db
```

#### 📄 `requirements.txt`
> Lists all dependencies so anyone can recreate your environment.

```
langchain
langchain-community
langchain-ollama
pgvector
psycopg2-binary
fastapi
uvicorn[standard]
pypdf
python-dotenv
```

#### 📁 `data/`
> Empty folder — you'll drop PDF files here for ingestion.

#### 📁 `app/` and `ingestion/`
> Create these two empty folders.

---

### Step 2 — `app/embeddings.py`
> **Purpose:** Wraps the embedding model so the rest of the app just calls `get_embeddings()`.

**What to code:**
- Import `OllamaEmbeddings` from `langchain_ollama`
- Create a function `get_embeddings()` that returns an `OllamaEmbeddings` instance using model `nomic-embed-text`
- This is a thin wrapper — keeps the model choice in one place

---

### Step 3 — `app/retriever.py`
> **Purpose:** Connects to PostgreSQL/pgvector and creates a retriever that finds the most relevant document chunks for a query.

**What to code:**
- Import `PGVector` from `langchain_community.vectorstores`
- Read `DATABASE_URL` from environment variables
- Create a function `get_retriever()` that:
  1. Creates a `PGVector` vectorstore using your embeddings and database URL
  2. Returns `.as_retriever(search_kwargs={"k": 4})` — this fetches the top 4 most similar chunks

---

### Step 4 — `app/prompts.py`
> **Purpose:** Defines the prompt template that tells the LLM *how* to answer using the retrieved context.

**What to code:**
- Import `ChatPromptTemplate` from `langchain_core.prompts`
- Create a `get_prompt()` function that returns a `ChatPromptTemplate` with:
  - A **system message** telling the LLM: "You are a helpful assistant. Answer the question using ONLY the provided context. If the context doesn't contain the answer, say so."
  - A **human message** with two placeholders: `{context}` and `{question}`

---

### Step 5 — `app/rag_pipeline.py`
> **Purpose:** This is the brain — it chains together Retriever → Prompt → LLM → Output into one pipeline.

**What to code:**
- Import `ChatOllama` from `langchain_ollama`
- Import `StrOutputParser` from `langchain_core.output_parsers`
- Import `RunnablePassthrough` from `langchain_core.runnables`
- Import your `get_retriever`, `get_embeddings`, and `get_prompt` functions
- Create a function `get_rag_chain()` that builds an **LCEL chain**:
  ```
  {"context": retriever, "question": RunnablePassthrough()} | prompt | llm | StrOutputParser()
  ```
- The chain flow is: User question → retrieve docs → fill prompt → send to LLM → parse output string

---

### Step 6 — `app/main.py`
> **Purpose:** The FastAPI server with the `/ask` endpoint.

**What to code:**
- Load `.env` using `dotenv`
- Create a FastAPI app
- Define a Pydantic model `QueryRequest` with a `question: str` field
- Define a Pydantic model `QueryResponse` with `answer: str` and `sources: list` fields
- On app startup (`@app.on_event("startup")`), initialize the RAG chain once
- Create `POST /ask` endpoint:
  1. Receives a `QueryRequest`
  2. Invokes the RAG chain with the question
  3. Returns the answer and source document metadata
- Create `GET /health` endpoint for a simple health check

---

### Step 7 — `ingestion/ingest_documents.py`
> **Purpose:** CLI script that reads PDFs from `data/`, chunks them, generates embeddings, and stores everything in PostgreSQL.

**What to code:**
- Import `PyPDFLoader` from `langchain_community.document_loaders`
- Import `RecursiveCharacterTextSplitter` from `langchain.text_splitter`
- Import `PGVector` from `langchain_community.vectorstores`
- Load `.env` for the database URL
- Scan the `data/` folder for all `.pdf` files
- For each PDF: load → split into chunks (size=1000, overlap=200)
- Use `PGVector.from_documents()` to embed and store all chunks
- Print progress messages

Run it with: `python -m ingestion.ingest_documents`

---

### Step 8 — `README.md`
> **Purpose:** Documentation for anyone (including future-you) to understand and run the project.

**What to include:**
- Project overview
- Architecture flow diagram
- Setup instructions (Ollama, PostgreSQL, Python deps)
- How to ingest documents
- How to start the server
- Example API request/response

---

## Architecture Flow

```mermaid
graph LR
    A[User Question] --> B[POST /ask]
    B --> C[Retriever - pgvector similarity search]
    C --> D[Top 4 document chunks]
    D --> E[Prompt Builder - inject context + question]
    E --> F[LLM - Ollama llama3]
    F --> G[Answer + Sources - JSON response]
```

---

## Verification Plan

### After you finish coding:

1. **Start Ollama** — make sure it's running (`ollama serve`)
2. **Ingest a test PDF** — drop a PDF in `data/`, run ingestion script
3. **Start the server** — `uvicorn app.main:app --reload`
4. **Test health** — `curl http://localhost:8000/health`
5. **Test a question**:
   ```bash
   curl -X POST http://localhost:8000/ask -H "Content-Type: application/json" -d "{\"question\": \"What is this document about?\"}"
   ```
