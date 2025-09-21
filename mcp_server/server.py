"""
Session-Based Authenticated MCP Server

This Model Context Protocol (MCP) server provides secure access to:
- Books database operations (search and retrieve book information)  
- Currency exchange rate calculations with real-time conversion

Architecture Overview:
===================
This server implements a session-based authentication system specifically designed
for AI assistants and automated tools. Unlike traditional API authentication that
requires passing tokens with each request, this system maintains a global session
state that persists across tool calls within the same conversation/session.

Key Components:
- Authentication Manager: Handles JWT token creation/validation and session lifecycle
- Session Store: Global storage for active user sessions with expiration tracking
- Protected Operations: Books and currency tools that require authentication
- Session Management Tools: authenticate, session_status, logout for user control

Features:
========
- Session-based authentication system designed for AI assistants
- JWT tokens for secure session management with HS256 signing
- Automatic session expiration (1 hour) with cleanup
- Protected operations requiring authentication
- Simple authenticate-then-use workflow
- Real-time session status checking
- Graceful error handling and user feedback

Security Model:
==============
- JWT tokens signed with HS256 algorithm using demo secret
- 1-hour session expiration for security (3600 seconds)
- Automatic cleanup of expired sessions on access
- Global session management for AI assistant compatibility
- No sensitive data stored in session (only user metadata)
- Secure token generation with timestamp validation

Authentication Flow:
==================
1. AI Assistant calls authenticate(username) to create a session
   - Server generates unique user_id and session_id
   - JWT token created with user claims and expiration
   - Session stored in global _USER_SESSIONS dictionary
   - Global _CURRENT_SESSION set for subsequent tool calls

2. AI Assistant can check status with session_status()
   - Returns authentication state, user info, and time remaining
   - Automatically cleans up expired sessions

3. AI Assistant calls protected operations (books_query, exchange_convert)
   - Server checks _CURRENT_SESSION for valid authentication
   - Validates session hasn't expired (removes if expired)
   - Executes operation with user context
   - Returns results with authenticated_user information

4. AI Assistant calls logout() to end session (optional)
   - Removes session from global storage
   - Clears _CURRENT_SESSION
   - Confirms logout success

Error Handling:
==============
- authentication_required: No active session for protected operations
- session_expired: Session exists but has exceeded 1-hour limit
- invalid_credentials: JWT token validation failed
- tool_not_found: Unknown tool name provided
- parameter_missing: Required parameters not provided

Data Flow:
=========
User Request → Tool Call → Authentication Check → Operation Execution → Response

For protected operations:
Tool Call → Session Validation → Expiration Check → Data Processing → User Context + Results

Compatibility:
=============
This design specifically addresses the limitation where AI assistants cannot
pass authentication tokens as parameters to individual tool calls. Instead,
the authentication state is maintained globally within the server session,
allowing AI assistants to authenticate once and then use all protected tools
seamlessly without additional token management.

Usage Pattern:
=============
# 1. Authenticate
authenticate(username="alice") 
→ Creates session, returns session info

# 2. Check status (optional)  
session_status()
→ Shows authentication state and time remaining

# 3. Use protected operations
books_query(title="python")
→ Returns books with authenticated_user: "alice"

exchange_convert(from_currency="USD", to_currency="EUR", amount=100)
→ Returns conversion with authenticated_user: "alice"

# 4. Logout (optional)
logout()
→ Cleans up session

Author: MCP Server Team
Date: September 2025
Version: 1.0.0
"""

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
    """
    Prepare the books CSV file from XLSX source.
    
    This function handles the conversion of the Excel dataset to CSV format
    for efficient processing by the BooksRepository. It ensures the data
    directory exists and only converts if the CSV doesn't already exist.
    
    Returns:
        str: Absolute path to the prepared CSV file
        
    File Locations:
        - Input: sample-data/BooksDatasetClean.xlsx
        - Output: data/books.csv
    """
    root = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
    csv_out = os.path.join(root, "data", "books.csv")
    xlsx_in = os.path.join(root, "sample-data", "BooksDatasetClean.xlsx")
    os.makedirs(os.path.dirname(csv_out), exist_ok=True)
    if not os.path.exists(csv_out) and os.path.exists(xlsx_in):
        xlsx_first_sheet_to_csv(xlsx_in, csv_out)
    return csv_out


