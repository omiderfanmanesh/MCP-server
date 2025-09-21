# Changelog

All notable changes to this project will be documented in this file.

## [2.0.0] - 2025-09-21

### 🔐 Added - JWT Authentication System
- **JWT Token Generation**: Added `get_jwt_token` tool for creating secure tokens
- **Authentication Middleware**: All database and exchange operations now require valid JWT tokens
- **Token Validation**: Comprehensive JWT signature and expiration validation
- **User Context**: All authenticated responses include username information
- **Security Headers**: HS256 algorithm with proper token structure

### 🛡️ Security Features
- **Protected Operations**: `books_query` and `exchange_convert` require authentication
- **Token Expiration**: 1-hour token lifetime with expiration checking
- **Error Handling**: Clear authentication error messages and hints
- **User Identification**: Each token contains user_id and username claims

### 📚 Enhanced API
- **books_query**: Now requires `token` parameter for authentication
- **exchange_convert**: Now requires `token` parameter for authentication  
- **get_jwt_token**: New tool for generating JWT tokens (no auth required)
- **Response Format**: All authenticated responses include `authenticated_user` field

### 🔧 Configuration
- **JWT Secret**: Configurable secret key (default: demo-secret-key-123)
- **Token Expiry**: Configurable expiration time (default: 3600 seconds)
- **Environment Variables**: Support for JWT_SECRET and JWT_EXPIRY

### 📖 Documentation
- **README.md**: Complete rewrite with authentication focus
- **AUTHENTICATION.md**: Comprehensive authentication guide
- **EXAMPLES.md**: Updated with authentication examples
- **CURSOR-SETUP.md**: Updated integration instructions

### 🐳 Docker Support
- **Updated Configuration**: Docker setup now includes authentication
- **Environment Support**: Docker compose with environment variables
- **Container Integration**: Updated Cursor config for Docker deployment

### ⚠️ Breaking Changes
- **Authentication Required**: Books and currency tools now require JWT tokens
- **Response Format**: All authenticated responses include user context
- **Parameter Addition**: New `token` parameter required for protected operations

---

## [1.0.0] - 2025-09-20

### Added
- Initial release of Books MCP Server
- Books database tool with comprehensive filtering options
- Currency exchange tool with synthetic rates
- Official MCP Python SDK integration
- Docker support for containerized deployment
- Comprehensive documentation and examples
- GitHub CI/CD workflows
- MIT License

### Features
- **Books Query Tool**: Search by genre, author, year, title with pagination
- **Currency Exchange Tool**: Convert between major world currencies
- **MCP Protocol Compliance**: Full compatibility with MCP clients
- **Error Handling**: Robust error responses and validation
- **Data Processing**: Automatic XLSX to CSV conversion

### Technical Details
- Built with MCP Python SDK v1.14.1
- Python 3.12+ support
- Stdio transport for maximum compatibility
- Docker containerization
- Clean project structure and documentation

### Documentation
- Comprehensive README with setup instructions
- API documentation with detailed schemas
- Usage examples for multiple clients
- Contributing guidelines
- GitHub issue templates

### Infrastructure
- GitHub Actions CI pipeline
- Docker build automation
- Code quality checks
- Import and functionality tests