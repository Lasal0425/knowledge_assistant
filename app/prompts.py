from langchain_core.prompts import ChatPromptTemplate

def get_prompt():

    prompt: ChatPromptTemplate = ChatPromptTemplate.from_messages([
        ("system", "You are a helpful assistant. Answer the question using ONLY the provided context. "
                "If the context does not contain the answer, say you don't know."),
                
        ("human", "Context:\n{context}\n\nQuestion:\n{question}"),
    ])

    return prompt