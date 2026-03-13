import os
from langchain_community.vectorstores import PGVector
from app.embeddings import get_embeddings

def get_retriever():
    
    vectorstore = PGVector.from_existing_index(
        embedding=get_embeddings(),
        connection_string=os.getenv("DATABASE_URL"),
        collection_name="documents",
    )

    return vectorstore.as_retriever(search_kwargs={"k": 4})