# Namami Gange RAG System

A Retrieval-Augmented Generation (RAG) system for answering questions about the Namami Gange Programme using FastAPI, FAISS, and Google Gemini.

## Overview

This project implements a question-answering system specifically focused on the Namami Gange Programme. It uses RAG architecture to provide accurate, contextual answers by combining information retrieval with large language model capabilities.

## High-Level System Architecture

The architecture is divided into two distinct phases:

### A. Offline Indexing Pipeline
- **Scrape**: Python script fetches raw HTML content from predefined URLs (e.g., nmcg.nic.in, news articles)
- **Extract & Clean**: Parses HTML to extract meaningful text, removing navigation bars, ads, and footers
- **Load & Chunk**: Breaks documents into smaller, semantically coherent chunks
- **Embed & Store**: Converts text chunks into embeddings using sentence-transformers, stored in FAISS vector index

### B. Online Querying Pipeline
- **API Request**: User sends query to FastAPI /query endpoint
- **Load Index**: FastAPI loads pre-built FAISS index on startup
- **Embed Query**: Converts user query into embedding
- **Retrieve**: Performs similarity search for relevant document chunks
- **Augment & Generate**: Combines query and context into prompt for Google Gemini
- **Synthesize & Respond**: Returns generated answer as JSON response

## Project Directory Structure

```
rag_namami_gange/
├── scripts/
│   ├── scrape.py           # Script to scrape web data
│   └── build_index.py      # Script to create the FAISS vector index
├── data/
│   └── raw_text/           # Scraped text files will be saved here
├── vector_store/
│   └── faiss_index/        # The saved FAISS index will be stored here
├── main.py                 # The FastAPI application
├── .env                    # To store API keys and other secrets
├── requirements.txt        # Project dependencies
└── .gitignore             # To exclude unnecessary files from version control
```

## Example Queries and Expected Responses

### Query 1 (In-Scope)
**User Question**: "What are the main pillars of the Namami Gange Programme?"  
**Expected Response**: "Based on the provided information, the main pillars of the Namami Gange Programme include Sewerage Treatment Infrastructure, River-Front Development, River-Surface Cleaning, Biodiversity Conservation, Afforestation, Public Awareness, Industrial Effluent Monitoring, and Ganga Gram."

### Query 2 (Out-of-Scope)
**User Question**: "What is the weather like in Paris today?"  
**Expected Response**: "This assistant is specialized in the Namami Gange program. Please ask a relevant question."

### Query 3 (Not in Knowledge Base)
**User Question**: "Who was the project manager for the Varanasi ghat development in 2016 under Namami Gange?"  
**Expected Response**: "Based on the provided information, I cannot answer this question."

## How to Run the System

1. **Set up environment**:
   ```bash
   # Create and configure .env file
   # Install dependencies
   pip install -r requirements.txt
   ```

2. **Scrape Data**:
   ```bash
   cd rag_namami_gange/scripts
   python scrape.py
   ```

3. **Build the Index**:
   ```bash
   # Still in the scripts directory
   python build_index.py
   ```

4. **Run the API Server**:
   ```bash
   cd ..
   uvicorn main:app --reload
   ```

The API will be available at http://127.0.0.1:8000, with interactive documentation at http://127.0.0.1:8000/docs.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.
