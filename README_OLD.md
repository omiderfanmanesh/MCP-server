# 🔐 Session-Based Authenticated MCP Server# 🔐 Authenticated JWT MCP Server# � Authenticated JWT MCP Server



A **Model Context Protocol (MCP) server** with **session-based authentication** that provides secure access to books database and currency conversion tools. **Designed specifically for AI assistants** to use authentication seamlessly.



![License](https://img.shields.io/badge/license-MIT-blue.svg)A **Model Context Protocol (MCP) server** with **JWT authentication** that provides secure access to books database and currency conversion tools. Perfect for demonstrating authenticated API interactions and testing JWT workflows.A **Model Context Protocol (MCP) server** with **JWT authentication** that provides secure access to books database and currency conversion tools. Perfect for demonstrating authenticated API interactions and testing JWT workflows.

![Python](https://img.shields.io/badge/python-3.12+-green.svg)

![MCP](https://img.shields.io/badge/MCP-1.0-orange.svg)

![Docker](https://img.shields.io/badge/docker-ready-blue.svg)

![License](https://img.shields.io/badge/license-MIT-blue.svg)![License](https://img.shields.io/badge/license-MIT-blue.svg)

## ✨ Features

![Python](https://img.shields.io/badge/python-3.12+-green.svg)![Python](https://img.shields.io/badge/python-3.12+-green.svg)

### 🔐 **Session-Based Authentication**

- Simple authentication with username![MCP](https://img.shields.io/badge/MCP-1.0-orange.svg)![MCP](https://img.shields.io/badge/MCP-1.0-orange.svg)

- Automatic session management

- 1-hour session expiration![Docker](https://img.shields.io/badge/docker-ready-blue.svg)![Docker](https://img.shields.io/badge/docker-ready-blue.svg)

- No token parameters required in tool calls



### 📚 **Books Database**

- Search books by title, author, genre, year## ✨ Features## ✨ Features

- Paginated results with limit/offset

- Individual book lookup by ID

- Protected by session authentication

### 🔑 **JWT Authentication System**### � **JWT Authentication System**

### 💱 **Currency Exchange**

- Convert between multiple currencies- Generate JWT tokens for users- Generate JWT tokens for users

- Real-time synthetic exchange rates

- Support for major world currencies- Secure HS256 signature algorithm- Secure HS256 signature algorithm

- Session authentication required

- 1-hour token expiration- 1-hour token expiration

### 🤖 **AI Assistant Friendly**

- No complex token passing required- Comprehensive token validation- Comprehensive token validation

- Simple authenticate-then-use workflow

- Clear error messages for unauthenticated requests

- Session status checking

### 📚 **Books Database**### 📚 **Books Database**

## 🚀 Quick Start

- Search books by title, author, genre, year- Search books by title, author, genre, year

### Prerequisites

- Python 3.12+- Paginated results with limit/offset- Paginated results with limit/offset

- Docker (optional)

- VS Code with Cursor or Claude- Individual book lookup by ID- Individual book lookup by ID



### 📦 Installation- Protected by JWT authentication- Protected by JWT authentication



**Option 1: Local Python**

```bash

git clone https://github.com/omiderfanmanesh/MCP-server.git### 💱 **Currency Exchange**### 💱 **Currency Exchange**

cd MCP-server

pip install -r requirements.txt- Convert between multiple currencies- Convert between multiple currencies

python -m mcp_server.server

```- Real-time synthetic exchange rates- Real-time synthetic exchange rates



**Option 2: Docker**- Support for major world currencies- Support for major world currencies

```bash

git clone https://github.com/omiderfanmanesh/MCP-server.git- Authenticated access required- Authenticated access required

cd MCP-server

docker compose up -d

```

### 🛡️ **Security Features**### 🛡️ **Security Features**

### 🔧 Cursor Integration

- All database and exchange operations require valid JWT tokens- All database and exchange operations require valid JWT tokens

Add to your Cursor settings.json:

- Token signature verification- Token signature verification

**For Local Python:**

```json- Expiration time validation- Expiration time validation

{

  "mcpServers": {- User context in all responses- User context in all responses

    "session-auth-server": {

      "command": "/opt/anaconda3/bin/python",

      "args": ["-m", "mcp_server.server"],

      "cwd": "/path/to/MCP-server"## 🚀 Quick Start## 🚀 Quick Start

    }

  }

}

```### Prerequisites### Prerequisites



**For Docker:**- Python 3.12+- Python 3.12+

```json

{- Docker (optional)- Docker (optional)

  "mcpServers": {

    "session-auth-server": {- VS Code with Cursor or Claude- VS Code with Cursor or Claude

      "command": "docker",

      "args": ["exec", "-i", "mcp-books-server", "python", "-m", "mcp_server.server"],

      "cwd": "/path/to/MCP-server"

    }### 📦 Installation### 📦 Installation

  }

}

```

**Option 1: Local Python****Option 1: Local Python**

## 🎯 Usage Examples

```bash```bash

### 1. **Authenticate and Create Session**

```git clone https://github.com/omiderfanmanesh/MCP-server.gitgit clone https://github.com/omiderfanmanesh/MCP-server.git

"Authenticate as user 'alice'"

```cd MCP-servercd MCP-server



**Response:**pip install -r requirements.txtpip install -r requirements.txt

```json

{python -m mcp_server.serverpython -m mcp_server.server

  "success": true,

  "message": "Successfully authenticated as alice",``````

  "username": "alice",

  "user_id": "user_5484",

  "session_id": "session_99681",

  "expires_in": 3600**Option 2: Docker****Option 2: Docker**

}

``````bash```bash



### 2. **Check Session Status**git clone https://github.com/omiderfanmanesh/MCP-server.gitgit clone https://github.com/omiderfanmanesh/MCP-server.git

```

"Check my session status"cd MCP-servercd MCP-server

```

docker compose up -ddocker compose up -d

**Response:**

```json``````

{

  "authenticated": true,

  "username": "alice",

  "user_id": "user_5484",### 🔧 Cursor Integration### 🔧 Cursor Integration

  "session_age": 0,

  "expires_in": 3600

}

```Add to your Cursor settings.json:Add to your Cursor settings.json:



### 3. **Search Books** (Requires Active Session)

```

"Search for programming books"**For Local Python:****For Local Python:**

```

```json```json

**Response:**

```json{{

{

  "authenticated_user": "alice",  "mcpServers": {  "mcpServers": {

  "data": [

    {    "jwt-books-server": {    "jwt-books-server": {

      "id": "123",

      "title": "Clean Code",      "command": "/opt/anaconda3/bin/python",      "command": "/opt/anaconda3/bin/python",

      "author": "Robert Martin",

      "genre": "Programming",      "args": ["-m", "mcp_server.server"],      "args": ["-m", "mcp_server.server"],

      "year": "2008"

    }      "cwd": "/path/to/MCP-server"      "cwd": "/path/to/MCP-server"

  ],

  "count": 1    }    }

}

```  }  }



### 4. **Convert Currency** (Requires Active Session)}}

```

"Convert 100 USD to EUR"``````

```



**Response:**

```json**For Docker:****For Docker:**

{

  "authenticated_user": "alice",```json```json

  "from": "USD",

  "to": "EUR",{{

  "amount": 100.0,

  "converted": 92.0  "mcpServers": {  "mcpServers": {

}

```    "jwt-books-server": {    "jwt-books-server": {



### 5. **Unauthenticated Request** (Shows Error)      "command": "docker",      "command": "docker",

```

"Search for books about python"      "args": ["exec", "-i", "mcp-books-server", "python", "-m", "mcp_server.server"],      "args": ["exec", "-i", "mcp-books-server", "python", "-m", "mcp_server.server"],

```

      "cwd": "/path/to/MCP-server"      "cwd": "/path/to/MCP-server"

**Response:**

```json    }    }

{

  "error": "authentication_required",  }  }

  "message": "No active session. Please authenticate first using the 'authenticate' tool.",

  "hint": "Call authenticate tool with your username to create a session"}}

}

`````````



### 6. **Logout**

```

"Logout"## 🎯 Usage Examples**📖 Complete Docker guide**: [docs/DOCKER.md](docs/DOCKER.md)Setup Guide](docs/SETUP.md)** - Complete IDE integration instructions

```

- 🔧 **[API Reference](docs/API.md)** - Detailed tool documentation  

**Response:**

```json### 1. **Generate JWT Token** (No Authentication Required)- 💡 **[Usage Examples](docs/EXAMPLES.md)** - Real-world usage patterns

{

  "success": true,```- 🔐 **[Authentication Guide](docs/AUTHENTICATION.md)** - Security and user management/img.shields.io/badge/Model%20Context%20Protocol-v1.0-blue)](https://modelcontextprotocol.io/)

  "message": "Successfully logged out alice"

}"Generate a JWT token for user 'alice'"[![Python](https://img.shields.io/badge/Python-3.12+-green)](https://python.org)

```

```[![License](https://img.shields.io/badge/License-MIT-yellow)](LICENSE)

## 🔐 Authentication Flow



```mermaid

sequenceDiagram**Response:**A powerful **Model Context Protocol (MCP) server** that provides seamless access to a comprehensive books dataset and real-time currency exchange functionality. Built with the official MCP Python SDK for enterprise-grade reliability and performance.

    participant AI as AI Assistant

    participant MCP as MCP Server```json

    

    AI->>MCP: authenticate(username: "alice"){## ✨ Features

    MCP->>MCP: Create Session

    MCP->>AI: Session Created Successfully  "token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",

    

    AI->>MCP: books_query(title: "python")  "user_id": "user_1234",### 📖 Books Database

    MCP->>MCP: Check Active Session

    MCP->>AI: Authenticated Response + Books Data  "username": "alice",- **Advanced Search**: Filter by genre, author, publication year, and title

    

    AI->>MCP: books_query(title: "python") [No Session]  "expires_in": 3600,- **Comprehensive Dataset**: Thousands of books with detailed metadata

    MCP->>AI: Error: authentication_required

      "token_type": "Bearer",- **Smart Pagination**: Efficient browsing with limit and offset controls

    AI->>MCP: logout()

    MCP->>MCP: Destroy Session  "message": "Token generated successfully!"- **Instant Lookup**: Retrieve specific books by unique ID

    MCP->>AI: Successfully Logged Out

```}



## 🛠️ API Reference```### 💱 Currency Exchange



### Available Tools- **Real-time Conversion**: Convert between major world currencies



| Tool | Authentication | Description |### 2. **Search Books** (Authentication Required)- **Synthetic Rates**: Reliable exchange rate calculations

|------|----------------|-------------|

| `authenticate` | ❌ None | Create user session |```- **Global Coverage**: Support for USD, EUR, GBP, JPY, CAD, and more

| `session_status` | ❌ None | Check current authentication status |

| `logout` | ❌ None | End current session |"Search for programming books with token: [your-jwt-token]"

| `books_query` | ✅ Required | Search and filter books database |

| `exchange_convert` | ✅ Required | Convert between currencies |```### 🔐 Authentication & Security



### Tool Parameters- **API Key Authentication**: Secure access with pre-generated keys



**`authenticate`****Response:**- **JWT Token Support**: Session-based authentication with expiring tokens

- `username` (string, required): Username for the session

```json- **Role-based Access Control**: Admin and user roles with fine-grained permissions

**`session_status`**

- No parameters required{- **Secure Storage**: Hashed API keys and constant-time comparisons



**`logout`**  "authenticated_user": "alice",

- No parameters required

  "data": [### 🔧 Technical Excellence

**`books_query`** 

- `id` (string, optional): Specific book ID    {- **Official MCP SDK**: Built on the robust Model Context Protocol specification

- `title` (string, optional): Filter by title (contains)

- `author` (string, optional): Filter by author name      "id": "123",- **Docker Ready**: Containerized deployment for any environment

- `genre` (string, optional): Filter by genre

- `year` (string, optional): Filter by publication year      "title": "Clean Code",- **Zero Dependencies**: Minimal external requirements for maximum compatibility

- `limit` (integer, optional): Maximum results (default: 10)

- `offset` (integer, optional): Pagination offset      "author": "Robert Martin",- **Production Tested**: Stable, timeout-resistant architecture



**`exchange_convert`**      "genre": "Programming",

- `from_currency` (string, required): Source currency code

- `to_currency` (string, required): Target currency code        "year": "2008"## � Documentation

- `amount` (number, required): Amount to convert

    }

## 🧪 Testing

  ],- 📋 **[Setup Guide](docs/SETUP.md)** - Complete IDE integration instructions

### Integration Testing Workflow

```  "count": 1- 🔧 **[API Reference](docs/API.md)** - Detailed tool documentation  

1. "Check session status" → Should show not authenticated

2. "Authenticate as user 'testuser'" → Should create session}- 💡 **[Usage Examples](docs/EXAMPLES.md)** - Real-world usage patterns

3. "Check session status" → Should show authenticated

4. "Search for python books" → Should work and show authenticated_user```

5. "Convert 100 USD to EUR" → Should work and show authenticated_user

6. "Logout" → Should end session## �🚀 Quick Start

7. "Search for books" → Should fail with authentication_required

```### 3. **Convert Currency** (Authentication Required)



## 🐳 Docker Support```### Prerequisites



The project includes full Docker support:"Convert 100 USD to EUR with token: [your-jwt-token]"- Python 3.12+



**Build and Run:**```- Docker (optional)

```bash

docker compose up -d

```

**Response:**### Installation

**Check Logs:**

```bash```json

docker compose logs -f

```{1. **Clone the repository**



**Stop:**  "authenticated_user": "alice",   ```bash

```bash

docker compose down  "from": "USD",   git clone https://github.com/omiderfanmanesh/MCP-server.git

```

  "to": "EUR",   cd MCP-server

## 📁 Project Structure

  "amount": 100.0,   ```

```

MCP-server/  "converted": 85.2

├── mcp_server/

│   ├── __init__.py}2. **Install dependencies**

│   ├── server.py          # Main MCP server with session auth

│   ├── books.py           # Books repository```   ```bash

│   ├── exchange.py        # Currency exchange rates

│   └── util/   pip install -r requirements.txt

│       └── xlsx_to_csv.py # Data conversion utility

├── data/### 4. **Unauthenticated Request** (Shows Error)   ```

│   └── books.csv          # Generated books database

├── sample-data/```

│   └── BooksDatasetClean.xlsx

├── docs/"Search for books about python"3. **Run the server**

│   ├── API.md

│   ├── EXAMPLES.md```   ```bash

│   └── SETUP.md

├── examples/   python -m mcp_server.server

│   └── mcp-server-config.json

├── Dockerfile**Response:**   ```

├── docker-compose.yml

├── requirements.txt```json

└── README.md

```{### Docker Deployment



## 🔧 Configuration  "error": "authentication_required",



### Session Management  "message": "JWT token is required. Generate one using get_jwt_token first.",```bash

- **Session Duration**: 1 hour (3600 seconds)

- **Storage**: In-memory (for production, use Redis or database)  "hint": "Include 'token' parameter with your JWT token"# Build the image

- **Cleanup**: Automatic expiration checking

}docker build -t books-mcp-server .

### Security Notes

- Sessions are stored in memory and reset on server restart```

- For production, implement persistent session storage

- Consider adding rate limiting for authentication attempts# Run the container

- Use HTTPS in production environments

## 🔐 Authentication Flowdocker run -i books-mcp-server

## 🆚 Why Session-Based vs Token-Based?

```

### Session-Based (Current Implementation)

✅ **AI Assistant Friendly**: No token parameters to pass  ```mermaid

✅ **Simple Workflow**: Authenticate once, use many tools  

✅ **Clear State**: Easy to check authentication status  sequenceDiagram## 🔧 Cursor IDE Integration

✅ **No Token Management**: No copying/pasting tokens  

    participant Client

### Token-Based (Previous Implementation)

❌ **AI Assistant Unfriendly**: Required token in every call      participant MCP Server### Quick Setup

❌ **Complex Workflow**: Generate token, then pass to every tool  

❌ **Token Management**: Manual token handling required      

❌ **Interface Issues**: Token parameters not accessible to AI  

    Client->>MCP Server: get_jwt_token(username: "alice")1. **Open Cursor Settings**

## 🤝 Contributing

    MCP Server->>Client: JWT Token + User Info   - Press `Cmd + ,` (Mac) or `Ctrl + ,` (Windows/Linux)

1. Fork the repository

2. Create a feature branch (`git checkout -b feature/amazing-feature`)       - Search for "MCP" or go to Features → Model Context Protocol

3. Commit your changes (`git commit -m 'Add amazing feature'`)

4. Push to the branch (`git push origin feature/amazing-feature`)    Client->>MCP Server: books_query(token: "jwt_token", title: "python")

5. Open a Pull Request

    MCP Server->>MCP Server: Validate JWT Token2. **Add Server Configuration**

## 📄 License

    MCP Server->>Client: Authenticated Response + Books Data   ```json

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

       {

## 🙏 Acknowledgments

    Client->>MCP Server: books_query(title: "python") [No Token]     "mcpServers": {

- [Model Context Protocol](https://modelcontextprotocol.io/) for the framework

- [Anthropic](https://www.anthropic.com/) for MCP development    MCP Server->>Client: Error: authentication_required       "jwt-books-server": {

- The AI community for feedback on authentication usability

```         "command": "/opt/anaconda3/bin/python",

## 📞 Support

         "args": ["-m", "mcp_server.server"],

- 🐛 [Report Issues](https://github.com/omiderfanmanesh/MCP-server/issues)

- 💬 [Discussions](https://github.com/omiderfanmanesh/MCP-server/discussions)## 🛠️ API Reference         "cwd": "/Users/omiderfanmanesh/Projects/MCP-server",

- 📧 Contact: [your-email@example.com]

         "env": {

---

### Available Tools           "PYTHONUNBUFFERED": "1",

**⭐ Star this repo if it helped you build better MCP servers!**
           "PYTHONIOENCODING": "utf-8"

| Tool | Authentication | Description |         }

|------|----------------|-------------|       }

| `get_jwt_token` | ❌ None | Generate JWT tokens for users |     }

| `books_query` | ✅ Required | Search and filter books database |   }

| `exchange_convert` | ✅ Required | Convert between currencies |   ```

   

### Tool Parameters   **⚠️ Important**: Replace the `cwd` path with your actual project directory!



**`get_jwt_token`**3. **Restart Cursor** and test with:

- `username` (string, required): Username for the token   - *"Generate a JWT token for username 'test_user'"*

   - *"Search for books by genre 'Fiction'"*

**`books_query`** 

- `token` (string, required): Valid JWT token**📖 Complete setup guide**: [CURSOR-SETUP.md](CURSOR-SETUP.md)

- `id` (string, optional): Specific book ID

- `title` (string, optional): Filter by title (contains)### Alternative: Docker Integration (if you have Docker)

- `author` (string, optional): Filter by author name

- `genre` (string, optional): Filter by genreIf you prefer using Docker with Cursor:

- `year` (string, optional): Filter by publication year

- `limit` (integer, optional): Maximum results (default: 10)```json

- `offset` (integer, optional): Pagination offset{

  "mcpServers": {

**`exchange_convert`**    "jwt-books-docker": {

- `token` (string, required): Valid JWT token      "command": "docker",

- `from_currency` (string, required): Source currency code      "args": ["run", "--rm", "-i", "mcp-books-server"],

- `to_currency` (string, required): Target currency code        "cwd": "/Users/omiderfanmanesh/Projects/MCP-server"

- `amount` (number, required): Amount to convert    }

  }

## 🧪 Testing}

```

### Manual Testing

```bashFirst build the image: `docker build -t mcp-books-server .`

# Test JWT creation and validation       "books-mcp-server": {

python -c "         "command": "docker",

from mcp_server.server import create_jwt_token, validate_jwt_token         "args": ["run", "-i", "--rm", "books-mcp-server"],

token = create_jwt_token('test123', 'testuser')         "cwd": "/Users/omiderfanmanesh/Projects/MCP-server"

print('Token:', token)       }

payload = validate_jwt_token(token)     }

print('Valid:', payload is not None)   }

"   ```

```

3. **Restart Application**: Close and reopen Claude Desktop

### Integration Testing

Use the provided Cursor integration to test:### Environment-Specific Setup

1. Generate tokens without authentication

2. Try protected operations without tokens (should fail)**Docker (Recommended)**:

3. Use valid tokens for protected operations (should succeed)```json

4. Test with expired tokens (should fail){

  "mcpServers": {

## 🐳 Docker Support    "books-mcp": {

      "command": "docker",

The project includes full Docker support:      "args": ["run", "-i", "--rm", "books-mcp-server"],

      "cwd": "/Users/omiderfanmanesh/Projects/MCP-server"

**Build and Run:**    }

```bash  }

docker compose up -d}

``````



**Check Logs:****Local Python (Alternative)**:

```bash```json

docker compose logs -f{

```  "mcpServers": {

    "books-mcp": {

**Stop:**      "command": "python",

```bash      "args": ["-m", "mcp_server.server"],

docker compose down      "cwd": "/path/to/MCP-server"

```    }

  }

## 📁 Project Structure}

```

```

MCP-server/## 🎯 Usage Examples

├── mcp_server/

│   ├── __init__.py### Interactive Examples

│   ├── server.py          # Main MCP server with JWT auth

│   ├── books.py           # Books repository**Search for books:**

│   ├── exchange.py        # Currency exchange rates```

│   └── util/"Find science fiction books from the 2020s"

│       └── xlsx_to_csv.py # Data conversion utility"Show me books by Isaac Asimov"

├── data/"List the top 10 fantasy novels"

│   └── books.csv          # Generated books database```

├── sample-data/

│   └── BooksDatasetClean.xlsx**Currency conversion:**

├── docs/```

│   ├── API.md"Convert 100 USD to EUR"

│   ├── EXAMPLES.md"What's 50 GBP in Japanese Yen?"

│   └── SETUP.md"How much is 200 CAD in USD?"

├── examples/```

│   └── mcp-server-config.json

├── Dockerfile## 🛠 API Reference

├── docker-compose.yml

├── requirements.txt### Tools Available

└── README.md

```#### `books_query`

Query the books database with flexible filtering options.

## 🔧 Configuration

**Parameters:**

### Environment Variables- `id` (optional): Specific book ID

- `JWT_SECRET`: Custom JWT secret key (default: `demo-secret-key-123`)- `genre` (optional): Filter by genre

- `JWT_EXPIRY`: Token expiry in seconds (default: `3600`)- `year` (optional): Publication year

- `author` (optional): Author name

### Security Notes- `title` (optional): Title search (contains)

- Default secret key is for **demonstration only**- `limit` (optional): Maximum results (default: 10)

- Use strong, unique secrets in production- `offset` (optional): Pagination offset

- Store secrets in environment variables

- Use HTTPS for token transmission**Example:**

- Implement proper token storage on client side```json

{

## 🤝 Contributing  "genre": "Science Fiction",

  "year": "2020",

1. Fork the repository  "limit": 5

2. Create a feature branch (`git checkout -b feature/amazing-feature`)}

3. Commit your changes (`git commit -m 'Add amazing feature'`)```

4. Push to the branch (`git push origin feature/amazing-feature`)

5. Open a Pull Request#### `exchange_convert`

Convert amounts between different currencies.

## 📄 License

**Parameters:**

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.- `from_currency` (required): Source currency code

- `to_currency` (required): Target currency code

## 🙏 Acknowledgments- `amount` (required): Amount to convert



- [Model Context Protocol](https://modelcontextprotocol.io/) for the framework**Example:**

- [Anthropic](https://www.anthropic.com/) for MCP development```json

- JWT.io for JWT debugging tools{

  "from_currency": "USD",

## 📞 Support  "to_currency": "EUR", 

  "amount": 100.0

- 🐛 [Report Issues](https://github.com/omiderfanmanesh/MCP-server/issues)}

- 💬 [Discussions](https://github.com/omiderfanmanesh/MCP-server/discussions)```

- 📧 Contact: [your-email@example.com]

## 📁 Project Structure

---

```

**⭐ Star this repo if it helped you!**MCP-server/
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
