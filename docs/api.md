# API Documentation

## Endpoints

### 1. Health Check
```
GET /
```
Returns API status

**Response**:
```json
{
    "status": "ok",
    "message": "Namami Gange RAG API is running."
}
```

### 2. Query Endpoint
```
POST /query
```
Send questions about Namami Gange

**Request Body**:
```json
{
    "question": "What are the main pillars of Namami Gange?"
}
```

**Response**:
```json
{
    "answer": "Based on the provided information..."
}
```

## Error Handling

- 400: Bad Request
- 503: Service Unavailable (RAG components not loaded)

## Usage Limits
- Recommended: 10 requests/minute
- Response time: 2-5 seconds typical

## Example Usage

```python
import requests

response = requests.post(
    "http://localhost:8000/query",
    json={"question": "What is Namami Gange?"}
)
print(response.json())
```
