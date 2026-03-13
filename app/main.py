from fastapi import FastAPI
from pydantic import BaseModel
from dotenv import load_dotenv

from app.rag_pipeline import get_rag_chain

# Load environment variables
load_dotenv()

# Create FastAPI app
app = FastAPI()

# Global RAG chain
rag_chain = None


# Request model
class QueryRequest(BaseModel):
    question: str


# Response model
class QueryResponse(BaseModel):
    answer: str
    sources: list


# Initialize chain on startup
@app.on_event("startup")
def startup_event():
    global rag_chain
    rag_chain = get_rag_chain()


# Ask endpoint
@app.post("/ask", response_model=QueryResponse)
def ask_question(request: QueryRequest):

    result = rag_chain.invoke(request.question)

    return QueryResponse(
        answer=result,
        sources=[]
    )


# Health check
@app.get("/health")
def health():
    return {"status": "ok"}