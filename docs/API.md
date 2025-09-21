# MCP Server API Reference

Complete API documentation for the Session-Based Authenticated Model Context Protocol (MCP) Server.

## Table of Contents

1. [API Overview](#api-overview)
2. [Authentication](#authentication)
3. [Session Management](#session-management)
4. [Protected Operations](#protected-operations)
5. [Error Handling](#error-handling)
6. [Response Formats](#response-formats)
7. [Examples](#examples)

---

## API Overview

The MCP Server provides a session-based authentication API with tools for books database operations and currency exchange. All API interactions follow the Model Context Protocol (MCP) specification.

### Base Information

- **Protocol**: Model Context Protocol (MCP) v1.0
- **Transport**: stdio (standard input/output)
- **Authentication**: Session-based with JWT tokens
- **Session Duration**: 1 hour (3600 seconds)
- **Response Format**: JSON wrapped in MCP TextContent

### Tool Categories

| Category | Tools | Authentication Required |
|----------|-------|------------------------|
| Session Management | `authenticate`, `logout`, `session_status` | No |
| Books Operations | `books_query` | Yes |
| Currency Operations | `exchange_convert` | Yes |

---

## Authentication

### Overview

The server uses session-based authentication with JWT tokens. Unlike traditional APIs, authentication tokens are not passed with each request. Instead, the server maintains global session state.

### Workflow

1. Call `authenticate` to create a session
2. Server generates JWT token and stores session globally
3. All subsequent protected operations use the active session
4. Session expires after 1 hour or can be ended with `logout`

---

## Session Management

### authenticate

Create a new user session and authenticate for protected operations.

**Tool Name**: `authenticate`

**Parameters**:
```json
{
  "username": "string"  // Required: Username for authentication
}
```

**Example Request**:
```json
{
  "username": "alice"
}
```

**Success Response**:
```json
{
  "success": true,
  "message": "Successfully authenticated as alice",
  "username": "alice",
  "user_id": "user_1234",
  "session_id": "session_56789",
  "expires_in": 3600
}
```

**Response Fields**:
- `success`: Always `true` for successful authentication
- `message`: Human-readable confirmation message
- `username`: Confirmed username from request
- `user_id`: Generated unique user identifier
- `session_id`: Unique session identifier
- `expires_in`: Session duration in seconds (3600 = 1 hour)

---

### session_status

Check current authentication status and session information.

**Tool Name**: `session_status`

**Parameters**: None

**Example Request**:
```json
{}
```

**Authenticated Response**:
```json
{
  "authenticated": true,
  "username": "alice",
  "user_id": "user_1234",
  "session_age": 120,
  "expires_in": 3480
}
```

**Unauthenticated Response**:
```json
{
  "authenticated": false,
  "message": "No active session. Use 'authenticate' tool to login."
}
```

**Response Fields (Authenticated)**:
- `authenticated`: `true` when session is active
- `username`: Current authenticated username
- `user_id`: Current user identifier
- `session_age`: Seconds since session creation
- `expires_in`: Seconds until session expires

**Response Fields (Unauthenticated)**:
- `authenticated`: `false` when no session
- `message`: Instructions for authentication

---

### logout

End the current authentication session and clean up session data.

**Tool Name**: `logout`

**Parameters**: None

**Example Request**:
```json
{}
```

**Success Response (With Active Session)**:
```json
{
  "success": true,
  "message": "Successfully logged out alice"
}
```

**Success Response (No Active Session)**:
```json
{
  "success": true,
  "message": "No active session to logout"
}
```

**Response Fields**:
- `success`: Always `true` (logout cannot fail)
- `message`: Confirmation of logout action or no-op status

---

## Protected Operations

All protected operations require an active session created via `authenticate`. Each response includes `authenticated_user` for audit trails.

### books_query

Search and retrieve books from the dataset with various filtering options.

**Tool Name**: `books_query`

**Authentication**: Required

**Parameters**:
```json
{
  "id": "string",        // Optional: Specific book ID
  "genre": "string",     // Optional: Filter by genre
  "year": "string",      // Optional: Filter by publication year
  "author": "string",    // Optional: Filter by author name
  "title": "string",     // Optional: Filter by title (contains)
  "limit": "integer",    // Optional: Maximum results (default: 10)
  "offset": "integer"    // Optional: Pagination offset (default: 0)
}
```

#### Specific Book Lookup

**Example Request**:
```json
{
  "id": "book_123"
}
```

**Success Response**:
```json
{
  "authenticated_user": "alice",
  "data": {
    "id": "book_123",
    "Title": "Clean Code",
    "Authors": "Robert Martin",
    "Category": "Programming", 
    "Publisher": "Prentice Hall",
    "Price Starting With ($)": "45.99",
    "Publish Date (Year)": "2008"
  },
  "query_type": "specific_book"
}
```

**Not Found Response**:
```json
{
  "error": "not_found",
  "message": "Book with ID 'book_123' not found",
  "authenticated_user": "alice"
}
```

#### Filtered Search

**Example Request**:
```json
{
  "title": "python",
  "genre": "Programming",
  "limit": 5
}
```

**Success Response**:
```json
{
  "authenticated_user": "alice",
  "data": [
    {
      "id": "book_456",
      "Title": "Python Tricks",
      "Authors": "Dan Bader",
      "Category": "Programming",
      "Publisher": "Real Python",
      "Price Starting With ($)": "29.99",
      "Publish Date (Year)": "2017"
    }
  ],
  "count": 1,
  "query_type": "filtered_search",
  "filters_applied": {
    "genre": "Programming",
    "year": null,
    "author": null,
    "title": "python",
    "limit": 5,
    "offset": null
  }
}
```

**Response Fields**:
- `authenticated_user`: Username of the authenticated user
- `data`: Book object (specific lookup) or array of books (search)
- `count`: Number of results returned (search only)
- `query_type`: `"specific_book"` or `"filtered_search"`
- `filters_applied`: Summary of search criteria used (search only)

#### Book Data Structure

Each book object contains:
```json
{
  "id": "string",                           // Generated unique identifier
  "Title": "string",                        // Book title
  "Authors": "string",                      // Author name(s)
  "Category": "string",                     // Genre/category
  "Publisher": "string",                    // Publishing company
  "Price Starting With ($)": "string",      // Price in USD
  "Publish Date (Year)": "string"          // Publication year
}
```

---

### exchange_convert

Convert monetary amounts between different currencies using current exchange rates.

**Tool Name**: `exchange_convert`

**Authentication**: Required

**Parameters**:
```json
{
  "from_currency": "string",  // Required: Source currency code
  "to_currency": "string",    // Required: Target currency code  
  "amount": "number"          // Required: Amount to convert
}
```

**Example Request**:
```json
{
  "from_currency": "USD",
  "to_currency": "EUR",
  "amount": 100
}
```

**Success Response**:
```json
{
  "authenticated_user": "alice",
  "from": "USD",
  "to": "EUR", 
  "amount": 100.0,
  "converted": 85.23,
  "operation": "currency_conversion",
  "timestamp": 1640995200.0
}
```

**Error Response**:
```json
{
  "error": "conversion_failed",
  "message": "Currency 'XYZ' not supported",
  "authenticated_user": "alice",
  "attempted_conversion": "100 USD -> XYZ"
}
```

**Response Fields (Success)**:
- `authenticated_user`: Username of the authenticated user
- `from`: Source currency code (normalized to uppercase)
- `to`: Target currency code (normalized to uppercase)
- `amount`: Original amount as number
- `converted`: Converted amount as number
- `operation`: Always `"currency_conversion"`
- `timestamp`: Unix timestamp of conversion

**Response Fields (Error)**:
- `error`: Error type (`"conversion_failed"`)
- `message`: Detailed error description
- `authenticated_user`: Username of the authenticated user
- `attempted_conversion`: Summary of failed conversion attempt

#### Supported Currencies

The system supports major world currencies including:
- USD (US Dollar)
- EUR (Euro)
- GBP (British Pound)
- JPY (Japanese Yen)
- CAD (Canadian Dollar)
- AUD (Australian Dollar)
- CHF (Swiss Franc)
- And others via synthetic exchange rates

---

## Error Handling

### Authentication Errors

#### authentication_required

Returned when accessing protected operations without an active session.

```json
{
  "error": "authentication_required",
  "message": "No active session. Please authenticate first using the 'authenticate' tool.",
  "hint": "Call authenticate tool with your username to create a session"
}
```

#### session_expired

Returned when session has exceeded 1-hour time limit.

```json
{
  "error": "session_expired",
  "message": "Session has expired. Please authenticate again.",
  "hint": "Sessions expire after 1 hour. Please call authenticate tool again."
}
```

### Operation Errors

#### not_found

Returned when requested resource doesn't exist.

```json
{
  "error": "not_found",
  "message": "Book with ID 'invalid_id' not found",
  "authenticated_user": "alice"
}
```

#### conversion_failed

Returned when currency conversion encounters an error.

```json
{
  "error": "conversion_failed",
  "message": "Currency 'INVALID' not supported",
  "authenticated_user": "alice",
  "attempted_conversion": "100 USD -> INVALID"
}
```

#### invalid_request

Returned when request parameters are malformed.

```json
{
  "error": "invalid_request",
  "message": "Missing required parameter: from_currency"
}
```

### System Errors

#### Unknown Tool

When an unrecognized tool is called:

```
ValueError: Unknown tool: invalid_tool_name
```

---

## Response Formats

### MCP Protocol Wrapper

All responses are wrapped in MCP TextContent format:

```json
[
  {
    "type": "text",
    "text": "{\"authenticated_user\": \"alice\", \"data\": [...]}"
  }
]
```

### Common Response Elements

#### Success Responses
- Always include operation results
- Include `authenticated_user` for protected operations
- Include relevant metadata (counts, timestamps, etc.)

#### Error Responses
- Include `error` field with error type
- Include `message` field with human-readable description
- May include `hint` field with resolution guidance
- Include `authenticated_user` when available

#### Timestamps
- Unix timestamps as floating-point numbers
- Represent seconds since Unix epoch (January 1, 1970)

---

## Examples

### Complete Authentication Flow

```json
// 1. Check initial status
{"tool": "session_status", "arguments": {}}
// Response: {"authenticated": false, "message": "No active session..."}

// 2. Attempt protected operation (should fail)
{"tool": "books_query", "arguments": {"limit": 1}}
// Response: {"error": "authentication_required", "message": "No active session..."}

// 3. Authenticate
{"tool": "authenticate", "arguments": {"username": "alice"}}
// Response: {"success": true, "username": "alice", "session_id": "...", "expires_in": 3600}

// 4. Check status after authentication
{"tool": "session_status", "arguments": {}}
// Response: {"authenticated": true, "username": "alice", "session_age": 5, "expires_in": 3595}

// 5. Use protected operations
{"tool": "books_query", "arguments": {"title": "python", "limit": 3}}
// Response: {"authenticated_user": "alice", "data": [...], "count": 3}

{"tool": "exchange_convert", "arguments": {"from_currency": "USD", "to_currency": "EUR", "amount": 100}}
// Response: {"authenticated_user": "alice", "from": "USD", "to": "EUR", "amount": 100.0, "converted": 85.23}

// 6. Logout
{"tool": "logout", "arguments": {}}
// Response: {"success": true, "message": "Successfully logged out alice"}
```

### Books Search Examples

```json
// Search by title
{"tool": "books_query", "arguments": {"title": "clean code"}}

// Search by author
{"tool": "books_query", "arguments": {"author": "Robert Martin"}}

// Search by year
{"tool": "books_query", "arguments": {"year": "2008"}}

// Search by genre
{"tool": "books_query", "arguments": {"genre": "Programming"}}

// Complex search with pagination
{"tool": "books_query", "arguments": {"genre": "Fiction", "limit": 10, "offset": 20}}

// Get specific book
{"tool": "books_query", "arguments": {"id": "book_123"}}
```

### Currency Exchange Examples

```json
// Basic conversion
{"tool": "exchange_convert", "arguments": {"from_currency": "USD", "to_currency": "EUR", "amount": 100}}

// Convert with decimals
{"tool": "exchange_convert", "arguments": {"from_currency": "GBP", "to_currency": "JPY", "amount": 50.75}}

// Same currency (should return same amount)
{"tool": "exchange_convert", "arguments": {"from_currency": "USD", "to_currency": "USD", "amount": 100}}
```

### Error Scenarios

```json
// Authentication required
{"tool": "books_query", "arguments": {"title": "python"}}
// Response: {"error": "authentication_required", "message": "No active session..."}

// Book not found
{"tool": "books_query", "arguments": {"id": "nonexistent"}}
// Response: {"error": "not_found", "message": "Book with ID 'nonexistent' not found"}

// Invalid currency
{"tool": "exchange_convert", "arguments": {"from_currency": "INVALID", "to_currency": "USD", "amount": 100}}
// Response: {"error": "conversion_failed", "message": "Currency 'INVALID' not supported"}

// Missing required parameter
{"tool": "exchange_convert", "arguments": {"from_currency": "USD", "amount": 100}}
// Response: KeyError or similar indicating missing to_currency
```

---

## Integration Notes

### AI Assistant Usage

When integrating with AI assistants:

1. **Authentication First**: Always call `authenticate` before using protected operations
2. **Session Persistence**: Session state persists across multiple tool calls
3. **Error Handling**: Check for authentication errors and re-authenticate if needed
4. **Session Management**: Use `session_status` to monitor session health

### Production Considerations

- Replace demo JWT secret with secure environment variable
- Implement proper session storage (Redis, database)
- Add rate limiting and request validation
- Enable HTTPS transport for security
- Implement comprehensive logging and monitoring
- Add proper error tracking and alerting

### Development Tips

- Use `session_status` to debug authentication issues
- Check session expiration times to avoid mid-operation failures
- Test both authenticated and unauthenticated scenarios
- Validate all required parameters before making requests
- Handle network errors and timeouts appropriately

#### Response Format

**Single Book (when ID provided):**
```json
{
  "id": "123",
  "title": "The Great Gatsby",
  "author": "F. Scott Fitzgerald",
  "genre": "Classic Literature",
  "year": "1925",
  "isbn": "978-0-7432-7356-5"
}
```

**Multiple Books:**
```json
{
  "data": [
    {
      "id": "123",
      "title": "The Great Gatsby",
      "author": "F. Scott Fitzgerald",
      "genre": "Classic Literature", 
      "year": "1925"
    }
  ],
  "count": 1
}
```

**Error Response:**
```json
{
  "error": "not_found",
  "message": "Book not found"
}
```

#### Usage Examples

**Find a specific book:**
```json
{
  "id": "123"
}
```

**Search by genre:**
```json
{
  "genre": "Science Fiction",
  "limit": 10
}
```

**Filter by author and year:**
```json
{
  "author": "Isaac Asimov",
  "year": "1951",
  "limit": 5
}
```

**Search with pagination:**
```json
{
  "genre": "Fantasy",
  "limit": 20,
  "offset": 40
}
```

### exchange_convert

Convert amounts between different currencies using synthetic exchange rates.

#### Input Schema

```json
{
  "type": "object",
  "properties": {
    "from_currency": {
      "type": "string",
      "description": "Source currency code"
    },
    "to_currency": {
      "type": "string", 
      "description": "Target currency code"
    },
    "amount": {
      "type": "number",
      "description": "Amount to convert"
    }
  },
  "required": ["from_currency", "to_currency", "amount"],
  "additionalProperties": false
}
```

#### Supported Currencies

- **USD**: US Dollar
- **EUR**: Euro
- **GBP**: British Pound
- **JPY**: Japanese Yen
- **CAD**: Canadian Dollar
- **AUD**: Australian Dollar
- **CHF**: Swiss Franc
- **CNY**: Chinese Yuan

#### Response Format

**Successful conversion:**
```json
{
  "from": "USD",
  "to": "EUR", 
  "amount": 100.0,
  "converted": 85.23
}
```

**Error Response:**
```json
{
  "error": "invalid_request",
  "message": "Unsupported currency code: XYZ"
}
```

#### Usage Examples

**Basic conversion:**
```json
{
  "from_currency": "USD",
  "to_currency": "EUR",
  "amount": 100
}
```

**Large amount conversion:**
```json
{
  "from_currency": "GBP", 
  "to_currency": "JPY",
  "amount": 1500.50
}
```

## Error Handling

All tools return structured error responses when issues occur:

- `invalid_request`: Invalid parameters or unsupported values
- `not_found`: Requested resource doesn't exist
- `server_error`: Internal server errors

Error responses follow this format:
```json
{
  "error": "error_type",
  "message": "Human-readable error description"
}
```

## Rate Limiting

Currently, no rate limiting is implemented. The server processes requests as quickly as possible.

## Data Freshness

- **Books Data**: Static dataset, updated manually
- **Exchange Rates**: Synthetic rates, not real-time market data