import asyncio
from typing import Any, Dict, List, Optional
import os
import time
import json
import base64
import hmac
import hashlib

import mcp.types as types
from mcp.server import Server
from mcp.server.stdio import stdio_server

from .books import BooksRepository
from .exchange import default_rates
from .util.xlsx_to_csv import xlsx_first_sheet_to_csv


def _prepare_books_csv() -> str:
    root = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
    csv_out = os.path.join(root, "data", "books.csv")
    xlsx_in = os.path.join(root, "sample-data", "BooksDatasetClean.xlsx")
    os.makedirs(os.path.dirname(csv_out), exist_ok=True)
    if not os.path.exists(csv_out) and os.path.exists(xlsx_in):
        xlsx_first_sheet_to_csv(xlsx_in, csv_out)
    return csv_out


def _prepare_books_csv() -> str:
    root = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
    csv_out = os.path.join(root, "data", "books.csv")
    xlsx_in = os.path.join(root, "sample-data", "BooksDatasetClean.xlsx")
    os.makedirs(os.path.dirname(csv_out), exist_ok=True)
    if not os.path.exists(csv_out) and os.path.exists(xlsx_in):
        xlsx_first_sheet_to_csv(xlsx_in, csv_out)
    return csv_out


def create_jwt_token(user_id: str, username: str) -> str:
    """Create a simple JWT token for demonstration."""
    # Simple JWT implementation for demo
    secret = "demo-secret-key-123"
    
    header = {"typ": "JWT", "alg": "HS256"}
    payload = {
        "user_id": user_id,
        "username": username,
        "exp": time.time() + 3600,  # 1 hour expiry
        "iat": time.time()
    }

    # Encode header and payload
    header_b64 = base64.urlsafe_b64encode(json.dumps(header, separators=(',', ':')).encode()).decode().rstrip('=')
    payload_b64 = base64.urlsafe_b64encode(json.dumps(payload, separators=(',', ':')).encode()).decode().rstrip('=')
    
    # Create signature
    message = f"{header_b64}.{payload_b64}"
    signature = hmac.new(secret.encode(), message.encode(), hashlib.sha256).digest()
    signature_b64 = base64.urlsafe_b64encode(signature).decode().rstrip('=')
    
    return f"{header_b64}.{payload_b64}.{signature_b64}"
    return f"{header_b64}.{payload_b64}.{signature_b64}"


def validate_jwt_token(token: str) -> Optional[Dict[str, Any]]:
    """Validate a JWT token and return the payload if valid."""
    try:
        # Split token into parts
        parts = token.split('.')
        if len(parts) != 3:
            return None
        
        header_b64, payload_b64, signature_b64 = parts
        
        # Verify signature
        secret = "demo-secret-key-123"
        message = f"{header_b64}.{payload_b64}"
        expected_signature = hmac.new(secret.encode(), message.encode(), hashlib.sha256).digest()
        expected_signature_b64 = base64.urlsafe_b64encode(expected_signature).decode().rstrip('=')
        
        if signature_b64 != expected_signature_b64:
            return None
        
        # Decode payload
        # Add padding if needed
        payload_b64 += '=' * (4 - len(payload_b64) % 4)
        payload = json.loads(base64.urlsafe_b64decode(payload_b64.encode()).decode())
        
        # Check expiration
        if payload.get('exp', 0) < time.time():
            return None
        
        return payload
    except Exception:
        return None


# Initialize repositories
_CSV = _prepare_books_csv()
_BOOKS = BooksRepository(_CSV)
_RATES = default_rates()

# Create server instance
server = Server("books-mcp")


