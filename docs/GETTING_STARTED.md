# Getting Started Guide

Welcome to the Session-Based Authenticated MCP Server! This guide will help you get up and running quickly.

## Table of Contents

1. [Quick Start](#quick-start)
2. [Understanding the System](#understanding-the-system)
3. [First Steps](#first-steps)
4. [Basic Usage Examples](#basic-usage-examples)
5. [Common Workflows](#common-workflows)
6. [Troubleshooting](#troubleshooting)
7. [Next Steps](#next-steps)

---

## Quick Start

### 30-Second Setup

1. **Clone and Install**:
   ```bash
   git clone <repository-url>
   cd MCP-server
   pip install -r requirements.txt
   ```

2. **Run the Server**:
   ```bash
   python -m mcp_server.server
   ```

3. **Test with AI Assistant**:
   Configure your AI assistant to connect to the MCP server and try:
   ```
   Call: authenticate {"username": "your_name"}
   Call: books_query {"title": "python", "limit": 3}
   ```

That's it! You now have a working authenticated MCP server.

---

## Understanding the System

### What is This System?

The Session-Based Authenticated MCP Server is a **Model Context Protocol** server that provides:
- 📚 **Books Database**: Search through thousands of books
- 💱 **Currency Exchange**: Convert between world currencies  
- 🔐 **Session Authentication**: Secure access designed for AI assistants

### Key Concepts

**Session-Based Authentication**: Unlike traditional APIs where you pass a token with each request, this system works like a conversation:
1. You authenticate once: "Hello, I'm Alice"
2. The server remembers you: "Hi Alice! I'll remember you for 1 hour"
3. You use tools freely: "Show me Python books" → "Here are Python books for Alice"
4. Session expires automatically for security

**AI Assistant Friendly**: Designed specifically for AI assistants like GitHub Copilot and Cursor that can't easily manage authentication tokens in individual tool calls.

### Architecture Overview

```
AI Assistant → MCP Client → MCP Server → [Authentication] → Data Sources
                                      ↓
                                 Session Store
```

---

## First Steps

### Step 1: Choose Your Setup Method

**Option A - Local Development (Recommended for Learning)**:
```bash
# Setup Python environment
conda create -n mcp-server python=3.12
conda activate mcp-server
pip install -r requirements.txt

# Run directly
python -m mcp_server.server
```

**Option B - Docker (Recommended for Production)**:
```bash
# Build and run with Docker
docker-compose up

# Or build manually
docker build -t mcp-server .
docker run -v $(pwd)/data:/app/data mcp-server
```

### Step 2: Verify Installation

Test that everything works:
```bash
# Check Python imports
python -c "import mcp_server.server; print('✓ Server module OK')"

# Check data files
ls sample-data/BooksDatasetClean.xlsx
ls data/books.csv  # Created automatically
```

### Step 3: Configure AI Assistant

**For Cursor IDE**:
Add to your `.cursor/settings.json`:
```json
{
  "mcpServers": {
    "books-mcp": {
      "command": "python",
      "args": ["-m", "mcp_server.server"],
      "cwd": "/absolute/path/to/MCP-server"
    }
  }
}
```

**For GitHub Copilot**:
Configure your MCP client to connect to the server.

---

## Basic Usage Examples

### Example 1: Your First Session

```json
// 1. Start by checking if you're logged in
Tool: session_status
Arguments: {}
Response: {"authenticated": false, "message": "No active session..."}

// 2. Log in with any username
Tool: authenticate  
Arguments: {"username": "alice"}
Response: {
  "success": true,
  "username": "alice", 
  "session_id": "session_12345",
  "expires_in": 3600
}

// 3. Verify you're logged in
Tool: session_status
Arguments: {}
Response: {
  "authenticated": true,
  "username": "alice",
  "session_age": 15,
  "expires_in": 3585
}
```

### Example 2: Searching for Books

```json
// Find books about Python programming
Tool: books_query
Arguments: {"title": "python", "limit": 3}
Response: {
  "authenticated_user": "alice",
  "data": [
    {
      "id": "book_456",
      "Title": "Python Tricks",
      "Authors": "Dan Bader",
      "Category": "Programming",
      "Price Starting With ($)": "29.99"
    }
  ],
  "count": 1
}

// Find books by a specific author
Tool: books_query
Arguments: {"author": "Robert Martin"}
Response: {
  "authenticated_user": "alice",
  "data": [
    {
      "Title": "Clean Code",
      "Authors": "Robert Martin",
      "Category": "Programming",
      "Publisher": "Prentice Hall"
    }
  ]
}
```

### Example 3: Currency Conversion

```json
// Convert USD to EUR
Tool: exchange_convert
Arguments: {
  "from_currency": "USD",
  "to_currency": "EUR", 
  "amount": 100
}
Response: {
  "authenticated_user": "alice",
  "from": "USD",
  "to": "EUR",
  "amount": 100.0,
  "converted": 85.23,
  "timestamp": 1640995200.0
}

// Convert with decimals
Tool: exchange_convert
Arguments: {
  "from_currency": "GBP",
  "to_currency": "JPY",
  "amount": 50.75
}
Response: {
  "authenticated_user": "alice", 
  "from": "GBP",
  "to": "JPY",
  "amount": 50.75,
  "converted": 7631.25
}
```

### Example 4: Session Management

```json
// Check how much time you have left
Tool: session_status
Arguments: {}
Response: {
  "authenticated": true,
  "username": "alice",
  "session_age": 1800,    // 30 minutes old
  "expires_in": 1800      // 30 minutes left
}

// Log out when done (optional - sessions expire automatically)
Tool: logout
Arguments: {}
Response: {
  "success": true,
  "message": "Successfully logged out alice"
}
```

---

## Common Workflows

### Workflow 1: Research Assistant

Perfect for AI assistants helping with research:

```json
// 1. Authenticate
{"tool": "authenticate", "arguments": {"username": "researcher"}}

// 2. Find programming books
{"tool": "books_query", "arguments": {"genre": "Programming", "limit": 5}}

// 3. Find specific author's works  
{"tool": "books_query", "arguments": {"author": "Martin Fowler"}}

// 4. Get pricing for international sales
{"tool": "exchange_convert", "arguments": {"from_currency": "USD", "to_currency": "EUR", "amount": 45.99}}

// 5. Clean up (optional)
{"tool": "logout", "arguments": {}}
```

### Workflow 2: Book Discovery

For finding books on specific topics:

```json
// 1. Log in
{"tool": "authenticate", "arguments": {"username": "bookworm"}}

// 2. Search by multiple criteria
{"tool": "books_query", "arguments": {"title": "data science", "year": "2020"}}

// 3. Browse by category
{"tool": "books_query", "arguments": {"genre": "Science", "limit": 10}}

// 4. Get detailed book info
{"tool": "books_query", "arguments": {"id": "book_123"}}
```

### Workflow 3: International Commerce

For e-commerce price calculations:

```json
// 1. Authenticate
{"tool": "authenticate", "arguments": {"username": "merchant"}}

// 2. Get book prices in different currencies
{"tool": "books_query", "arguments": {"title": "economics", "limit": 5}}

// 3. Convert prices for different markets
{"tool": "exchange_convert", "arguments": {"from_currency": "USD", "to_currency": "EUR", "amount": 29.99}}
{"tool": "exchange_convert", "arguments": {"from_currency": "USD", "to_currency": "GBP", "amount": 29.99}}
{"tool": "exchange_convert", "arguments": {"from_currency": "USD", "to_currency": "JPY", "amount": 29.99}}
```

### Workflow 4: Long Research Session

For extended work periods:

```json
// 1. Start session
{"tool": "authenticate", "arguments": {"username": "academic"}}

// 2. Multiple searches over time...
{"tool": "books_query", "arguments": {"author": "Knuth"}}
// ... 30 minutes later ...
{"tool": "books_query", "arguments": {"title": "algorithms"}}

// 3. Check session health periodically
{"tool": "session_status", "arguments": {}}

// 4. If session expires, re-authenticate
{"tool": "authenticate", "arguments": {"username": "academic"}}
```

---

## Troubleshooting

### Problem: "authentication_required" Error

**Symptom**:
```json
{"error": "authentication_required", "message": "No active session..."}
```

**Solution**:
```json
// Simply authenticate first
{"tool": "authenticate", "arguments": {"username": "your_name"}}

// Then try your operation again
{"tool": "books_query", "arguments": {"title": "python"}}
```

### Problem: "session_expired" Error

**Symptom**:
```json
{"error": "session_expired", "message": "Session has expired..."}
```

**Explanation**: Sessions last 1 hour for security. After that, you need to log in again.

**Solution**:
```json
// Just authenticate again
{"tool": "authenticate", "arguments": {"username": "your_name"}}
```

### Problem: "not_found" Error for Books

**Symptom**:
```json
{"error": "not_found", "message": "Book with ID 'xyz' not found"}
```

**Solution**:
```json
// Use search instead of specific ID
{"tool": "books_query", "arguments": {"title": "search terms", "limit": 10}}

// Or browse by category
{"tool": "books_query", "arguments": {"genre": "Programming"}}
```

### Problem: Server Won't Start

**Symptom**:
```bash
ModuleNotFoundError: No module named 'mcp'
```

**Solution**:
```bash
# Install requirements
pip install -r requirements.txt

# Verify installation
python -c "import mcp; print('MCP installed')"
```

### Problem: Data Files Missing

**Symptom**:
```bash
FileNotFoundError: BooksDatasetClean.xlsx
```

**Solution**:
```bash
# Check if sample data exists
ls sample-data/
# Should show: BooksDatasetClean.xlsx

# If missing, ensure you have the complete repository
git status
```

---

## Next Steps

### For Developers

1. **Explore the Code**:
   - Read `mcp_server/server.py` for authentication logic
   - Check `mcp_server/books.py` for database operations
   - Review `mcp_server/exchange.py` for currency conversion

2. **Run Tests**:
   ```bash
   python -m pytest tests/ -v
   ```

3. **Extend Functionality**:
   - Add new tools to the server
   - Integrate with real databases
   - Add more authentication methods

### For AI Assistant Users

1. **Master the Workflow**:
   - Always authenticate first
   - Use `session_status` to check remaining time
   - Logout when finished (optional)

2. **Explore Advanced Features**:
   - Complex book searches with multiple filters
   - Currency conversions for international pricing
   - Session management for long research tasks

3. **Integration Tips**:
   - Save common search patterns
   - Create templates for frequent workflows
   - Monitor session expiration for long tasks

### For Production Users

1. **Security Setup**:
   - Replace demo JWT secret with secure key
   - Set up proper session storage (Redis)
   - Configure logging and monitoring

2. **Scalability**:
   - Use Docker for deployment
   - Set up load balancing for multiple instances
   - Implement proper backup procedures

3. **Documentation**:
   - Read the [Deployment Guide](DEPLOYMENT.md)
   - Review the [Architecture Documentation](ARCHITECTURE.md)
   - Check the [API Reference](API.md)

---

## Quick Reference

### Essential Commands

```json
// Authentication
{"tool": "authenticate", "arguments": {"username": "your_name"}}
{"tool": "session_status", "arguments": {}}
{"tool": "logout", "arguments": {}}

// Books (requires authentication)
{"tool": "books_query", "arguments": {"title": "search_term"}}
{"tool": "books_query", "arguments": {"author": "author_name"}}
{"tool": "books_query", "arguments": {"genre": "category"}}
{"tool": "books_query", "arguments": {"id": "book_id"}}

// Currency (requires authentication)  
{"tool": "exchange_convert", "arguments": {"from_currency": "USD", "to_currency": "EUR", "amount": 100}}
```

### Common Parameters

**Books Query**:
- `title`: Search in book titles
- `author`: Filter by author name
- `genre`: Filter by category
- `year`: Filter by publication year
- `limit`: Maximum results (default: 10)
- `offset`: Skip results for pagination

**Currency Convert**:
- `from_currency`: Source currency (USD, EUR, GBP, etc.)
- `to_currency`: Target currency
- `amount`: Amount to convert (supports decimals)

### Session Information

- **Duration**: 1 hour (3600 seconds)
- **Automatic Cleanup**: Expired sessions removed automatically
- **Re-authentication**: Just call `authenticate` again after expiration

---

Ready to start? Try the [Quick Start](#quick-start) section above and begin exploring your authenticated MCP server!