# 🎯 Usage Examples

This document provides real-world examples of using the Session-Based Authenticated MCP Server.

## Session Authentication Workflow

### Example 1: First-Time User Setup

**Step 1: Authenticate Your Session**
```
User: "Please authenticate me as 'developer'"
```

**Server Response:**
```json
{
  "session_id": "sess_dev_20240921_143022",
  "user_id": "user_7890",
  "username": "developer",
  "authenticated_at": "2024-09-21T14:30:22Z",
  "session_expires": "2024-09-21T15:30:22Z",
  "status": "authenticated",
  "message": "Authentication successful! Session is active for 1 hour."
}
```

**Step 2: Verify Your Session Status**
```
User: "What's my current session status?"
```

**Response:**
```json
{
  "session_active": true,
  "session_id": "sess_dev_20240921_143022",
  "username": "developer",
  "authenticated_at": "2024-09-21T14:30:22Z",
  "time_remaining": "55 minutes",
  "status": "Session active and ready for operations"
}
```

## 🎯 Cursor IDE Examples

### Authentication Flow in Cursor

**First, authenticate your session:**
```
User: "Authenticate me as data_analyst"
```

**Then start using the tools:**
```
User: "Find me trending science fiction books from the last 5 years"
User: "Show me classic fantasy novels that are highly rated"
User: "What mystery books were published in 2020?"
```

### Session Management

**Check your session status:**
```
User: "What's my current authentication status?"
```

**When done working:**
```
User: "Please log me out"
```

Expected Response:
```json
{
  "logged_out": true,
  "session_cleared": true,
  "message": "Successfully logged out. Session data cleared."
}
```

### Book Discovery Queries

**Genre Exploration:**
```
"Find me trending science fiction books from the last 5 years"
"Show me classic fantasy novels that are highly rated"
"What mystery books were published in 2020?"
```

**Author Deep Dives:**
```
"Find all books by Isaac Asimov in the database"
"Show me Stephen King's most recent works"
"List books by female authors in the science fiction genre"
```

**Smart Recommendations:**
```
"Recommend books similar to Dune"
"Find books for someone who loves both fantasy and historical fiction"
"What are some good starting books for someone new to science fiction?"
```

### Currency Operations

**Travel Planning:**
```
"I'm traveling to Europe with $500, how much is that in EUR?"
"Convert my $1000 budget to GBP and EUR for my UK trip"
"What's the current exchange rate from CAD to JPY?"
```

**Shopping Comparisons:**
```
"If a book costs £15 in the UK, how much is that in USD?"
"Compare prices: $25 USD vs €20 EUR vs £18 GBP"
```

## 🤖 AI Assistant Examples (GitHub Copilot / Claude Desktop)

### Complete Authentication Workflow

**Step 1: Start Your Session**
```
User: "I need to authenticate to use the MCP server"
Assistant: I'll authenticate you now.
[Calls authenticate tool with username from context]

Response: ✅ Authentication successful! Your session is now active.
```

**Step 2: Use Protected Operations**
```
User: "Find books about artificial intelligence"
Assistant: Now that you're authenticated, I can search the books database.
[Calls books_query tool - works because session is active]

Results: Found 15 books about artificial intelligence...
```

**Step 3: Session Management**
```
User: "How much time do I have left in my session?"
Assistant: Let me check your session status.
[Calls session_status tool]

Response: You have 45 minutes remaining in your current session.
```

### Research Assistance

**Academic Research:**
```
"Help me find books about artificial intelligence published after 2018"
"I need sources on climate change - what books are available?"
"Find books about data science for beginners"
```

**Content Creation:**
```
"I'm writing about space exploration - find relevant books for research"
"Need inspiration for a fantasy story - show me popular fantasy books"
"Find books about economics to reference in my article"
```

### Error Handling Examples

**Trying to use tools without authentication:**
```
User: "Find me some books"
Assistant: I need to authenticate you first.
[Calls authenticate tool with default username]

Success: Authentication successful! Now I can search for books.
[Calls books_query tool]
```

**Session expiry handling:**
```
User: "Convert 100 USD to EUR" (after 1+ hour)
Assistant: Let me convert that for you.
[Calls exchange_convert tool]

Error: Session expired. Re-authenticating...
[Calls authenticate tool automatically]
Success: Session renewed. Converting 100 USD to EUR...
```

### Data Analysis Workflows

**Market Research:**
```
"Analyze book trends: what genres are most popular in the 2020s?"
"Compare publication years - are more books being published recently?"
"Show me the distribution of books by decade"
```

**Currency Analysis:**
```
"If I'm buying books internationally, what's the best currency to use?"
"Calculate bulk pricing: 100 books at $15 each in different currencies"
"Show me exchange rates for all major currencies against USD"
```

