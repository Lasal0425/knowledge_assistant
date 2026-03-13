import os
from dotenv import load_dotenv
from app.rag_pipeline import get_rag_chain
from app.retriever import get_retriever

load_dotenv()

def test_rag():
    print("--- DEBUG START ---")
    
    print("1. Initializing Retriever...")
    retriever = get_retriever()
    print("   Retriever initialized.")
    
    question = "What is the update on NatCon 2026 CCM Selection?"
    print(f"2. Querying Retriever for: {question}")
    try:
        docs = retriever.invoke(question)
        print(f"   Found {len(docs)} relevant document(s).")
        for i, doc in enumerate(docs):
            print(f"   [Doc {i}] Source: {doc.metadata.get('source', 'Unknown')}")
            print(f"   [Doc {i}] Content snippet: {doc.page_content[:100].replace('\n', ' ')}...")
    except Exception as e:
        print(f"   Error during retrieval: {e}")
        return

    print("3. Building RAG chain...")
    chain = get_rag_chain()
    print("   RAG chain built.")
    
    print("4. Invoking LLM via Chain...")
    try:
        response = chain.invoke(question)
        print("\n--- LLM RESPONSE ---")
        print(response)
        print("--------------------")
    except Exception as e:
        print(f"Error during RAG invoke: {e}")

if __name__ == "__main__":
    test_rag()
