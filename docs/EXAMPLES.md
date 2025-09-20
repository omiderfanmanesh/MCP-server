# 💡 Usage Examples

This document provides comprehensive examples of using the Books MCP Server with various MCP clients and development environments.

## 🎯 Cursor IDE Examples

### Quick Setup Verification

Once you've added the MCP server to Cursor, test with:
```
"Test the books database connection"
```
Expected: Server connects and shows available tools.

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

## 🤖 GitHub Copilot / Claude Desktop Examples

## 🤖 GitHub Copilot / Claude Desktop Examples

### Configuration Testing
```
"Can you access the books database? Show me what tools are available."
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
```
User: I have 500 GBP, how much is that in Japanese Yen?
Response: Converting 500 GBP to JPY...
Result: 500.00 GBP = 74,250.00 JPY
```

## Claude Desktop Examples

### Natural Language Queries

**Book recommendations:**
```
User: I love fantasy novels. Can you recommend some good ones?
Assistant: I'll search our books database for fantasy novels...
[Uses books_query with genre="Fantasy"]
```

**Research assistance:**
```
User: I'm writing a paper on 1950s science fiction. What books from that era are available?
Assistant: Let me find science fiction books from the 1950s...
[Uses books_query with genre="Science Fiction" and year filter]
```

### Complex Workflows

**Planning a book purchase:**
```
User: I want to buy books by Isaac Asimov. The price is $15 USD each. How much would 3 books cost in EUR?
Assistant: 
1. First, let me find Isaac Asimov books...
   [Uses books_query with author="Isaac Asimov"]
2. Now I'll convert $45 USD to EUR...
   [Uses exchange_convert with 45 USD to EUR]
Result: 3 books at $15 each = $45 USD = €38.35 EUR
```

## API Client Examples

### Python Client

```python
import asyncio
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

async def search_books():
    server_params = StdioServerParameters(
        command="python",
        args=["-m", "mcp_server.server"]
    )
    
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            
            # Search for science fiction books
            result = await session.call_tool(
                "books_query",
                {"genre": "Science Fiction", "limit": 5}
            )
            print(result.content[0].text)

asyncio.run(search_books())
```

### JavaScript Client

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

// Convert currency
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

console.log(result);
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

### Recommendation System

```
User: I liked "Dune". What similar books do you recommend?
Assistant:
1. Let me find books in the science fiction genre...
2. Here are some recommendations from our database...
3. If you're interested in purchasing, I can help with currency conversion for international stores.
```

### Research Workflow

```
User: I'm studying literature from the 1960s. Help me find relevant books and calculate research budget costs.
Assistant:
1. Searching for books from the 1960s...
2. Found X books across various genres
3. Estimating costs in your local currency...
```