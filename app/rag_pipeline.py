from langchain_ollama import ChatOllama
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough

from app.retriever import get_retriever
from app.prompts import get_prompt
from app.embeddings import get_embeddings


def get_rag_chain():

    # Load retriever
    retriever = get_retriever()

    # Load prompt template
    prompt = get_prompt()

    # Initialize local LLM (Ollama)
    llm = ChatOllama(model="llama3")

    # Build LCEL chain
    rag_chain = (
        {"context": retriever, "question": RunnablePassthrough()}
        | prompt
        | llm
        | StrOutputParser()
    )

    return rag_chain