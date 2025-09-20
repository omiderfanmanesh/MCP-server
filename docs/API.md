# API Documentation

## Overview

The Books MCP Server provides two main tools for interacting with a books database and currency exchange functionality through the Model Context Protocol.

## Tools

### books_query

Query and filter the books database with flexible parameters.

#### Input Schema

```json
{
  "type": "object",
  "properties": {
    "id": {
      "type": "string",
      "description": "Book ID to fetch specific book"
    },
    "genre": {
      "type": "string", 
      "description": "Filter by genre"
    },
    "year": {
      "type": "string",
      "description": "Filter by publication year"
    },
    "author": {
      "type": "string",
      "description": "Filter by author name"
    },
    "title": {
      "type": "string",
      "description": "Filter by title (contains)"
    },
    "limit": {
      "type": "integer",
      "description": "Maximum number of results"
    },
    "offset": {
      "type": "integer", 
      "description": "Offset for pagination"
    }
  },
  "additionalProperties": false
}
```

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