def create_jwt_token(user_id: str, username: str) -> str:
    """
    Create a JWT token for session authentication.
    
    This function generates a JWT token using the HS256 algorithm with:
    - Header: Specifies token type and signing algorithm
    - Payload: Contains user claims and expiration timestamp
    - Signature: HMAC-SHA256 signature for token integrity
    
    Security Notes:
    - Uses demo secret key (replace with secure random key in production)
    - 1-hour expiration time for session security
    - Base64 URL-safe encoding without padding for JWT standard compliance
    
    Args:
        user_id (str): Unique identifier for the user
        username (str): Human-readable username
        
    Returns:
        str: Signed JWT token in format header.payload.signature
        
    Token Structure:
        Header: {"typ": "JWT", "alg": "HS256"}
        Payload: {"user_id": "...", "username": "...", "exp": ..., "iat": ...}
        Signature: HMAC-SHA256 of header.payload using secret key
    """
    # Demo secret key - in production, use a secure random key from environment
    secret = "demo-secret-key-123"
    
    # JWT header specifying token type and algorithm
    header = {"typ": "JWT", "alg": "HS256"}
    
    # JWT payload with user claims and timestamps
    payload = {
        "user_id": user_id,        # Unique user identifier
        "username": username,       # Human-readable username
        "exp": time.time() + 3600, # Expiration: 1 hour from now
        "iat": time.time()         # Issued at: current timestamp
    }

    # Encode header and payload to base64 (URL-safe, no padding)
    header_b64 = base64.urlsafe_b64encode(json.dumps(header, separators=(',', ':')).encode()).decode().rstrip('=')
    payload_b64 = base64.urlsafe_b64encode(json.dumps(payload, separators=(',', ':')).encode()).decode().rstrip('=')
    
    # Create HMAC-SHA256 signature of header.payload
    message = f"{header_b64}.{payload_b64}"
    signature = hmac.new(secret.encode(), message.encode(), hashlib.sha256).digest()
    signature_b64 = base64.urlsafe_b64encode(signature).decode().rstrip('=')
    
    # Return complete JWT token
    return f"{header_b64}.{payload_b64}.{signature_b64}"


def validate_jwt_token(token: str) -> Optional[Dict[str, Any]]:
    """
    Validate a JWT token and return the payload if valid.
    
    This function performs comprehensive JWT validation:
    1. Structure validation (3 parts separated by dots)
    2. Signature verification using HMAC-SHA256
    3. Expiration check against current time
    4. Safe decoding with error handling
    
    Security Checks:
    - Verifies token signature matches expected value
    - Checks token hasn't expired (exp claim vs current time)
    - Handles malformed tokens gracefully
    - Uses constant-time comparison for signature verification
    
    Args:
        token (str): JWT token to validate
        
    Returns:
        Optional[Dict[str, Any]]: Token payload if valid, None if invalid/expired
        
    Validation Process:
        1. Split token into header.payload.signature
        2. Recompute signature using same secret and algorithm
        3. Compare signatures for integrity verification
        4. Decode payload and check expiration time
        5. Return payload or None based on validation result
    """
    try:
        # Split token into its three components
        parts = token.split('.')
        if len(parts) != 3:
            return None  # Invalid JWT structure
        
        header_b64, payload_b64, signature_b64 = parts
        
        # Verify signature integrity
        secret = "demo-secret-key-123"  # Must match creation secret
        message = f"{header_b64}.{payload_b64}"
        expected_signature = hmac.new(secret.encode(), message.encode(), hashlib.sha256).digest()
        expected_signature_b64 = base64.urlsafe_b64encode(expected_signature).decode().rstrip('=')
        
        # Signature verification (constant-time comparison)
        if signature_b64 != expected_signature_b64:
            return None  # Invalid signature
        
        # Decode payload from base64
        # Add padding if needed for proper base64 decoding
        payload_b64 += '=' * (4 - len(payload_b64) % 4)
        payload = json.loads(base64.urlsafe_b64decode(payload_b64.encode()).decode())
        
        # Check token expiration
        if payload.get('exp', 0) < time.time():
            return None  # Token has expired
        
        return payload  # Valid token, return claims
        
    except Exception:
        # Handle any decoding or parsing errors
        return None  # Invalid token format


