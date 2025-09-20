# 📚 Books MCP Server

[![MCP](ht## 📖 Documentation

- 📋3. **Install depende## 📖 Documentation

- 📋 **[Setup Guide](docs/SETUP.md)** - Complete IDE integration instructions
- 🔧 **[API Reference](docs/API.md)** - Detailed tool documentation  
- 💡 **[Usage Examples](docs/EXAMPLES.md)** - Real-world usage patterns
- 🔐 **[Authentication Guide](docs/AUTHENTICATION.md)** - Security and user management
- 🐳 **[Docker Deployment](docs/DOCKER.md)** - Containerized deployment guide**
   ```bash
   pip install -r requirements.txt
   ```

## 🐳 Docker Deployment

### Quick Start with Docker

1. **Install Docker** (if not already installed)
   - [Docker Desktop](https://www.docker.com/products/docker-desktop/) for Mac/Windows
   - Docker Engine for Linux

2. **Build and run**
   ```bash
   # Quick setup
   ./scripts/docker-setup.sh
   
   # Start server (no authentication)
   docker-compose up mcp-server
   
   # Start with authentication
   docker-compose up mcp-server-auth
   ```

3. **Create users** (for authenticated version)
   ```bash
   # Create admin user
   ./scripts/manage-users.sh create-admin
   
   # Create regular user
   ./scripts/manage-users.sh create-user john john@example.com
   ```

### Docker Configuration Options

- **No Authentication**: `docker-compose up mcp-server`
- **Full Authentication**: `docker-compose up mcp-server-auth`  
- **Partial Protection**: `docker-compose up mcp-server-partial`

**📖 Complete Docker guide**: [docs/DOCKER.md](docs/DOCKER.md)Setup Guide](docs/SETUP.md)** - Complete IDE integration instructions
- 🔧 **[API Reference](docs/API.md)** - Detailed tool documentation  
- 💡 **[Usage Examples](docs/EXAMPLES.md)** - Real-world usage patterns
- 🔐 **[Authentication Guide](docs/AUTHENTICATION.md)** - Security and user management/img.shields.io/badge/Model%20Context%20Protocol-v1.0-blue)](https://modelcontextprotocol.io/)
[![Python](https://img.shields.io/badge/Python-3.12+-green)](https://python.org)
[![License](https://img.shields.io/badge/License-MIT-yellow)](LICENSE)

A powerful **Model Context Protocol (MCP) server** that provides seamless access to a comprehensive books dataset and real-time currency exchange functionality. Built with the official MCP Python SDK for enterprise-grade reliability and performance.

## ✨ Features

### 📖 Books Database
- **Advanced Search**: Filter by genre, author, publication year, and title
- **Comprehensive Dataset**: Thousands of books with detailed metadata
- **Smart Pagination**: Efficient browsing with limit and offset controls
- **Instant Lookup**: Retrieve specific books by unique ID

### 💱 Currency Exchange
- **Real-time Conversion**: Convert between major world currencies
- **Synthetic Rates**: Reliable exchange rate calculations
- **Global Coverage**: Support for USD, EUR, GBP, JPY, CAD, and more

### 🔐 Authentication & Security
- **API Key Authentication**: Secure access with pre-generated keys
- **JWT Token Support**: Session-based authentication with expiring tokens
- **Role-based Access Control**: Admin and user roles with fine-grained permissions
- **Secure Storage**: Hashed API keys and constant-time comparisons

### 🔧 Technical Excellence
- **Official MCP SDK**: Built on the robust Model Context Protocol specification
- **Docker Ready**: Containerized deployment for any environment
- **Zero Dependencies**: Minimal external requirements for maximum compatibility
- **Production Tested**: Stable, timeout-resistant architecture

## � Documentation

- 📋 **[Setup Guide](docs/SETUP.md)** - Complete IDE integration instructions
- 🔧 **[API Reference](docs/API.md)** - Detailed tool documentation  
- 💡 **[Usage Examples](docs/EXAMPLES.md)** - Real-world usage patterns

## �🚀 Quick Start

### Prerequisites
- Python 3.12+
- Docker (optional)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/omiderfanmanesh/MCP-server.git
   cd MCP-server
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the server**
   ```bash
   python -m mcp_server.server
   ```

### Docker Deployment

```bash
# Build the image
docker build -t books-mcp-server .

# Run the container
docker run -i books-mcp-server
```

## 🔧 Cursor IDE Integration

### Quick Setup

1. **Open Cursor Settings**
   - Press `Cmd + ,` (Mac) or `Ctrl + ,` (Windows/Linux)
   - Search for "MCP" or go to Features → Model Context Protocol

2. **Add Server Configuration**
   ```json
   {
     "mcpServers": {
       "jwt-books-server": {
         "command": "/opt/anaconda3/bin/python",
         "args": ["-m", "mcp_server.server"],
         "cwd": "/Users/omiderfanmanesh/Projects/MCP-server",
         "env": {
           "PYTHONUNBUFFERED": "1",
           "PYTHONIOENCODING": "utf-8"
         }
       }
     }
   }
   ```
   
   **⚠️ Important**: Replace the `cwd` path with your actual project directory!

3. **Restart Cursor** and test with:
   - *"Generate a JWT token for username 'test_user'"*
   - *"Search for books by genre 'Fiction'"*

**📖 Complete setup guide**: [CURSOR-SETUP.md](CURSOR-SETUP.md)

### Alternative: Docker Integration (if you have Docker)

If you prefer using Docker with Cursor:

```json
{
  "mcpServers": {
    "jwt-books-docker": {
      "command": "docker",
      "args": ["run", "--rm", "-i", "mcp-books-server"],
      "cwd": "/Users/omiderfanmanesh/Projects/MCP-server"
    }
  }
}
```

First build the image: `docker build -t mcp-books-server .`
       "books-mcp-server": {
         "command": "docker",
         "args": ["run", "-i", "--rm", "books-mcp-server"],
         "cwd": "/Users/omiderfanmanesh/Projects/MCP-server"
       }
     }
   }
   ```

3. **Restart Application**: Close and reopen Claude Desktop

### Environment-Specific Setup

**Docker (Recommended)**:
```json
{
  "mcpServers": {
    "books-mcp": {
      "command": "docker",
      "args": ["run", "-i", "--rm", "books-mcp-server"],
      "cwd": "/Users/omiderfanmanesh/Projects/MCP-server"
    }
  }
}
```

**Local Python (Alternative)**:
```json
{
  "mcpServers": {
    "books-mcp": {
      "command": "python",
      "args": ["-m", "mcp_server.server"],
      "cwd": "/path/to/MCP-server"
    }
  }
}
```

## 🎯 Usage Examples

### Interactive Examples

**Search for books:**
```
"Find science fiction books from the 2020s"
"Show me books by Isaac Asimov"
"List the top 10 fantasy novels"
```

**Currency conversion:**
```
"Convert 100 USD to EUR"
"What's 50 GBP in Japanese Yen?"
"How much is 200 CAD in USD?"
```

## 🛠 API Reference

### Tools Available

#### `books_query`
Query the books database with flexible filtering options.

**Parameters:**
- `id` (optional): Specific book ID
- `genre` (optional): Filter by genre
- `year` (optional): Publication year
- `author` (optional): Author name
- `title` (optional): Title search (contains)
- `limit` (optional): Maximum results (default: 10)
- `offset` (optional): Pagination offset

**Example:**
```json
{
  "genre": "Science Fiction",
  "year": "2020",
  "limit": 5
}
```

#### `exchange_convert`
Convert amounts between different currencies.

**Parameters:**
- `from_currency` (required): Source currency code
- `to_currency` (required): Target currency code
- `amount` (required): Amount to convert

**Example:**
```json
{
  "from_currency": "USD",
  "to_currency": "EUR", 
  "amount": 100.0
}
```

## 📁 Project Structure

```
MCP-server/
├── 📄 README.md              # This file
├── 📄 requirements.txt       # Python dependencies
├── 🐳 Dockerfile            # Container configuration
├── 📁 mcp_server/           # Main server package
│   ├── 🐍 server.py         # MCP server implementation
│   ├── 📚 books.py          # Books database interface
│   ├── 💱 exchange.py       # Currency exchange logic
│   └── 📁 util/            # Utility functions
│       └── 🔧 xlsx_to_csv.py # Data processing
├── 📁 sample-data/          # Sample dataset
│   └── 📊 BooksDatasetClean.xlsx
├── 📁 data/                 # Generated data files
│   └── 📄 books.csv         # Processed dataset
└── 📁 examples/             # Configuration examples
    └── ⚙️ mcp-server-config.json
```

## 🔧 Development

### Local Development Setup

1. **Clone and setup**
   ```bash
   git clone https://github.com/omiderfanmanesh/MCP-server.git
   cd MCP-server
   pip install -r requirements.txt
   ```

2. **Test the server**
   ```bash
   python -m mcp_server.server
   ```

3. **Data Processing**
   The server automatically converts the Excel dataset to CSV format on first run.

### Environment Variables

- `PYTHONUNBUFFERED=1`: Ensures real-time output
- `PYTHONIOENCODING=utf-8`: Handles international characters

### Debugging

Check server logs for troubleshooting:
- MCP clients typically log to application-specific directories
- Use `--verbose` or debug mode in your MCP client

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request. For major changes, please open an issue first to discuss what you would like to change.

### Development Guidelines

1. Follow PEP 8 style guidelines
2. Add tests for new features
3. Update documentation as needed
4. Ensure Docker builds successfully

## 📊 Dataset Information

The included sample dataset contains:
- **Format**: Excel/CSV with structured book metadata
- **Fields**: Title, Author, Genre, Publication Year, and more
- **Size**: Thousands of entries for comprehensive testing
- **Source**: Curated collection of popular literature

## 🔒 Security & Privacy

- **No External APIs**: All processing happens locally
- **Data Privacy**: Your data never leaves your environment
- **Secure Communication**: Standard MCP protocol security
- **No Telemetry**: Zero tracking or data collection

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Built with the [Model Context Protocol](https://modelcontextprotocol.io/)
- Powered by the [MCP Python SDK](https://github.com/modelcontextprotocol/python-sdk)
- Sample data curated for educational and testing purposes

## 📞 Support

- 🐛 **Issues**: [GitHub Issues](https://github.com/omiderfanmanesh/MCP-server/issues)
- 💬 **Discussions**: [GitHub Discussions](https://github.com/omiderfanmanesh/MCP-server/discussions)
- 📚 **Documentation**: [MCP Specification](https://spec.modelcontextprotocol.io/)

---

<div align="center">

**[⭐ Star this repo](https://github.com/omiderfanmanesh/MCP-server)** if you find it useful!

Made with ❤️ for the MCP community

</div>



1. Build the image:**Run**

```bash- Install dependencies: `pip install mcp`

docker build -t books-mcp .- Start the MCP server over stdio:

```  - `python -m mcp_server.sdk_server`



2. Run with Docker:This server speaks MCP-ish methods over JSON-RPC with `Content-Length` framing. It is compatible with tools that expect:

```bash- `mcp/initialize`, `mcp/resources/list`, `mcp/resources/templates`, `mcp/resources/read`, `mcp/tools/list`, `mcp/tools/call`.

docker run --rm -i books-mcp

```If you just want to exercise functionality without an MCP client, see the test suite for direct invocation patterns.



### MCP Client Configuration**Docker**

- Build: `docker build -t books-mcp .`

Add to your MCP client configuration:- Run (interactive stdio): `docker run --rm -i -e MCP_LOG=debug -v "$PWD/data:/app/data" books-mcp`

  - The `-i` flag keeps STDIN open for MCP stdio.

```json  - Mounting `./data` persists the generated CSV outside the container.

{- Compose (optional): `docker compose run --rm mcp`

  "mcpServers": {

    "books-mcp": {**Use with MCP Clients (including Copilot/Cursor builds that support MCP)**

      "command": "docker",- Command (local Python): `python` with args `[-m, mcp_server.sdk_server]`

      "args": [- Command (Docker): `docker` with args `[run, --rm, -i, -v, <abs-path>/data:/app/data, books-mcp]`

        "run", "--rm", "-i",- Example client config snippet (common MCP shape):

        "--init",  - {

        "-e", "MCP_LOG=debug",    "mcpServers": {

        "-e", "PYTHONUNBUFFERED=1",      "books-mcp": {

        "-v", "/path/to/MCP-server/data:/app/data",        "command": "python",

        "books-mcp"        "args": ["-m", "mcp_server.server"],

      ]        "env": {}

    }      }

  }    }

}  }

```- Example using Docker instead of Python:

  - {

## Available Tools    "mcpServers": {

      "books-mcp": {

### books_query        "command": "docker",

Query the books database with optional filters:        "args": [

- `id`: Get a specific book by ID          "run", "--rm", "-i",

- `genre`: Filter by genre          "-v", "/absolute/path/to/project/data:/app/data",

- `year`: Filter by publication year            "books-mcp"

- `author`: Filter by author name        ]

- `title`: Filter by title (partial match)      }

- `limit`: Maximum number of results (default: 10)    }

- `offset`: Pagination offset (default: 0)  }



### exchange_convertAfter adding, restart your MCP client. It should discover tools:

Convert currency amounts:- `books_query` (filters by `genre/year/author/title`, pagination; `id` to fetch one)

- `from_currency`: Source currency code (e.g., "USD")- `exchange_convert` (`from_currency`, `to_currency`, `amount`)

- `to_currency`: Target currency code (e.g., "EUR")

- `amount`: Amount to convert**Quick Demo (No MCP client)**

- This server is designed to be used by MCP-aware clients. For manual testing, use Cursor/Copilot MCP integration or add a simple stdio JSON-RPC client.

## Project Structure

**Use with Postman (via HTTP proxy)**

```- Start the proxy (spawns the MCP server under the hood):

├── mcp_server/  - `python scripts/http_proxy.py`

│   ├── sdk_server.py      # Main MCP server implementation  - Opens `http://127.0.0.1:8080`.

│   ├── books.py           # Books database repository- In Postman:

│   ├── exchange.py        # Currency exchange functionality  - POST `http://127.0.0.1:8080/rpc` with JSON body `{ "method": "mcp/initialize", "params": {} }` (optional).

│   └── util/  - GET `http://127.0.0.1:8080/resources/list`.

│       └── xlsx_to_csv.py # XLSX to CSV conversion utility  - GET `http://127.0.0.1:8080/resources/read?uri=books%3A%2F%2Ffilter%3Fgenre%3DFantasy%26limit%3D3`

├── data/  - POST `http://127.0.0.1:8080/tools/call` with body `{ "name": "exchange.convert", "arguments": { "from": "USD", "to": "EUR", "amount": 100 } }`.

│   └── books.csv          # Books dataset  - GET `http://127.0.0.1:8080/tools/list`

├── assignment/  - GET `http://127.0.0.1:8080/resources/templates`

│   └── BooksDatasetClean.xlsx  # Original dataset

├── Dockerfile             # Docker container configuration

├── docker-compose.yml     # Docker Compose setup**Ask Copilot (when MCP-enabled)**

├── mcp_config_docker.json # MCP client configuration- “Using the books-mcp server, list 5 Fantasy books.”

└── requirements.txt       # Python dependencies- “Fetch the book with id 42 from the books MCP.”

```- “Filter books by author ‘Harper Lee’ and year 1960.”

- “Convert 100 USD to EUR using the exchange MCP tool.”

## Development

**Example Interactions (JSON-RPC)**

The server uses the official MCP Python SDK for robust protocol handling and automatic client compatibility.- Initialize:
  - Request: `{ "jsonrpc": "2.0", "id": 1, "method": "mcp/initialize", "params": {} }`
  - Response: protocol version, capabilities, server info.
- List resources:
  - Request: `{ "jsonrpc": "2.0", "id": 2, "method": "mcp/resources/list" }`
  - Response: `resources: [ { uri: "books://all" }, ... ]`.
- Read filtered books:
  - Request: `{ "jsonrpc": "2.0", "id": 3, "method": "mcp/resources/read", "params": { "uri": "books://filter?genre=Fantasy&limit=5" } }`
  - Response: `{ contents: [{ text: "{\"data\":[...],\"count\":5}" }] }`
- Exchange tool call:
  - Request: `{ "jsonrpc": "2.0", "id": 4, "method": "mcp/tools/call", "params": { "name": "exchange.convert", "arguments": { "from": "USD", "to": "EUR", "amount": 100 } } }`
  - Response: `{ result: { content: [{ text: "{\"from\":\"USD\",...}" }], isError: false } }`

**Design Choices**
- **No external deps:** A small XLSX parser converts the dataset to CSV, ensuring portability.
- **Resources + Tools:** Exposes both, so clients can either read resources or invoke a tool for the same functionality.
- **Filtering:** Implemented server-side with case-insensitive matching and simple pagination (`limit`, `offset`).

**Testing**
- Run tests:
  - `python -m unittest discover -s tests -p "test_*.py" -v`

**Notes & Trade-offs**
- Protocol surface is a pragmatic subset matching common MCP expectations. If you use a strict MCP client, minor differences in capability fields or protocol version names may require slight adjustments.
- The XLSX converter targets common cases (first sheet, shared strings). It is intentionally minimal.
