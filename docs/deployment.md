# Deployment Guide

## Docker Deployment

### Prerequisites
- Docker and Docker Compose installed
- Google API key for Gemini
- Sufficient disk space for vector store

### Steps

1. **Environment Setup**:
   ```bash
   cp .env.example .env
   # Edit .env and add your GOOGLE_API_KEY
   ```

2. **Build and Start**:
   ```bash
   docker-compose up --build
   ```

3. **Initialize Data**:
   ```bash
   # In a new terminal
   docker-compose exec rag-api python scripts/scrape.py
   docker-compose exec rag-api python scripts/build_index.py
   ```

4. **Verify Deployment**:
   - Access API docs: http://localhost:8000/docs
   - Test health endpoint: http://localhost:8000/

## Monitoring and Maintenance

### Logs
```bash
docker-compose logs -f rag-api
```

### Updating Data
1. Add new URLs to `scripts/scrape.py`
2. Re-run scraping and indexing scripts
3. No service restart required

### Troubleshooting
- Check logs for errors
- Verify volume mounts
- Ensure API key is properly set
