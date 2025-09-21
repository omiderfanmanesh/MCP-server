# 🔐 JWT Authentication API Documentation

## Overview

This MCP server implements a JWT-based authentication system where:
- **Token generation** is open to all users
- **Protected operations** require valid JWT tokens
- **All responses** include authentication context

## Authentication Flow

### 1. Generate JWT Token

**Tool:** `get_jwt_token`
**Authentication:** ❌ **Not Required**

```json
{
  "tool": "get_jwt_token",
  "arguments": {
    "username": "alice"
  }
}
```

**Response:**
```json
{
  "token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjoidXNlcl8xMjM0IiwidXNlcm5hbWUiOiJhbGljZSIsImV4cCI6MTcyNjg1NjQwMCwiaWF0IjoxNzI2ODUyODAwfQ.signature",
  "user_id": "user_1234",
  "username": "alice",
  "expires_in": 3600,
  "token_type": "Bearer",
  "message": "Token generated successfully! Use this token for authenticated requests."
}
```

### 2. Use Token for Protected Operations

Include the `token` parameter in all protected operations:

```json
{
  "tool": "books_query",
  "arguments": {
    "token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
    "title": "programming"
  }
}
```

## Error Responses

### Missing Token
```json
{
  "error": "authentication_required",
  "message": "JWT token is required. Generate one using get_jwt_token first.",
  "hint": "Include 'token' parameter with your JWT token"
}
```

### Invalid/Expired Token
```json
{
  "error": "invalid_token",
  "message": "Invalid or expired JWT token. Generate a new one using get_jwt_token."
}
```

## JWT Token Structure

### Header
```json
{
  "typ": "JWT",
  "alg": "HS256"
}
```

### Payload
```json
{
  "user_id": "user_1234",
  "username": "alice", 
  "exp": 1726856400,
  "iat": 1726852800
}
```

### Signature
- **Algorithm**: HMAC SHA256
- **Secret**: `demo-secret-key-123` (demo only)
- **Format**: `base64url(header).base64url(payload).base64url(signature)`

## Token Validation Process

1. **Split token** into header, payload, signature
2. **Verify signature** using HMAC SHA256
3. **Check expiration** time (`exp` claim)
4. **Extract user info** from payload
5. **Return payload** if valid, `null` if invalid

## Security Considerations

### For Development
- ✅ Use the default secret for testing
- ✅ Generate multiple tokens for different users
- ✅ Test expired token scenarios

### For Production
- ⚠️ **Replace the demo secret** with a strong random key
- ⚠️ **Store secrets in environment variables**
- ⚠️ **Use HTTPS** for token transmission
- ⚠️ **Implement proper token storage** on client side
- ⚠️ **Add token refresh mechanism**
- ⚠️ **Implement user management system**

## Example Workflows

### Complete Authentication Flow
```bash
# 1. Generate token
curl -X POST /mcp/call_tool \
  -d '{"tool": "get_jwt_token", "arguments": {"username": "alice"}}'

# 2. Use token for protected operation
curl -X POST /mcp/call_tool \
  -d '{"tool": "books_query", "arguments": {"token": "...", "author": "shakespeare"}}'
```

### Cursor Integration Example
```
User: "Generate a JWT token for user 'bob'"
Assistant: [Calls get_jwt_token with username: "bob"]

User: "Search for fiction books with token: eyJ0eXAiOiJKV1Q..."
Assistant: [Calls books_query with token and genre: "fiction"]
```

### Error Handling Example
```
User: "Search for python books"
Assistant: [Calls books_query without token]
Response: "authentication_required" error

User: "Generate a token for 'dev'"
Assistant: [Calls get_jwt_token]

User: "Now search for python books with token: [token]"
Assistant: [Calls books_query with valid token - succeeds]
```

## Testing Authentication

### Manual Testing Script
```python
from mcp_server.server import create_jwt_token, validate_jwt_token

# Test 1: Create and validate token
token = create_jwt_token("user123", "testuser")
payload = validate_jwt_token(token)
print(f"Token valid: {payload is not None}")

# Test 2: Test invalid token
invalid = validate_jwt_token("invalid.token.here")
print(f"Invalid token: {invalid is None}")

# Test 3: Test token structure
parts = token.split('.')
print(f"Token parts: {len(parts)} (should be 3)")
```

### Integration Testing Checklist
- [ ] Generate token without authentication
- [ ] Use valid token for books_query
- [ ] Use valid token for exchange_convert  
- [ ] Try books_query without token (should fail)
- [ ] Try exchange_convert without token (should fail)
- [ ] Test with malformed token (should fail)
- [ ] Test with expired token (should fail)

## Rate Limiting & Security

Currently the server has no rate limiting. For production consider:

- **Token generation limits** (e.g., 10 tokens per IP per hour)
- **Request rate limiting** (e.g., 100 requests per token per minute)
- **Token blacklisting** for compromised tokens
- **User session management**
- **Audit logging** for security events

## Environment Configuration

```bash
# Optional environment variables
export JWT_SECRET="your-super-secret-key-here"
export JWT_EXPIRY="3600"  # 1 hour in seconds
export TOKEN_ISSUER="your-app-name"
export TOKEN_AUDIENCE="api-users"
```

## Troubleshooting

### Common Issues

**"Invalid token" errors:**
- Check token format (should have 3 parts separated by dots)
- Verify token hasn't expired
- Ensure you're using the complete token string

**"Authentication required" errors:**
- Make sure to include `"token"` parameter
- Check parameter name spelling
- Verify you're calling the right tool

**Token generation fails:**
- Check server logs for errors
- Verify username parameter is provided
- Ensure server has proper dependencies installed