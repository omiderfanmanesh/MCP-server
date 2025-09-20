import asyncio
from typing import Any, Dict, List, Optional
import os

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
                },
                "required": ["from_currency", "to_currency", "amount"],
                "additionalProperties": False,
            },
        ),
    ]


@server.call_tool()
async def handle_call_tool(name: str, arguments: Dict[str, Any]) -> List[types.TextContent]:
    """Handle tool calls."""
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
            return [types.TextContent(type="text", text=str(item))]
        
        # Handle filtered search
        data = _BOOKS.filter(
            genre=genre,
            year=year,
            author=author,
            title_contains=title,
            limit=limit,
            offset=offset,
        )
        result = {"data": data, "count": len(data)}
        return [types.TextContent(type="text", text=str(result))]
    
    elif name == "exchange_convert":
        # Extract required arguments
        from_currency = arguments["from_currency"]
        to_currency = arguments["to_currency"]
        amount = arguments["amount"]
        
        try:
            value = _RATES.convert(float(amount), from_currency, to_currency)
            result = {
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