@server.list_tools()
async def handle_list_tools() -> List[types.Tool]:
    """List available tools."""
    return [
        types.Tool(
            name="books_query",
            description="List, filter, or fetch books from the dataset",
            inputSchema={
                "type": "object",
                "properties": {
                    "id": {"type": "string", "description": "Book ID to fetch specific book"},
                    "genre": {"type": "string", "description": "Filter by genre"},
                    "year": {"type": "string", "description": "Filter by publication year"},
                    "author": {"type": "string", "description": "Filter by author name"},
                    "title": {"type": "string", "description": "Filter by title (contains)"},
                    "limit": {"type": "integer", "description": "Maximum number of results"},
                    "offset": {"type": "integer", "description": "Offset for pagination"},
                    "token": {"type": "string", "description": "JWT token for authentication"},
                },
                "additionalProperties": False,
            },
        ),
        types.Tool(
            name="exchange_convert",
            description="Convert amount between currencies using synthetic rates",
            inputSchema={
                "type": "object",
                "properties": {
                    "from_currency": {"type": "string", "description": "Source currency code"},
                    "to_currency": {"type": "string", "description": "Target currency code"},
                    "amount": {"type": "number", "description": "Amount to convert"},
                    "token": {"type": "string", "description": "JWT token for authentication"},
                },
                "required": ["from_currency", "to_currency", "amount"],
                "additionalProperties": False,
            },
        ),
        types.Tool(
            name="get_jwt_token",
            description="Get a JWT token for demonstration purposes",
            inputSchema={
                "type": "object",
                "properties": {
                    "username": {"type": "string", "description": "Username for the token"},
                },
                "required": ["username"],
                "additionalProperties": False,
            },
        ),
    ]


@server.call_tool()
async def handle_call_tool(name: str, arguments: Dict[str, Any]) -> List[types.TextContent]:
    """Handle tool calls with authentication."""
    
    # JWT token generation doesn't require authentication
    if name == "get_jwt_token":
        username = arguments.get("username", "demo_user")
        user_id = f"user_{hash(username) % 10000}"
        
        token = create_jwt_token(user_id, username)
        
        result = {
            "token": token,
            "user_id": user_id,
            "username": username,
            "expires_in": 3600,
            "token_type": "Bearer",
            "message": "Token generated successfully! Use this token for authenticated requests."
        }
        return [types.TextContent(type="text", text=str(result))]
    
    # All other tools require authentication
    auth_token = arguments.get("token")
    if not auth_token:
        error_result = {
            "error": "authentication_required",
            "message": "JWT token is required. Generate one using get_jwt_token first.",
            "hint": "Include 'token' parameter with your JWT token"
        }
        return [types.TextContent(type="text", text=str(error_result))]
    
    # Validate the JWT token
    payload = validate_jwt_token(auth_token)
    if not payload:
        error_result = {
            "error": "invalid_token",
            "message": "Invalid or expired JWT token. Generate a new one using get_jwt_token.",
        }
        return [types.TextContent(type="text", text=str(error_result))]
    
    # Token is valid, extract user info
    username = payload.get("username", "unknown")
    user_id = payload.get("user_id", "unknown")
    
    if name == "books_query":
        # Extract arguments
        book_id = arguments.get("id")
        genre = arguments.get("genre")
        year = arguments.get("year")
        author = arguments.get("author")
        title = arguments.get("title")
        limit = arguments.get("limit")
        offset = arguments.get("offset")
        
        # Handle specific book lookup
        if book_id not in (None, ""):
            item = _BOOKS.get_by_id(str(book_id))
            if item is None:
                return [types.TextContent(type="text", text='{"error": "not_found", "message": "Book not found"}')]
            result = {"authenticated_user": username, "data": item}
            return [types.TextContent(type="text", text=str(result))]
        
        # Handle filtered search
        data = _BOOKS.filter(
            genre=genre,
            year=year,
            author=author,
            title_contains=title,
            limit=limit,
            offset=offset,
        )
        result = {"authenticated_user": username, "data": data, "count": len(data)}
        return [types.TextContent(type="text", text=str(result))]
    
    elif name == "exchange_convert":
        # Extract required arguments
        from_currency = arguments["from_currency"]
        to_currency = arguments["to_currency"]
        amount = arguments["amount"]
        
        try:
            value = _RATES.convert(float(amount), from_currency, to_currency)
            result = {
                "authenticated_user": username,
                "from": from_currency.upper(),
                "to": to_currency.upper(),
                "amount": float(amount),
                "converted": value,
            }
            return [types.TextContent(type="text", text=str(result))]
        except Exception as e:
            error_result = {"error": "invalid_request", "message": str(e)}
            return [types.TextContent(type="text", text=str(error_result))]
    
    else:
        raise ValueError(f"Unknown tool: {name}")


async def main() -> None:
    """Run the MCP server with stdio transport."""
    async with stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            server.create_initialization_options()
        )


if __name__ == "__main__":
    asyncio.run(main())

