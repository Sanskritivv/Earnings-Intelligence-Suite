from langchain_community.vectorstores import Chroma
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
import os

def setup_rag(chunks, api_key=None):
    if not api_key:
        api_key = os.environ.get("GOOGLE_API_KEY")

    # Use robust local embeddings to avoid Google API Rate Limits and Tier Restrictions
    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    
    vectorstore = Chroma.from_documents(documents=chunks, embedding=embeddings)
    retriever = vectorstore.as_retriever(search_kwargs={"k": 3})
    
    llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", google_api_key=api_key, temperature=0.3)
    
    prompt = ChatPromptTemplate.from_template(
        "You are an expert financial analyst assistant. "
        "Use the provided context containing earnings call transcript excerpts to answer the user's question. "
        "Always cite exactly where you got the information from the context. "
        "If the answer is not in the context, say 'I cannot find the answer in the transcript'.\n\n"
        "Context: {context}\n\nQuestion: {question}"
    )
    
    def format_docs(docs):
        return "\n\n".join(doc.page_content for doc in docs)

    rag_chain = (
        {"context": retriever | format_docs, "question": RunnablePassthrough()}
        | prompt
        | llm
        | StrOutputParser()
    )
    
    return rag_chain
