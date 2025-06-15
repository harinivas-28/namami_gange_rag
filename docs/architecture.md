# System Architecture

## Overview
The Namami Gange RAG System is built using a modern stack of technologies to provide accurate information about the Namami Gange Programme through an API interface.

## Components

### 1. Data Collection Layer
- **Web Scraping**: Python scripts using BeautifulSoup4 for data extraction
- **Data Storage**: Raw text files stored in `data/raw_text` directory
- **Data Sources**: Official government websites, news articles, and verified sources

### 2. Vector Database Layer
- **Embeddings**: Sentence transformers (all-MiniLM-L6-v2)
- **Vector Store**: FAISS for efficient similarity search
- **Storage**: Persistent storage in `vector_store/faiss_index`

### 3. API Layer
- **Framework**: FastAPI
- **LLM Integration**: Google Gemini (gemini-1.5-flash)
- **Response Generation**: RAG-based answer synthesis

## Data Flow
1. **Indexing Pipeline**:
   ```
   Web Sources → Scraping → Text Cleaning → Chunking → Embedding → FAISS Index
   ```

2. **Query Pipeline**:
   ```
   User Query → Query Embedding → Similarity Search → Context Retrieval → LLM Processing → Response
   ```

## Deployment Architecture
- Containerized using Docker
- Stateless API design
- Volume-mounted storage for persistence
- Environment-based configuration
