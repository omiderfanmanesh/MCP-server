# Adding JWT Token MCP Server to Cursor

This guide shows you how to integrate your JWT token MCP server with Cursor IDE.

## Step-by-Step Setup

### 1. Open Cursor Settings

- **Method 1**: Press `Cmd + ,` (Mac) or `Ctrl + ,` (Windows/Linux)
- **Method 2**: Click `Cursor` → `Settings` in the menu bar
- **Method 3**: Use Command Palette (`Cmd/Ctrl + Shift + P`) → "Preferences: Open Settings"

### 2. Navigate to MCP Settings

- In the settings search bar, type: **"MCP"**
- Or navigate to: **Features → Model Context Protocol**
- You should see the MCP configuration section

### 3. Add Your Server Configuration

Since your server is running in Docker, click **"Edit in settings.json"** and add this configuration:

```json
{
  "mcpServers": {
    "jwt-books-server": {
      "command": "docker",
      "args": ["exec", "-i", "mcp-books-server", "python", "-m", "mcp_server.server"],
      "cwd": "/Users/omiderfanmanesh/Projects/MCP-server"
    }
  }
}
```

**Important**: 
- Replace `/Users/omiderfanmanesh/Projects/MCP-server` with your actual project path
- Make sure your Docker container is running: `docker-compose up -d`
- The container name `mcp-books-server` must match your docker-compose.yml

### 4. Alternative: Use the UI

If you prefer the UI instead of editing JSON:

1. Click **"Add Server"** button
2. Fill in the fields:
   - **Name**: `jwt-books-server`
   - **Command**: `python`
   - **Arguments**: `-m mcp_server.server`
   - **Working Directory**: `/Users/omiderfanmanesh/Projects/MCP-server`
   - **Environment Variables**:
     - `PYTHONUNBUFFERED=1`
     - `PYTHONIOENCODING=utf-8`

### 5. Restart Cursor

- Close and reopen Cursor completely
- Or use Command Palette: **"Developer: Reload Window"**

### 6. Test the Connection

1. Open a new chat in Cursor
2. Look for **"jwt-books-server"** in the available tools/context
3. Try asking: *"Can you generate a JWT token for username 'test_user'?"*

## Using the Tools

Once connected, you can use these tools in Cursor chat:

### Generate JWT Token
```
"Generate a JWT token for username 'john_doe'"
```

### Search Books  
```
"Find books by Stephen King"
"Show me 5 fiction books"
```

### Convert Currency
```
"Convert 100 USD to EUR"
```

## Troubleshooting

### ❌ Server Not Showing Up

**Check:**
1. Python is installed and in your PATH
2. You're in the correct working directory
3. Required packages are installed: `pip install -r requirements.txt`
4. Restart Cursor completely

**Test manually:**
```bash
cd /Users/omiderfanmanesh/Projects/MCP-server
python -m mcp_server.server
```

### ❌ "Command not found" Error

**Solution**: Use full Python path
```json
{
  "command": "/usr/bin/python3",
  "args": ["-m", "mcp_server.server"]
}
```

Find your Python path:
```bash
which python
which python3
```

### ❌ Import Errors

**Solution**: Install dependencies
```bash
cd /Users/omiderfanmanesh/Projects/MCP-server
pip install -r requirements.txt
```

### ❌ Permission Issues

**Solution**: Make sure you have read/write access to the project directory
```bash
ls -la /Users/omiderfanmanesh/Projects/MCP-server
```

## Advanced Configuration

### Using Virtual Environment

If you use a virtual environment:

```json
{
  "command": "/Users/omiderfanmanesh/Projects/MCP-server/venv/bin/python",
  "args": ["-m", "mcp_server.server"],
  "cwd": "/Users/omiderfanmanesh/Projects/MCP-server"
}
```

### Using Conda

If you use conda:

