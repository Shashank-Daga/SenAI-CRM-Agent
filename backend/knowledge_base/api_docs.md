# API Documentation

## API Versions

### V2 (Current)
- Base URL: `https://api.company.com/v2`
- Authentication: OAuth 2.0 + API Key
- Rate limits: 1,000 requests/minute (Professional), 10,000 requests/minute (Enterprise)
- Response format: JSON
- TLS 1.2+ required

### V1 (Deprecated)
- **Deprecation Date**: 2026-06-01
- **Sunset Date**: 2026-12-31
- **Migration Path**: See v1-to-v2 migration guide
- **Breaking Changes**: Endpoint paths, request/response schemas

## Authentication

### API Key Authentication

```
Authorization: Bearer YOUR_API_KEY
```

- Keys issued via admin dashboard
- Scoped by resource (emails, threads, classifications)
- Rotatable at any time
- Expires after 90 days of inactivity (configurable)

### OAuth 2.0

- Standard OAuth 2.0 with PKCE flow
- Requires client ID and client secret
- Redirect URI must be registered
- Access tokens expire in 1 hour
- Refresh tokens expire in 30 days

## Rate Limits

### Professional Plan
- API Rate Limit: 1,000 requests/minute
- Burst Capacity: 100 requests/second
- Daily Quota: 1.44M requests/day

### Enterprise Plan
- API Rate Limit: 10,000 requests/minute
- Burst Capacity: 1,000 requests/second
- Daily Quota: 14.4M requests/day

### Endpoints

| Endpoint | Method | Rate Limit |
|----------|--------|-----------|
| `/emails` | GET | 100 req/min |
| `/emails` | POST | 50 req/min |
| `/emails/{id}/classify` | POST | 20 req/min |
| `/threads` | GET | 100 req/min |
| `/rag/search` | GET | 200 req/min |

### Rate Limit Headers

```
X-RateLimit-Limit: 1000
X-RateLimit-Remaining: 987
X-RateLimit-Reset: 1621276800
```

## API Endpoints

### Email Ingestion
```
POST /v2/emails
Content-Type: application/json

{
  "message_id": "...",
  "sender": "...",
  "recipient": "...",
  "subject": "...",
  "body": "...",
  "received_at": "2026-05-20T10:00:00Z"
}
```

### Email Retrieval
```
GET /v2/emails?thread_id=...&limit=50&offset=0
```

### Email Classification
```
POST /v2/emails/{id}/classify

Response:
{
  "category": "Complaint",
  "sentiment": "Negative",
  "urgency": "High",
  "confidence": 0.92
}
```

### Thread Management
```
GET /v2/threads?limit=50&offset=0
GET /v2/threads/{id}
```

### RAG Search
```
GET /v2/rag/search?q=pricing&limit=3

Response:
{
  "query": "pricing",
  "results": [...]
}
```

## Error Responses

### 400 Bad Request
```json
{
  "error_code": "validation_error",
  "message": "Invalid request payload",
  "details": {
    "field": "sender",
    "reason": "Invalid email format"
  }
}
```

### 401 Unauthorized
```json
{
  "error_code": "auth_failed",
  "message": "Invalid or expired API key"
}
```

### 429 Too Many Requests
```json
{
  "error_code": "rate_limit_exceeded",
  "message": "Rate limit exceeded. Retry after 60 seconds",
  "retry_after": 60
}
```

### 500 Server Error
```json
{
  "error_code": "internal_error",
  "message": "Unexpected server error",
  "request_id": "req-12345"
}
```

## Webhooks

### Email Classification Webhook
```
POST https://your-domain.com/webhooks/classifications
Content-Type: application/json
X-Webhook-Signature: sha256=...

{
  "event": "email.classified",
  "timestamp": "2026-05-20T10:00:00Z",
  "data": {
    "email_id": "...",
    "classification": {...}
  }
}
```

## Client Libraries

### JavaScript
```
npm install @company/api-client
```

### Python
```
pip install company-api-client
```

### Go
```
go get github.com/company/api-go
```

## Pagination

Default limit: 50
Max limit: 500

```
GET /v2/threads?limit=100&offset=0&sort=-created_at
```

## SDK Examples

### Python SDK
```python
from company_api import Client

client = Client(api_key="sk_live_...")
threads = client.threads.list(limit=10)
classification = client.emails.classify(email_id="...")
```

### JavaScript SDK
```javascript
const client = new CompanyClient({ apiKey: "sk_live_..." });
const threads = await client.threads.list({ limit: 10 });
const classification = await client.emails.classify(emailId);
```
