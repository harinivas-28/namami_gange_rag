# main.py
import os
from dotenv import load_dotenv

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List

from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import ChatPromptTemplate
from langchain.schema.runnable import RunnablePassthrough
from langchain.schema.output_parser import StrOutputParser

# --- 1. Load Configuration and Initialize Models ---
load_dotenv()

# Check for API Key
if not os.getenv("GOOGLE_API_KEY"):
    raise ValueError("GOOGLE_API_KEY not found in .env file")

# Configuration
VECTOR_STORE_PATH = "vector_store/faiss_index"
EMBEDDING_MODEL = "all-MiniLM-L6-v2"
LLM_MODEL = "gemini-1.5-flash" # Fast, efficient, and with a large context window

# --- 2. Define API Models ---
class QueryRequest(BaseModel):
    question: str

class QueryResponse(BaseModel):
    answer: str
    # In the future, you could add sources here:
    # sources: List[str]

# --- 3. Initialize FastAPI App ---
app = FastAPI(
    title="Namami Gange RAG API",
    description="An API to answer questions about the Namami Gange program based on a local knowledge base."
)

# --- 4. Load RAG Components (on startup) ---
try:
    embeddings = HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL)
    vector_store = FAISS.load_local(VECTOR_STORE_PATH, embeddings, allow_dangerous_deserialization=True)
    retriever = vector_store.as_retriever(search_kwargs={"k": 4}) # Retrieve top 4 relevant chunks
    llm = ChatGoogleGenerativeAI(model=LLM_MODEL, temperature=0.3)
except Exception as e:
    print(f"Error loading RAG components: {e}")
    # In a production scenario, you might want the app to fail startup if components don't load.
    retriever = None 
    llm = None

# --- 5. Define the RAG Chain and Prompt ---
PROMPT_TEMPLATE = """
You are a specialized assistant for the Namami Gange program.
Your task is to answer the user's question strictly based on the provided context.
Do not use any external knowledge or make up information.
If the context does not contain the answer, you must state: "Based on the provided information, I cannot answer this question."

CONTEXT:
{context}

QUESTION:
{question}

ANSWER:
"""

prompt = ChatPromptTemplate.from_template(PROMPT_TEMPLATE)

# Helper to format retrieved documents
def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)

# The RAG chain using LangChain Expression Language (LCEL)
rag_chain = (
    {"context": retriever | format_docs, "question": RunnablePassthrough()}
    | prompt
    | llm
    | StrOutputParser()
)

# --- 6. Define API Endpoints ---
@app.get("/", summary="Health Check")
def read_root():
    """Root endpoint to check if the API is running."""
    return {"status": "ok", "message": "Namami Gange RAG API is running."}


@app.post("/query", response_model=QueryResponse, summary="Query the RAG system")
async def query_rag(request: QueryRequest):
    """
    Receives a question, retrieves relevant context, and generates an answer.
    """
    if not retriever or not llm:
         raise HTTPException(status_code=503, detail="RAG components are not available. Please check server logs.")

    question = request.question
    
    # Simple check for out-of-scope questions
    if "namami gange" not in question.lower() and "ganga" not in question.lower():
         return QueryResponse(answer="This assistant is specialized in the Namami Gange program. Please ask a relevant question.")
    
    print(f"Received query: {question}")
    
    # Invoke the RAG chain
    answer = rag_chain.invoke(question)
    
    return QueryResponse(answer=answer)

# To run this app: uvicorn main:app --reload