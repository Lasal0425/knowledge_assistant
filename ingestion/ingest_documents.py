import os
import glob
from dotenv import load_dotenv
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import PGVector
from app.embeddings import get_embeddings

# Load environment variables
load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")


def ingest():
    # Find all PDFs in the data/ folder
    pdf_folder = os.path.join(os.path.dirname(__file__), "..", "data")
    pdf_files = glob.glob(os.path.join(pdf_folder, "*.pdf"))

    if not pdf_files:
        print("No PDF files found in data/ folder.")
        return

    print(f"Found {len(pdf_files)} PDF file(s).")

    # Load and split all PDFs
    all_chunks = []
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
    )

    for pdf_path in pdf_files:
        print(f"Loading: {os.path.basename(pdf_path)}")
        loader = PyPDFLoader(pdf_path)
        pages = loader.load()
        chunks = text_splitter.split_documents(pages)
        print(f"  → Split into {len(chunks)} chunks.")
        all_chunks.extend(chunks)

    print(f"\nTotal chunks to embed: {len(all_chunks)}")

    # Embed and store in PostgreSQL via pgvector
    print("Embedding and storing in PostgreSQL...")
    PGVector.from_documents(
        documents=all_chunks,
        embedding=get_embeddings(),
        connection_string=DATABASE_URL,
        collection_name="documents",
    )

    print("✅ Ingestion complete!")


if __name__ == "__main__":
    ingest()