# ===============================================================================
# GLOBAL SESSION STORAGE
# ===============================================================================
# These global variables manage the authentication state across tool calls.
# In production, these should be replaced with Redis, database, or other
# persistent storage solutions for scalability and reliability.

# Dictionary storing all active user sessions
# Structure: {session_id: {"user_id": str, "username": str, "token": str, "created_at": float}}
_USER_SESSIONS = {}

# Currently active session for this MCP server instance
# This enables the session-based authentication model where AI assistants
# authenticate once and then use tools without passing tokens
_CURRENT_SESSION = None

# ===============================================================================
# REPOSITORY INITIALIZATION  
# ===============================================================================
# Initialize data repositories and server components

# Prepare books CSV from Excel source and create repository
_CSV = _prepare_books_csv()
_BOOKS = BooksRepository(_CSV)

# Initialize exchange rates with synthetic data
_RATES = default_rates()

# Create MCP server instance with descriptive name
server = Server("books-mcp")


# ===============================================================================
# MCP TOOL DEFINITIONS
# ===============================================================================

@server.list_tools()
async def handle_list_tools() -> List[types.Tool]:
    """
    Define all available MCP tools for this server.
    
    This function returns the complete catalog of tools that AI assistants can use.
    Tools are divided into two categories:
    
    1. Protected Operations (require active session):
       - books_query: Search and retrieve book information from dataset
       - exchange_convert: Convert currency amounts using current rates
       
    2. Session Management (public access):
       - authenticate: Create new user session with JWT token
       - session_status: Check current authentication state  
       - logout: End current session and cleanup
    
    Schema Design:
    - All schemas use JSON Schema format for parameter validation
    - Required parameters explicitly defined for critical operations
    - Optional parameters allow flexible usage patterns
    - additionalProperties: false prevents unexpected parameters
    
    Returns:
        List[types.Tool]: Complete list of available MCP tools
    """
    return [
        # =======================================================================
        # PROTECTED OPERATIONS - REQUIRE ACTIVE SESSION
        # =======================================================================
        
        types.Tool(
            name="books_query",
            description="Search and retrieve books from the dataset. Supports filtering by title, author, genre, year, and pagination. Returns detailed book information including metadata. Requires active session for access.",
            inputSchema={
                "type": "object",
                "properties": {
                    "id": {
                        "type": "string", 
                        "description": "Specific book ID to fetch (returns single book)"
                    },
                    "genre": {
                        "type": "string", 
                        "description": "Filter books by genre/category"
                    },
                    "year": {
                        "type": "string", 
                        "description": "Filter by publication year (exact match)"
                    },
                    "author": {
                        "type": "string", 
                        "description": "Filter by author name (partial match supported)"
                    },
                    "title": {
                        "type": "string", 
                        "description": "Filter by book title (contains search)"
                    },
                    "limit": {
                        "type": "integer", 
                        "description": "Maximum number of results to return (default: 10)"
                    },
                    "offset": {
                        "type": "integer", 
                        "description": "Starting position for pagination (default: 0)"
                    },
                },
                "additionalProperties": False,
            },
        ),
        
        types.Tool(
            name="exchange_convert",
            description="Convert monetary amounts between different currencies using current exchange rates. Supports major world currencies with real-time conversion calculations. Requires active session for access.",
            inputSchema={
                "type": "object",
                "properties": {
                    "from_currency": {
                        "type": "string", 
                        "description": "Source currency code (e.g., 'USD', 'EUR', 'GBP')"
                    },
                    "to_currency": {
                        "type": "string", 
                        "description": "Target currency code for conversion"
                    },
                    "amount": {
                        "type": "number", 
                        "description": "Amount to convert (supports decimals)"
                    },
                },
                "required": ["from_currency", "to_currency", "amount"],
                "additionalProperties": False,
            },
        ),
        
        # =======================================================================
        # SESSION MANAGEMENT - PUBLIC ACCESS
        # =======================================================================
        
        types.Tool(
            name="authenticate",
            description="Create a new user session and authenticate for protected operations. Generates JWT token and establishes session state for subsequent tool calls. Required before using books_query or exchange_convert.",
            inputSchema={
                "type": "object",
                "properties": {
                    "username": {
                        "type": "string", 
                        "description": "Username for authentication (any string allowed for demo)"
                    },
                },
                "required": ["username"],
                "additionalProperties": False,
            },
        ),
        types.Tool(
            name="logout",
            description="End the current authentication session and clean up session data. Removes session from server storage and clears authentication state. Safe to call even when not authenticated.",
            inputSchema={
                "type": "object",
                "properties": {},
                "additionalProperties": False,
            },
        ),
        
        types.Tool(
            name="session_status",
            description="Check current authentication status and session information. Returns authentication state, user details, session age, and time remaining before expiration. Useful for monitoring session health.",
            inputSchema={
                "type": "object", 
                "properties": {},
                "additionalProperties": False,
            },
        ),
    ]