```json
{
  "command": "conda",
  "args": ["run", "-n", "your-env-name", "python", "-m", "mcp_server.server"],
  "cwd": "/Users/omiderfanmanesh/Projects/MCP-server"
}
```

Replace `your-env-name` with your actual conda environment name.

### With Docker (if you have Docker installed)

```json
{
  "command": "docker",
  "args": ["run", "--rm", "-i", "mcp-books-server"],
  "cwd": "/Users/omiderfanmanesh/Projects/MCP-server"
}
```

## Testing Your Setup

### 1. Basic Connection Test

Ask Cursor: *"What tools are available from the jwt-books-server?"*

### 2. JWT Token Test

Ask Cursor: *"Generate a JWT token for username 'demo_user' and show me what's in it"*

### 3. Book Search Test  

Ask Cursor: *"Find 3 books and show me their details"*

### 4. Currency Test

Ask Cursor: *"Convert 50 USD to GBP"*

## Example Chat Prompts

Once your server is connected, try these example prompts in Cursor:

```
"Generate a JWT token for 'alice' and explain what each part means"

"Search for books with 'science' in the title and limit to 5 results"

"Convert 1000 EUR to JPY and USD"

"Create a JWT token for 'bob' and then search for fiction books"
```

## Success Indicators

✅ **You'll know it's working when:**
- Server appears in Cursor's MCP servers list
- You can see tools like `get_jwt_token`, `books_query`, `exchange_convert`
- Cursor can successfully call these tools and get responses
- JWT tokens are generated with proper format

## Configuration File Location

Your complete configuration should be in Cursor's settings.json at:
- **Mac**: `~/Library/Application Support/Cursor/User/settings.json`
- **Windows**: `%APPDATA%\Cursor\User\settings.json`
- **Linux**: `~/.config/Cursor/User/settings.json`

---

## 🎉 How to Use Your Authenticated JWT MCP Server

Now that authentication is enabled, here's how the new system works:

### � Authentication Flow

**Step 1: Generate a JWT Token (No Auth Required)**
```
"Generate a JWT token for user 'john_doe'"
```

**Step 2: Use the Token for Protected Operations**
```
"Search for books about 'python' with token: [paste your JWT token here]"
"Convert 100 USD to EUR with token: [paste your JWT token here]"
```

### � Authentication Rules

- ✅ **`get_jwt_token`** - No authentication required (generates tokens)
- 🔒 **`books_query`** - Requires valid JWT token 
- 🔒 **`exchange_convert`** - Requires valid JWT token

### 🎯 Example Usage Flow

**1. First, generate a token:**
```
"Generate a JWT token for user 'alice'"
```

**Response:**
```json
{
  "token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
  "user_id": "user_1234",
  "username": "alice",
  "expires_in": 3600,
  "token_type": "Bearer",
  "message": "Token generated successfully! Use this token for authenticated requests."
}
```

**2. Copy the token and use it for protected operations:**
```
"Search for fiction books with token: eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
```

### ❌ What Happens Without Authentication

**Unauthenticated Request:**
```
"Search for books about 'python'"
```

**Response:**
```json
{
  "error": "authentication_required",
  "message": "JWT token is required. Generate one using get_jwt_token first.",
  "hint": "Include 'token' parameter with your JWT token"
}
```

### ✅ Authenticated Response

**Authenticated Request:**
```
"Search for programming books with token: [valid-jwt-token]"
```

**Response:**
```json
{
  "authenticated_user": "alice",
  "data": [...books...],
  "count": 5
}
```

### � Token Expiration

- Tokens expire after **1 hour**
- Expired tokens return: `"error": "invalid_token"`
- Simply generate a new token when needed

### 🛠️ Pro Tips for Authentication

1. **Save Your Tokens**: Copy generated tokens for repeated use
2. **Check Expiration**: Tokens last 1 hour, generate new ones as needed
3. **User Context**: Each token includes the username in responses
4. **Test Flow**: Always test without token first to see auth errors
5. **Token Format**: Include the full JWT string after "token:"