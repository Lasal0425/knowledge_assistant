from fastapi import FastAPI
from dotenv import load_dotenv
import os
from pydantic import BaseModel
from app.rag_pipeline import get_rag_chain