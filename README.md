# 🧠 Knowledge Assistant

Knowledge Assistant is a powerful **Retrieval-Augmented Generation (RAG)** system designed to help you interact with your documents locally. Built with **FastAPI**, **LangChain**, and **Ollama**, it leverages the efficiency of **pgvector** for high-performance similarity search.

---

## ✨ Key Features

- **Local-First AI**: Runs entirely on your machine using **Ollama** (Llama 3).
- **PDF Ingestion**: Automatically process and chunk PDF documents for search.
- **Vector Storage**: Uses **PostgreSQL** with the `pgvector` extension for semantic search.
- **RESTful API**: Simple FastAPI endpoints to query your knowledge base.
- **LCEL Integration**: Uses LangChain Expression Language (LCEL) for a robust processing pipeline.

---

## 🏗️ Architecture Overview

The system consists of two primary pipelines:

1.  **Ingestion Pipeline**: 
    - Loads PDFs from the `data/` directory.
    - Splits text into manageable chunks using a recursive splitter.
    - Generates embeddings and stores them in **pgvector**.

2.  **Query Pipeline**:
    - Receives user questions via a FastAPI endpoint.
    - Retrieves relevant context from the vector database.
    - Augments the LLM prompt with retrieved context to generate accurate answers.

---

## 🛠️ Tech Stack

- **Large Language Model (LLM)**: [Ollama](https://ollama.com/) (Llama 3)
- **Framework**: [LangChain](https://www.langchain.com/)
- **API Backend**: [FastAPI](https://fastapi.tiangolo.com/)
- **Database**: [PostgreSQL](https://www.postgresql.org/) with [pgvector](https://github.com/pgvector/pgvector)
- **Embeddings**: LangChain Ollama Embeddings

---

## 🚀 Getting Started

### Prerequisites

- **Python 3.10+**
- **Docker** (for running PostgreSQL/pgvector)
- **Ollama** (with the `llama3` model pulled)

### Installation

1.  **Clone the repository**:
    ```bash
    git clone https://github.com/yourusername/knowledge-assistant.git
    cd knowledge-assistant
    ```

2.  **Set up a virtual environment**:
    ```bash
    python -m venv .venv
    # On Windows:
    .\.venv\Scripts\activate
    # On macOS/Linux:
    source .venv/bin/activate
    ```

3.  **Install dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

4.  **Configure Environment Variables**:
    Create a `.env` file in the root directory:
    ```env
    DATABASE_URL=postgresql://user:password@localhost:5432/dbname
    ```

---

## 📖 Usage Guide

### 1. Ingest Documents

Place your PDF files in the `data/` folder, then run the ingestion script:

```bash
python ingestion/ingest_documents.py
```

### 2. Start the API Server

Run the FastAPI server using Uvicorn:

```bash
uvicorn app.main:app --reload
```

The server will be available at `http://127.0.0.1:8000`.

### 3. Query the Assistant

You can ask questions using `curl` or any API client:

```bash
curl -X POST "http://127.0.0.1:8000/ask" \
     -H "Content-Type: application/json" \
     -d '{"question": "How does the RAG pipeline work?"}'
```

---

## 📁 Project Structure

```text
Knowledge Assistant/
├── app/                  # FastAPI Application logic
│   ├── main.py           # API endpoints and server setup
│   ├── rag_pipeline.py   # RAG chain definition
│   ├── retriever.py      # Vector store retriever logic
│   └── ...
├── ingestion/            # Document processing scripts
│   └── ingest_documents.py # PDF to Vector Store pipeline
├── data/                 # Directory for your PDF documents
├── requirements.txt      # Project dependencies
└── README.md             # Project documentation
```

---

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📄 License

This project is licensed under the MIT License.