## 🔧 VS Code Integration Examples

### Session-Based Workflow

**Authentication in VS Code:**
```
User: "Authenticate me as researcher"
Response: ✅ Session authenticated for user 'researcher'
Session ID: sess_researcher_20240921_150000
Valid until: 2024-09-21T16:00:00Z
```

**Currency conversion:**
```
User: "I have 500 GBP, how much is that in Japanese Yen?"
Response: Converting 500 GBP to JPY...
Result: 500.00 GBP = 74,250.00 JPY
```

**Session status check:**
```
User: "What's my session status?"
Response: 
- Session Active: ✅ Yes
- Username: researcher  
- Time Remaining: 38 minutes
- Session ID: sess_researcher_20240921_150000
```

## Claude Desktop Examples

### Complete Session Workflow

**Authentication:**
```
User: I love fantasy novels. Can you recommend some good ones?
Assistant: I'll need to authenticate first to access the books database.
[Calls authenticate tool]
✅ Authenticated! Now searching for fantasy novels...
[Calls books_query with genre="Fantasy"]
```

**Research assistance with session management:**
```
User: I'm writing a paper on 1950s science fiction. What books from that era are available?
Assistant: Perfect! Let me authenticate and search for 1950s science fiction.
[Calls authenticate tool, then books_query with filters]
Found 12 science fiction books from the 1950s...
```

### Complex Workflows with Session Management

**Multi-step planning with authentication:**
```
User: I want to buy books by Isaac Asimov. The price is $15 USD each. How much would 3 books cost in EUR?
Assistant: 
1. First, I'll authenticate to access the system...
   [Calls authenticate tool]
   ✅ Session authenticated!

2. Now let me find Isaac Asimov books...
   [Calls books_query with author="Isaac Asimov"]
   Found 8 books by Isaac Asimov in our database.

3. Converting $45 USD (3 × $15) to EUR...
   [Calls exchange_convert with amount=45, from="USD", to="EUR"]
   
Result: 3 books at $15 each = $45 USD = €38.35 EUR
```

**Extended session with logout:**
```
User: I'm done with my research. Please log me out.
Assistant: I'll log you out of your session.
[Calls logout tool]
✅ Successfully logged out! Your session data has been cleared.
```

## API Client Examples

### Python Client with Session Authentication

```python
import asyncio
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

async def authenticated_search():
    server_params = StdioServerParameters(
        command="python",
        args=["-m", "mcp_server.server"]
    )
    
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            
            # Step 1: Authenticate
            auth_result = await session.call_tool(
                "authenticate",
                {"username": "python_client"}
            )
            print(f"✅ {auth_result.content[0].text}")
            
            # Step 2: Search for science fiction books
            result = await session.call_tool(
                "books_query",
                {"genre": "Science Fiction", "limit": 5}
            )
            print(result.content[0].text)
            
            # Step 3: Check session status
            status = await session.call_tool("session_status", {})
            print(f"Session: {status.content[0].text}")
            
            # Step 4: Logout when done
            logout = await session.call_tool("logout", {})
            print(f"✅ {logout.content[0].text}")

asyncio.run(authenticated_search())
```

### JavaScript Client with Session Management

```javascript
import { Client } from '@modelcontextprotocol/sdk/client/index.js';
import { StdioClientTransport } from '@modelcontextprotocol/sdk/client/stdio.js';

const transport = new StdioClientTransport({
  command: 'python',
  args: ['-m', 'mcp_server.server']
});

const client = new Client({
  name: "books-client",
  version: "1.0.0"
}, {
  capabilities: {}
});

await client.connect(transport);

// Step 1: Authenticate
const authResult = await client.request({
  method: "tools/call",
  params: {
    name: "authenticate",
    arguments: {
      username: "js_client"
    }
  }
});
console.log("✅ Authenticated:", authResult);

// Step 2: Convert currency (now that we're authenticated)
const result = await client.request({
  method: "tools/call",
  params: {
    name: "exchange_convert",
    arguments: {
      from_currency: "USD",
      to_currency: "EUR", 
      amount: 100
    }
  }
});
console.log("💱 Conversion:", result);

// Step 3: Logout
const logoutResult = await client.request({
  method: "tools/call",
  params: {
    name: "logout",
    arguments: {}
  }
});
console.log("👋 Logged out:", logoutResult);
```

## Command Line Examples

### Using MCP Inspector

```bash
# Install MCP Inspector
npm install -g @modelcontextprotocol/inspector

# Test the server
npx @modelcontextprotocol/inspector python -m mcp_server.server
```

### Direct Testing

```bash
# Start the server
python -m mcp_server.server

# Send test requests (manual JSON-RPC)
echo '{"jsonrpc":"2.0","id":1,"method":"tools/list","params":{}}' | python -m mcp_server.server
```

