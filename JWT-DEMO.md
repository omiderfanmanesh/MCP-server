# Simple JWT Token MCP Server

A basic MCP server that demonstrates JWT token generation along with book and currency tools.

## Features

- **Books Query**: Search and filter books from a dataset
- **Currency Exchange**: Convert between currencies  
- **JWT Token Generator**: Creates JWT tokens for demonstration

## Quick Start

### Local Development

```bash
# Install dependencies
pip install -r requirements.txt

# Run the server
python -m mcp_server.server
```

### Docker

```bash
# Build and run
docker build -t mcp-books-server .
docker-compose up mcp-server
```

## JWT Token Tool

The server includes a `get_jwt_token` tool that demonstrates JWT functionality:

### Usage Example

```json
{
  "name": "get_jwt_token",
  "arguments": {
    "username": "john_doe"
  }
}
```

### Response

```json
{
  "token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
  "user_id": "user_1234",
  "username": "john_doe", 
  "expires_in": 3600,
  "token_type": "Bearer"
}
```

## Available Tools

1. **get_jwt_token** - Generate a JWT token
   - Parameters: `username` (required)
   - Returns: JWT token with user info

2. **books_query** - Search books
   - Parameters: `genre`, `author`, `title`, `year`, `limit`, `offset`
   - Returns: Filtered book results

3. **exchange_convert** - Convert currency
   - Parameters: `from_currency`, `to_currency`, `amount` (all required)
   - Returns: Converted amount

## JWT Implementation

The JWT tokens are created with:
- **Algorithm**: HS256 (HMAC SHA-256)
- **Secret**: "demo-secret-key-123" (hardcoded for demo)
- **Expiry**: 1 hour
- **Claims**: user_id, username, exp, iat

**Note**: This is a demonstration implementation. In production, use a secure secret and proper key management.

## Configuration

The server works out of the box with no configuration needed. It uses:
- Default JWT secret for demo purposes
- Sample book dataset
- Synthetic exchange rates

## MCP Client Integration

Add to your MCP client configuration:

```json
{
  "mcpServers": {
    "jwt-demo-server": {
      "command": "python",
      "args": ["-m", "mcp_server.server"],
      "cwd": "/path/to/MCP-server"
    }
  }
}
```

Or with Docker:

```json
{
  "mcpServers": {
    "jwt-demo-docker": {
      "command": "docker",
      "args": ["run", "--rm", "-i", "mcp-books-server"]
    }
  }
}
```