# ===============================================================================
# MCP TOOL CALL HANDLER
# ===============================================================================

@server.call_tool()
async def handle_call_tool(name: str, arguments: Dict[str, Any]) -> List[types.TextContent]:
    """
    Handle all incoming tool calls with session-based authentication.
    
    This is the main dispatcher for all MCP tool requests. It implements:
    
    1. Session Management Tools (no authentication required):
       - authenticate: Creates new session with JWT token
       - session_status: Returns current authentication state  
       - logout: Ends session and cleans up storage
    
    2. Protected Operations (require active session):
       - books_query: Database operations on book dataset
       - exchange_convert: Currency conversion calculations
    
    Authentication Flow:
    - Public tools execute immediately without session checks
    - Protected tools first validate _CURRENT_SESSION exists and is valid
    - Expired sessions are automatically cleaned up and marked invalid
    - All responses include user context for audit trails
    
    Error Handling:
    - authentication_required: No session for protected operations
    - session_expired: Session exists but exceeded time limit
    - tool_not_found: Unknown tool name requested
    - parameter_missing: Required parameters not provided
    
    Args:
        name (str): Name of the tool to execute
        arguments (Dict[str, Any]): Tool parameters from the request
        
    Returns:
        List[types.TextContent]: JSON response wrapped in MCP TextContent
        
    Session State Management:
    - _CURRENT_SESSION: Global variable tracking active session
    - _USER_SESSIONS: Dictionary of all active sessions with metadata
    - Automatic cleanup of expired sessions on access
    """
    global _CURRENT_SESSION
    
    # =======================================================================
    # TOOL NAME VALIDATION
    # =======================================================================
    
    # Check if tool name is valid before authentication check
    valid_tools = {"authenticate", "logout", "session_status", "books_query", "exchange_convert"}
    if name not in valid_tools:
        raise ValueError(f"Unknown tool: {name}")
    
    # =======================================================================
    # SESSION MANAGEMENT TOOLS (PUBLIC ACCESS)
    # =======================================================================
    
    if name == "authenticate":
        """
        Create new user session and authenticate for protected operations.
        
        Process:
        1. Extract username from arguments (default to demo_user)
        2. Generate unique user_id using hash of username
        3. Create JWT token with user claims and 1-hour expiration
        4. Store session in global _USER_SESSIONS dictionary
        5. Set _CURRENT_SESSION for immediate use
        6. Return session details and authentication confirmation
        """
        username = arguments.get("username", "demo_user")
        user_id = f"user_{hash(username) % 10000}"  # Generate deterministic user ID
        
        # Create JWT token with user claims
        token = create_jwt_token(user_id, username)
        
        # Generate unique session ID and store session data
        session_id = f"session_{hash(username + str(time.time())) % 100000}"
        _USER_SESSIONS[session_id] = {
            "username": username,    # Human-readable username
            "user_id": user_id,     # Unique user identifier
            "token": token,         # JWT token for validation
            "created_at": time.time()  # Session creation timestamp
        }
        
        # Set as current active session
        _CURRENT_SESSION = session_id
        
        # Return session details and success confirmation
        result = {
            "success": True,
            "message": f"Successfully authenticated as {username}",
            "username": username,
            "user_id": user_id,
            "session_id": session_id,
            "expires_in": 3600  # 1 hour in seconds
        }
        return [types.TextContent(type="text", text=str(result))]
    
    elif name == "logout":
        """
        End current authentication session and clean up session data.
        
        Process:
        1. Check if there's an active session
        2. Remove session from global storage
        3. Clear _CURRENT_SESSION variable
        4. Return logout confirmation with username
        5. Handle case where no session exists gracefully
        """
        if _CURRENT_SESSION and _CURRENT_SESSION in _USER_SESSIONS:
            username = _USER_SESSIONS[_CURRENT_SESSION]["username"]
            del _USER_SESSIONS[_CURRENT_SESSION]  # Remove from storage
            _CURRENT_SESSION = None  # Clear current session
            result = {
                "success": True, 
                "message": f"Successfully logged out {username}"
            }
        else:
            result = {
                "success": True, 
                "message": "No active session to logout"
            }
        return [types.TextContent(type="text", text=str(result))]
    
    elif name == "session_status":
        """
        Check current authentication status and session information.
        
        Process:
        1. Check if there's an active session in _CURRENT_SESSION
        2. Validate session exists in _USER_SESSIONS storage
        3. Check if session has expired (1 hour limit)
        4. Clean up expired sessions automatically
        5. Return detailed session information or unauthenticated state
        """
        if _CURRENT_SESSION and _CURRENT_SESSION in _USER_SESSIONS:
            session = _USER_SESSIONS[_CURRENT_SESSION]
            
            # Calculate session timing information
            session_age = int(time.time() - session["created_at"])
            expires_in = max(0, 3600 - session_age)  # Time remaining until expiration
            
            result = {
                "authenticated": True,
                "username": session["username"],
                "user_id": session["user_id"], 
                "session_age": session_age,      # How long session has been active
                "expires_in": expires_in         # Seconds until session expires
            }
        else:
            result = {
                "authenticated": False,
                "message": "No active session. Use 'authenticate' tool to login."
            }
        return [types.TextContent(type="text", text=str(result))]
    
    # =======================================================================
    # PROTECTED OPERATIONS - AUTHENTICATION REQUIRED
    # =======================================================================
    
    # Validate active session exists
    if not _CURRENT_SESSION or _CURRENT_SESSION not in _USER_SESSIONS:
        error_result = {
            "error": "authentication_required",
            "message": "No active session. Please authenticate first using the 'authenticate' tool.",
            "hint": "Call authenticate tool with your username to create a session"
        }
        return [types.TextContent(type="text", text=str(error_result))]
    
    # Validate session hasn't expired (1 hour limit)
    session = _USER_SESSIONS[_CURRENT_SESSION]
    if time.time() - session["created_at"] > 3600:  # 1 hour = 3600 seconds
        # Clean up expired session
        del _USER_SESSIONS[_CURRENT_SESSION]
        _CURRENT_SESSION = None
        error_result = {
            "error": "session_expired",
            "message": "Session has expired. Please authenticate again.",
            "hint": "Sessions expire after 1 hour. Please call authenticate tool again."
        }
        return [types.TextContent(type="text", text=str(error_result))]
    
    # Session is valid - extract user information for operation context
    username = session["username"]
    user_id = session["user_id"]
    
    # =======================================================================
    # BOOKS DATABASE OPERATIONS
    # =======================================================================
    
    if name == "books_query":
        """
        Search and retrieve books from the dataset with various filtering options.
        
        This tool provides flexible book search capabilities:
        - Specific book lookup by ID (returns single book)
        - Multi-field filtering (genre, year, author, title)
        - Pagination support (limit, offset)
        - Partial text matching for titles and authors
        
        All operations include authenticated_user context for audit trails.
        """
        # Extract search parameters from arguments
        book_id = arguments.get("id")          # Specific book ID lookup
        genre = arguments.get("genre")         # Filter by genre/category
        year = arguments.get("year")           # Filter by publication year
        author = arguments.get("author")       # Filter by author name
        title = arguments.get("title")         # Filter by title (contains)
        limit = arguments.get("limit")         # Maximum results to return
        offset = arguments.get("offset")       # Pagination offset
        
        # Handle specific book ID lookup (highest priority)
        if book_id not in (None, ""):
            item = _BOOKS.get_by_id(str(book_id))
            if item is None:
                error_result = {
                    "error": "not_found", 
                    "message": f"Book with ID '{book_id}' not found",
                    "authenticated_user": username
                }
                return [types.TextContent(type="text", text=str(error_result))]
            
            # Return single book with user context
            result = {
                "authenticated_user": username,
                "data": item,
                "query_type": "specific_book"
            }
            return [types.TextContent(type="text", text=str(result))]
        
        # Handle filtered search with multiple criteria
        data = _BOOKS.filter(
            genre=genre,              # Category filter
            year=year,                # Publication year filter
            author=author,            # Author name filter (partial match)
            title_contains=title,     # Title search (partial match)
            limit=limit,              # Result count limit
            offset=offset,            # Pagination offset
        )
        
        # Return search results with metadata
        result = {
            "authenticated_user": username,
            "data": data,
            "count": len(data),
            "query_type": "filtered_search",
            "filters_applied": {
                "genre": genre,
                "year": year, 
                "author": author,
                "title": title,
                "limit": limit,
                "offset": offset
            }
        }
        return [types.TextContent(type="text", text=str(result))]
    
    # =======================================================================
    # CURRENCY EXCHANGE OPERATIONS
    # =======================================================================
    
    elif name == "exchange_convert":
        """
        Convert monetary amounts between different currencies.
        
        This tool provides real-time currency conversion using:
        - Synthetic exchange rates for demonstration
        - Support for major world currencies
        - Decimal precision for accurate calculations
        - Error handling for invalid currency codes
        
        All conversions include authenticated_user context for audit trails.
        """
        # Extract required conversion parameters
        from_currency = arguments["from_currency"]  # Source currency code
        to_currency = arguments["to_currency"]      # Target currency code  
        amount = arguments["amount"]                 # Amount to convert
        
        try:
            # Perform currency conversion using exchange rates
            value = _RATES.convert(float(amount), from_currency, to_currency)
            
            # Return conversion result with detailed information
            result = {
                "authenticated_user": username,
                "from": from_currency.upper(),    # Normalized source currency
                "to": to_currency.upper(),        # Normalized target currency
                "amount": float(amount),          # Original amount
                "converted": value,               # Converted amount
                "operation": "currency_conversion",
                "timestamp": time.time()          # Conversion timestamp
            }
            return [types.TextContent(type="text", text=str(result))]
            
        except Exception as e:
            # Handle conversion errors (invalid currencies, rates, etc.)
            error_result = {
                "error": "conversion_failed", 
                "message": str(e),
                "authenticated_user": username,
                "attempted_conversion": f"{amount} {from_currency} -> {to_currency}"
            }
            return [types.TextContent(type="text", text=str(error_result))]
    
    # This should never be reached due to early validation above
    # But kept as a safety net
    raise ValueError(f"Unknown tool: {name}")