## Error Handling Examples

### Authentication Required

```
User: Get book with ID 123
Assistant: [Calls books_query without authentication]
Response: ❌ Authentication required. Please authenticate first using the authenticate tool.

User: Please authenticate me  
Assistant: [Calls authenticate tool]
Response: ✅ Authentication successful! Now I can search for book ID 123.
```

### Session Expiry

```
User: Convert 100 USD to EUR (after 1+ hour of inactivity)
Assistant: [Calls exchange_convert with expired session]
Response: ❌ Session expired. Please authenticate again.
```

### Invalid Book ID

```
User: Get book with ID 99999
Response: Book with ID 99999 not found
```

### Unsupported Currency

```
User: Convert 100 XYZ to USD
Response: Error: Unsupported currency code: XYZ
```

### Invalid Parameters

```
User: Convert "hello" dollars to EUR
Response: Error: Amount must be a valid number
```

## Performance Examples

### Large Dataset Queries

```
User: Show me all books (no limit)
Response: [Returns paginated results with count information]
```

### Concurrent Requests

```python
# Multiple simultaneous requests
tasks = [
    session.call_tool("books_query", {"genre": "Fiction"}),
    session.call_tool("exchange_convert", {"from_currency": "USD", "to_currency": "EUR", "amount": 100}),
    session.call_tool("books_query", {"author": "Tolkien"})
]

results = await asyncio.gather(*tasks)
```

## Integration Patterns

### Smart Session Management

**Auto-authentication pattern:**
```
User: I'm studying literature from the 1960s. Help me find relevant books and calculate research budget costs.
Assistant:
1. First, I'll authenticate you automatically...
   [Calls authenticate with username="literature_researcher"]
   ✅ Session established!

2. Searching for books from the 1960s...
   [Calls books_query with year filter]
   Found 23 books from the 1960s across various genres.

3. Let me help estimate costs in your local currency...
   [Calls exchange_convert for price calculations]
   Estimated budget: $345 USD = €294 EUR = £251 GBP
```

### Recommendation System with Session Continuity

```
User: I liked "Dune". What similar books do you recommend?
Assistant:
1. Maintaining your active session (35 minutes remaining)...
2. Searching for science fiction books similar to Dune...
   [Calls books_query with genre="Science Fiction"]
3. Here are 8 recommendations from our database...
4. If you're interested in purchasing internationally, I can help with currency conversion.

User: Yes, convert $120 to Canadian dollars
Assistant: [Calls exchange_convert]
Result: $120 USD = $162 CAD
```

### Extended Research Workflow

```
User: I need comprehensive research on space exploration literature for my thesis.
Assistant:
1. Authenticating for extended research session...
   [Calls authenticate tool]
   ✅ Ready for research! Session expires in 60 minutes.

2. Finding space exploration books...
   [Multiple calls to books_query with various space-related terms]
   
3. Organizing results by publication decade...
   
4. Calculating research material costs...
   [Calls exchange_convert for budget planning]
   
5. Session status check...
   [Calls session_status]
   Session healthy - 45 minutes remaining.

User: Perfect! Save my session for later.
Assistant: Your session will remain active for 45 more minutes. 
When you return, just ask me anything and I'll check if you're still authenticated!
```

## 🚀 Quick Start Examples

### First Time Users

**Complete beginner workflow:**
```
User: "I'm new to this MCP server. What can it do?"
Assistant: 
Welcome! This server provides book database access and currency conversion. 
Let me authenticate you and show you what's available.

[Calls authenticate tool]
✅ You're now authenticated as 'new_user'!

Available tools:
- 📚 Search books by title, author, genre, or year
- 💱 Convert between currencies with real-time rates  
- 🔍 Get detailed book information
- ⏱️ Check your session status
- 👋 Logout when finished

Try asking: "Find me some science fiction books" or "Convert 50 USD to EUR"
```

### Advanced Power Users

**Complex query workflow:**
```
User: "I'm a book dealer. Show me high-value fantasy books published after 2010, and calculate profit margins if I buy at $20 USD and sell at €25 EUR."
Assistant:
1. Authenticating as book_dealer...
   ✅ Professional session established!

2. Finding valuable fantasy books (2010+)...
   [Calls books_query with filters]
   Found 34 high-rated fantasy books published after 2010.

3. Converting currencies for profit analysis...
   [Calls exchange_convert: 20 USD → EUR]
   [Calls exchange_convert: 25 EUR → USD]
   
Analysis:
- Buy price: $20 USD = €17.04 EUR
- Sell price: €25 EUR = $29.35 USD  
- Profit margin: $9.35 USD (46.75% margin)

4. Session status: 58 minutes remaining for continued analysis.
```