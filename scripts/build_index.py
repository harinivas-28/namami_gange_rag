# scripts/build_index.py
import os
from langchain_community.document_loaders import DirectoryLoader, TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS

# --- Configuration ---
DATA_PATH = "./data/raw_text"
VECTOR_STORE_PATH = "./vector_store/faiss_index"
EMBEDDING_MODEL = "all-MiniLM-L6-v2" # A good, fast starting model

def build_vector_store():
    """Loads data, splits it, creates embeddings, and saves to a FAISS index."""
    print("Loading documents...")
    # Use TextLoader to ensure one document per file
    loader = DirectoryLoader(DATA_PATH, glob="*.txt", loader_cls=TextLoader, loader_kwargs={'encoding': 'utf-8'})
    documents = loader.load()

    if not documents:
        print("No documents found. Did you run the scrape.py script first?")
        return

    print(f"Loaded {len(documents)} documents.")

    print("Splitting documents into chunks...")
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000, # Max size of a chunk
        chunk_overlap=150  # Overlap between chunks to maintain context
    )
    docs = text_splitter.split_documents(documents)
    print(f"Split into {len(docs)} chunks.")

    print(f"Initializing embedding model: {EMBEDDING_MODEL}...")
    # Initialize sentence-transformers model for embeddings
    embeddings = HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL)

    print("Creating FAISS vector store...")
    db = FAISS.from_documents(docs, embeddings)

    print(f"Saving FAISS index to {VECTOR_STORE_PATH}...")
    if not os.path.exists("./vector_store"):
        os.makedirs("./vector_store")
    db.save_local(VECTOR_STORE_PATH)
    
    print("Vector store created and saved successfully.")

if __name__ == "__main__":
    build_vector_store()