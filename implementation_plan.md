# How to Run Knowledge Assistant

This guide outlines the steps to get the Knowledge Assistant up and running. 

## User Review Required

> [!IMPORTANT]
> Ensure **Ollama** is running on your machine.
> Ensure **PostgreSQL** is running on port 5432 with a database named `rag_db`.

## Proposed Steps

### 1. Environment Setup

*   **Python Version**: Ensure you are using Python 3.10 or higher.
*   **Virtual Environment**: It is recommended to use the existing `.venv`.
    ```powershell
    .\.venv\Scripts\activate
    ```
*   **Install Dependencies**:
    ```powershell
    pip install -r requirements.txt
    ```

### 2. Ingest Documents

Place your PDF files in the `data/` directory. (Currently, there is one PDF: `AIESEC Mail - [IMP] Update on NatCon 2026 CCM Selection.pdf`)

Run the ingestion script to process the documents and store them in the vector database:
```powershell
python ingestion/ingest_documents.py
```

### 3. Start the API Server

Run the FastAPI server using Uvicorn:
```powershell
uvicorn app.main:app --reload
```

### 4. Query the Assistant

Once the server is running, you can test it by sending a POST request to `http://127.0.0.1:8000/ask`.

Example using PowerShell:
```powershell
Invoke-RestMethod -Uri "http://127.0.0.1:8000/ask" -Method Post -ContentType "application/json" -Body '{"question": "What is the update on NatCon 2026 CCM Selection?"}'
```

---

## Verification Plan

### Automated Tests
*   Run the provided [test_rag.py](file:///c:/Users/ASUS/Desktop/Knowledge%20Assistant/test_rag.py) to verify the RAG pipeline end-to-end.
    ```powershell
    python test_rag.py
    ```

### Manual Verification
*   Access the FastAPI interactive documentation at `http://127.0.0.1:8000/docs` to test the endpoints directly from the browser.
