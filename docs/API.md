# DRDR API Documentation

## Base URL
`https://your-service.a.run.app`

## Endpoints

### POST /upload
Upload a file for deduplication

**Headers:**
- `X-User-ID: merohan@02` (Optional)

**Body:**
- `file`: Multipart file upload

**Response:**
```json
{
  "message": "File processed successfully",
  "chunks": 42,
  "file_id": "filename.txt"
}
