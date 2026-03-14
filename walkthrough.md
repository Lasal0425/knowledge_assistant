# Ingestion Fix Walkthrough

I've resolved the issues preventing the document ingestion from running. Here's what was done:

### 1. Dependency Installation
The error `ModuleNotFoundError: No module named 'dotenv'` occurred because the dependencies in [requirements.txt](file:///c:/Users/ASUS/Desktop/Knowledge%20Assistant/requirements.txt) hadn't been installed in your virtual environment. 
I ran:
```powershell
python -m pip install -r requirements.txt
```

### 2. Module Path Resolution
The subsequent error `ModuleNotFoundError: No module named 'app'` was due to the script not being able to find the `app` package when run from the root. I resolved this by setting the `PYTHONPATH` environment variable.

### 3. Successful Ingestion
I successfully executed the ingestion script:
```powershell
$env:PYTHONPATH="."; python ingestion/ingest_documents.py
```
**Results:**
- ✅ PDF processed: `AIESEC Mail - [IMP] Update on NatCon 2026 CCM Selection.pdf`
- ✅ Total chunks embedded: 5
- ✅ Data stored in `rag_db` (Postgres)

---

## 🚀 Next Steps

Now that your documents are ingested, you can start the API server to query the assistant.

### 1. Start the API Server
Run the following command in your terminal:
```powershell
$env:PYTHONPATH="."; uvicorn app.main:app --reload
```

### 2. Query the Knowledge Base
You can now ask questions about the ingested PDF.
Example:
```powershell
Invoke-RestMethod -Uri "http://127.0.0.1:8000/ask" -Method Post -ContentType "application/json" -Body '{"question": "What is the update on NatCon 2026 CCM Selection?"}'
```