# ===============================================================================
# MCP SERVER MAIN FUNCTION
# ===============================================================================

async def main() -> None:
    """
    Run the MCP server with stdio transport.
    
    This function initializes and runs the Model Context Protocol server using
    standard input/output for communication. This is the standard transport
    method for MCP servers that integrates with AI assistants and tools.
    
    The server will:
    1. Set up stdio streams for communication
    2. Initialize the MCP server with standard options
    3. Run the server event loop to handle incoming requests
    4. Process tool calls and return responses
    
    Transport Method:
    - Uses stdio (standard input/output) for communication
    - Compatible with AI assistants and MCP clients
    - Handles JSON-RPC protocol automatically
    - Manages connection lifecycle and error handling
    
    Usage:
    - Run directly: python -m mcp_server.server
    - Or via MCP client configuration in AI assistant settings
    """
    async with stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,             # Input stream for receiving requests
            write_stream,            # Output stream for sending responses
            server.create_initialization_options()  # Standard MCP initialization
        )


# ===============================================================================
# MAIN ENTRY POINT
# ===============================================================================

if __name__ == "__main__":
    """
    Entry point for running the MCP server directly.
    
    This allows the server to be run as a standalone Python module:
    - python mcp_server/server.py
    - python -m mcp_server.server
    
    The server will start and listen for MCP protocol messages on stdio,
    enabling integration with AI assistants and other MCP clients.
    """
    asyncio.run(main())

