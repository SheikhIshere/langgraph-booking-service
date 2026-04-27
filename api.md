# API Contract Documentation

## Endpoints

### 1. Send Message
Processes a message through the AI agent.

- **URL**: `/api/chat/{conversation_id}/message`
- **Method**: `POST`
- **Path Parameters**:
  - `conversation_id`: A unique string identifier for the chat session.
- **Request Body**:
```json
{
  "message": "I'm looking for a property in Dhaka for 2 people."
}
```
- **Response Body**:
```json
{
  "response": "I found several properties in Dhaka...",
  "requires_human": false
}
```

### 2. Get Chat History
Retrieves the full message history for a conversation.

- **URL**: `/api/chat/{conversation_id}/history`
- **Method**: `GET`
- **Response Body**:
```json
{
  "conversation_id": "session_123",
  "messages": [
    {
      "role": "user",
      "content": "Hello"
    },
    {
      "role": "assistant",
      "content": "How can I help you today?"
    }
  ]
}
```
