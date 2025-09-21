# Session-Based Authenticated MCP Server Architecture

This document provides comprehensive architectural diagrams and technical details for the Session-Based Authenticated Model Context Protocol (MCP) Server.

## Table of Contents

1. [System Overview](#system-overview)
2. [Authentication Flow](#authentication-flow)
3. [Session Management](#session-management)
4. [Tool Call Processing](#tool-call-processing)
5. [Data Flow Architecture](#data-flow-architecture)
6. [Component Relationships](#component-relationships)
7. [Security Model](#security-model)
8. [Deployment Architecture](#deployment-architecture)

---

## System Overview

The MCP Server implements a session-based authentication system specifically designed for AI assistants and automated tools. The architecture addresses the limitation where AI assistants cannot pass authentication tokens as parameters to individual tool calls.

```mermaid
graph TB
    subgraph "AI Assistant"
        AI[AI Assistant/Copilot]
    end
    
    subgraph "MCP Communication Layer"
        MCPC[MCP Client]
        STDIO[stdio Transport]
    end
    
    subgraph "MCP Server Core"
        AUTH[Authentication Manager]
        SESSION[Session Store]
        TOOLS[Tool Dispatcher]
        VALIDATE[Session Validator]
    end
    
    subgraph "Protected Operations"
        BOOKS[Books Repository]
        EXCHANGE[Exchange Rates]
    end
    
    subgraph "Data Sources"
        CSV[Books CSV Data]
        RATES[Currency Rates]
    end
    
    AI <--> MCPC
    MCPC <--> STDIO
    STDIO <--> AUTH
    AUTH <--> SESSION
    AUTH <--> TOOLS
    TOOLS <--> VALIDATE
    VALIDATE <--> SESSION
    TOOLS <--> BOOKS
    TOOLS <--> EXCHANGE
    BOOKS <--> CSV
    EXCHANGE <--> RATES
    
    classDef ai fill:#e1f5fe
    classDef mcp fill:#f3e5f5
    classDef server fill:#e8f5e8
    classDef data fill:#fff3e0
    
    class AI ai
    class MCPC,STDIO mcp
    class AUTH,SESSION,TOOLS,VALIDATE server
    class CSV,RATES data
```

### Key Architecture Principles

- **Session-Based Authentication**: Global session state eliminates need for token parameters
- **AI Assistant Compatibility**: Designed specifically for AI tool usage patterns
- **Stateful Server Design**: Maintains session context across multiple tool calls
- **Security Through Expiration**: 1-hour session limits with automatic cleanup
- **Modular Component Design**: Separated concerns for authentication, data, and operations

---

## Authentication Flow

The authentication system uses JWT tokens for session management with a global session store for AI assistant compatibility.

```mermaid
sequenceDiagram
    participant AI as AI Assistant
    participant MCP as MCP Server
    participant AUTH as Auth Manager
    participant SESSION as Session Store
    participant JWT as JWT Handler
    
    Note over AI,JWT: Initial Authentication
    AI->>MCP: authenticate(username)
    MCP->>AUTH: Process authentication
    AUTH->>JWT: create_jwt_token(user_id, username)
    JWT-->>AUTH: JWT token (1hr expiration)
    AUTH->>SESSION: Store session data
    SESSION-->>AUTH: session_id
    AUTH->>MCP: Set _CURRENT_SESSION
    MCP-->>AI: {success: true, session_id, expires_in: 3600}
    
    Note over AI,JWT: Session Validation for Protected Operations
    AI->>MCP: books_query(title="python")
    MCP->>AUTH: Check _CURRENT_SESSION
    AUTH->>SESSION: Validate session exists
    SESSION-->>AUTH: Session data
    AUTH->>JWT: validate_jwt_token(token)
    JWT-->>AUTH: Token payload (if valid)
    
    alt Session Valid
        AUTH-->>MCP: Authentication OK
        MCP->>MCP: Execute books_query
        MCP-->>AI: {authenticated_user, data, count}
    else Session Expired
        AUTH->>SESSION: Delete expired session
        AUTH->>MCP: Clear _CURRENT_SESSION
        MCP-->>AI: {error: "session_expired"}
    else No Session
        MCP-->>AI: {error: "authentication_required"}
    end
```

### Authentication Components

1. **JWT Handler**: Creates and validates HS256-signed tokens with 1-hour expiration
2. **Session Store**: Global dictionary storing active sessions with metadata
3. **Current Session Tracker**: `_CURRENT_SESSION` global variable for active session
4. **Automatic Cleanup**: Expired sessions removed on next access attempt

---

## Session Management

The session management system maintains global state to enable seamless AI assistant interactions.

```mermaid
stateDiagram-v2
    [*] --> Unauthenticated
    
    Unauthenticated --> Authenticating: authenticate(username)
    Authenticating --> Authenticated: JWT created & session stored
    Authenticating --> Unauthenticated: Authentication failed
    
    Authenticated --> Using_Tools: Protected tool call
    Using_Tools --> Authenticated: Tool execution complete
    
    Authenticated --> Checking_Status: session_status()
    Checking_Status --> Authenticated: Status returned
    
    Authenticated --> Logging_Out: logout()
    Logging_Out --> Unauthenticated: Session cleaned up
    
    Authenticated --> Session_Expired: 1 hour timeout
    Session_Expired --> Unauthenticated: Auto cleanup
    
    Using_Tools --> Session_Expired: Timeout during operation
```

### Session Data Structure

```json
{
  "session_id": {
    "username": "alice",
    "user_id": "user_1234",
    "token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
    "created_at": 1640995200.0
  }
}
```

### Global Variables

- **`_USER_SESSIONS`**: Dictionary storing all active sessions
- **`_CURRENT_SESSION`**: String ID of currently active session
- **Session Expiration**: 3600 seconds (1 hour) from creation

---

## Tool Call Processing

The tool dispatcher handles both public and protected operations with session validation.

```mermaid
flowchart TD
    START([Tool Call Received]) --> CHECK_TYPE{Tool Type?}
    
    CHECK_TYPE -->|Session Management| SESSION_TOOLS[authenticate, logout, session_status]
    CHECK_TYPE -->|Protected Operation| PROTECTED_TOOLS[books_query, exchange_convert]
    CHECK_TYPE -->|Unknown| ERROR_UNKNOWN[Unknown Tool Error]
    
    SESSION_TOOLS --> EXECUTE_SESSION[Execute Session Operation]
    EXECUTE_SESSION --> RETURN_SESSION[Return Session Response]
    
    PROTECTED_TOOLS --> CHECK_SESSION{Active Session?}
    CHECK_SESSION -->|No| ERROR_AUTH[authentication_required]
    CHECK_SESSION -->|Yes| VALIDATE_EXPIRY{Session Expired?}
    
    VALIDATE_EXPIRY -->|Yes| CLEANUP[Clean Up Session]
    CLEANUP --> ERROR_EXPIRED[session_expired]
    
    VALIDATE_EXPIRY -->|No| EXECUTE_TOOL[Execute Protected Operation]
    EXECUTE_TOOL --> ADD_CONTEXT[Add User Context]
    ADD_CONTEXT --> RETURN_RESULT[Return Tool Result]
    
    ERROR_UNKNOWN --> END_ERROR([Error Response])
    ERROR_AUTH --> END_ERROR
    ERROR_EXPIRED --> END_ERROR
    RETURN_SESSION --> END_SUCCESS([Success Response])
    RETURN_RESULT --> END_SUCCESS
    
    classDef session fill:#e3f2fd
    classDef protected fill:#f1f8e9
    classDef error fill:#ffebee
    classDef success fill:#e8f5e8
    
    class SESSION_TOOLS,EXECUTE_SESSION,RETURN_SESSION session
    class PROTECTED_TOOLS,EXECUTE_TOOL,ADD_CONTEXT,RETURN_RESULT protected
    class ERROR_UNKNOWN,ERROR_AUTH,ERROR_EXPIRED,END_ERROR error
    class END_SUCCESS success
```

### Tool Categories

1. **Session Management Tools** (Public Access):
   - `authenticate`: Create new session
   - `session_status`: Check authentication state
   - `logout`: End current session

2. **Protected Operations** (Require Authentication):
   - `books_query`: Search book database
   - `exchange_convert`: Currency conversion

### Response Format

All responses include user context for audit trails:

```json
{
  "authenticated_user": "alice",
  "data": {...},
  "timestamp": 1640995200.0
}
```

---

## Data Flow Architecture

The data flow shows how information moves through the system from AI assistant requests to data sources.

```mermaid
graph LR
    subgraph "Request Flow"
        REQ[AI Request] --> PARSE[Parse Tool Call]
        PARSE --> AUTH[Authentication Check]
        AUTH --> VALIDATE[Session Validation]
        VALIDATE --> EXEC[Execute Operation]
    end
    
    subgraph "Authentication Layer"
        AUTH --> SESSION_CHECK{Session Exists?}
        SESSION_CHECK -->|No| AUTH_ERROR[Authentication Required]
        SESSION_CHECK -->|Yes| EXPIRY_CHECK{Expired?}
        EXPIRY_CHECK -->|Yes| CLEANUP[Session Cleanup]
        EXPIRY_CHECK -->|No| PROCEED[Proceed to Operation]
    end
    
    subgraph "Data Operations"
        EXEC --> BOOKS_OP{Books Query?}
        EXEC --> EXCHANGE_OP{Currency Convert?}
        
        BOOKS_OP -->|Yes| BOOKS_FILTER[Apply Filters]
        BOOKS_FILTER --> BOOKS_DATA[(Books CSV)]
        BOOKS_DATA --> BOOKS_RESULT[Format Results]
        
        EXCHANGE_OP -->|Yes| EXCHANGE_CALC[Calculate Conversion]
        EXCHANGE_CALC --> RATES_DATA[(Exchange Rates)]
        RATES_DATA --> EXCHANGE_RESULT[Format Results]
    end
    
    subgraph "Response Flow"
        BOOKS_RESULT --> ADD_USER_CONTEXT[Add User Context]
        EXCHANGE_RESULT --> ADD_USER_CONTEXT
        ADD_USER_CONTEXT --> FORMAT_RESPONSE[Format MCP Response]
        FORMAT_RESPONSE --> SEND[Send to AI Assistant]
    end
    
    AUTH_ERROR --> ERROR_RESPONSE[Error Response]
    CLEANUP --> ERROR_RESPONSE
    ERROR_RESPONSE --> SEND
    
    classDef request fill:#e1f5fe
    classDef auth fill:#f3e5f5
    classDef data fill:#e8f5e8
    classDef response fill:#fff3e0
    classDef error fill:#ffebee
    
    class REQ,PARSE request
    class AUTH,VALIDATE,SESSION_CHECK,EXPIRY_CHECK,PROCEED auth
    class EXEC,BOOKS_OP,EXCHANGE_OP,BOOKS_FILTER,EXCHANGE_CALC,BOOKS_DATA,RATES_DATA data
    class BOOKS_RESULT,EXCHANGE_RESULT,ADD_USER_CONTEXT,FORMAT_RESPONSE,SEND response
    class AUTH_ERROR,CLEANUP,ERROR_RESPONSE error
```

### Data Sources

1. **Books Database**: CSV file converted from Excel with book metadata
2. **Exchange Rates**: Synthetic currency conversion rates for demo purposes
3. **Session Storage**: In-memory dictionary (Redis/DB in production)

---

## Component Relationships

The component diagram shows the internal structure and dependencies within the MCP server.

```mermaid
graph TB
    subgraph "MCP Server Process"
        subgraph "Core Components"
            SERVER[MCP Server Instance]
            HANDLER[Tool Call Handler]
            TOOLS[Tool Registry]
        end
        
        subgraph "Authentication System"
            JWT[JWT Manager]
            SESSION[Session Manager]
            VALIDATOR[Session Validator]
        end
        
        subgraph "Data Repositories"
            BOOKS[Books Repository]
            EXCHANGE[Exchange Manager]
            CSV_PREP[CSV Preparator]
        end
        
        subgraph "Global State"
            SESSIONS_STORE[_USER_SESSIONS]
            CURRENT[_CURRENT_SESSION]
        end
        
        subgraph "External Dependencies"
            MCP_SDK[MCP Python SDK]
            XLSX_UTIL[XLSX to CSV Converter]
        end
    end
    
    subgraph "File System"
        BOOKS_CSV[data/books.csv]
        BOOKS_XLSX[sample-data/BooksDatasetClean.xlsx]
    end
    
    SERVER --> HANDLER
    HANDLER --> TOOLS
    HANDLER --> VALIDATOR
    VALIDATOR --> SESSION
    SESSION --> SESSIONS_STORE
    SESSION --> CURRENT
    TOOLS --> JWT
    JWT --> SESSION
    
    HANDLER --> BOOKS
    HANDLER --> EXCHANGE
    BOOKS --> BOOKS_CSV
    CSV_PREP --> BOOKS_XLSX
    CSV_PREP --> BOOKS_CSV
    
    SERVER --> MCP_SDK
    CSV_PREP --> XLSX_UTIL
    
    classDef core fill:#e3f2fd
    classDef auth fill:#f1f8e9
    classDef data fill:#fff3e0
    classDef global fill:#fce4ec
    classDef external fill:#f5f5f5
    classDef files fill:#e0f2f1
    
    class SERVER,HANDLER,TOOLS core
    class JWT,SESSION,VALIDATOR auth
    class BOOKS,EXCHANGE,CSV_PREP data
    class SESSIONS_STORE,CURRENT global
    class MCP_SDK,XLSX_UTIL external
    class BOOKS_CSV,BOOKS_XLSX files
```

### Component Dependencies

1. **MCP Server Instance**: Central coordinator using Python MCP SDK
2. **Tool Call Handler**: Main dispatcher for all incoming requests
3. **Session Manager**: Handles authentication state and validation
4. **Data Repositories**: Encapsulate book and currency data operations
5. **Global State**: Shared session storage for AI assistant compatibility

---

## Security Model

The security architecture balances simplicity with protection for demonstration purposes.

```mermaid
graph TD
    subgraph "Security Layers"
        subgraph "Authentication Layer"
            JWT_CREATE[JWT Token Creation]
            JWT_VALIDATE[JWT Token Validation]
            HMAC[HMAC-SHA256 Signing]
        end
        
        subgraph "Session Security"
            EXPIRATION[1-Hour Expiration]
            AUTO_CLEANUP[Automatic Cleanup]
            SESSION_ISOLATION[Session Isolation]
        end
        
        subgraph "Access Control"
            PUBLIC_TOOLS[Public Tools]
            PROTECTED_TOOLS[Protected Tools]
            SESSION_CHECK[Session Validation]
        end
        
        subgraph "Data Protection"
            NO_SENSITIVE[No Sensitive Data Storage]
            AUDIT_TRAIL[User Context in Responses]
            ERROR_HANDLING[Secure Error Messages]
        end
    end
    
    JWT_CREATE --> HMAC
    JWT_VALIDATE --> HMAC
    JWT_VALIDATE --> EXPIRATION
    EXPIRATION --> AUTO_CLEANUP
    
    PUBLIC_TOOLS --> SESSION_CHECK
    PROTECTED_TOOLS --> SESSION_CHECK
    SESSION_CHECK --> SESSION_ISOLATION
    
    SESSION_ISOLATION --> AUDIT_TRAIL
    AUTO_CLEANUP --> NO_SENSITIVE
    ERROR_HANDLING --> AUDIT_TRAIL
    
    classDef auth fill:#e8f5e8
    classDef session fill:#e3f2fd
    classDef access fill:#fff3e0
    classDef data fill:#f1f8e9
    
    class JWT_CREATE,JWT_VALIDATE,HMAC auth
    class EXPIRATION,AUTO_CLEANUP,SESSION_ISOLATION session
    class PUBLIC_TOOLS,PROTECTED_TOOLS,SESSION_CHECK access
    class NO_SENSITIVE,AUDIT_TRAIL,ERROR_HANDLING data
```

### Security Features

1. **JWT Token Security**:
   - HS256 algorithm with HMAC-SHA256 signing
   - 1-hour expiration for session limits
   - Demo secret key (replace in production)

2. **Session Management**:
   - Automatic cleanup of expired sessions
   - Session isolation between users
   - No persistent storage of sensitive data

3. **Access Control**:
   - Public tools (session management) vs protected tools (data operations)
   - Session validation for all protected operations
   - Clear authentication error messages

4. **Audit Trail**:
   - All responses include authenticated_user context
   - Operation timestamps for tracking
   - Comprehensive error reporting

### Security Considerations for Production

- Replace demo secret key with secure random key from environment
- Implement Redis or database for session storage
- Add rate limiting and request validation
- Use HTTPS for transport security
- Implement proper logging and monitoring

---

## Deployment Architecture

The deployment architecture shows how the MCP server integrates with different environments and clients.

```mermaid
graph TB
    subgraph "Development Environment"
        subgraph "Local Python"
            CONDA[Conda Environment]
            PYTHON[Python 3.12+]
            MCP_PKG[MCP Package]
        end
        
        subgraph "AI Assistant Integration"
            CURSOR[Cursor IDE]
            COPILOT[GitHub Copilot]
            CONFIG[settings.json]
        end
    end
    
    subgraph "Docker Environment"
        subgraph "Container"
            DOCKER_PYTHON[Python Runtime]
            DOCKER_APP[MCP Server App]
            DOCKER_DATA[Data Volume]
        end
        
        subgraph "Docker Compose"
            COMPOSE[docker-compose.yml]
            VOLUMES[Volume Mounts]
            NETWORK[Container Network]
        end
    end
    
    subgraph "MCP Server Process"
        STDIO[stdio Transport]
        SERVER_CORE[MCP Server Core]
        DATA_REPOS[Data Repositories]
    end
    
    subgraph "Data Sources"
        CSV_DATA[books.csv]
        XLSX_SOURCE[BooksDatasetClean.xlsx]
        RATE_DATA[Exchange Rates]
    end
    
    CONDA --> PYTHON
    PYTHON --> MCP_PKG
    MCP_PKG --> SERVER_CORE
    
    CURSOR --> CONFIG
    COPILOT --> CONFIG
    CONFIG --> STDIO
    
    DOCKER_PYTHON --> DOCKER_APP
    DOCKER_DATA --> CSV_DATA
    COMPOSE --> VOLUMES
    VOLUMES --> DOCKER_DATA
    
    STDIO --> SERVER_CORE
    SERVER_CORE --> DATA_REPOS
    DATA_REPOS --> CSV_DATA
    DATA_REPOS --> XLSX_SOURCE
    DATA_REPOS --> RATE_DATA
    
    classDef local fill:#e1f5fe
    classDef docker fill:#f3e5f5
    classDef server fill:#e8f5e8
    classDef data fill:#fff3e0
    
    class CONDA,PYTHON,MCP_PKG,CURSOR,COPILOT,CONFIG local
    class DOCKER_PYTHON,DOCKER_APP,DOCKER_DATA,COMPOSE,VOLUMES,NETWORK docker
    class STDIO,SERVER_CORE,DATA_REPOS server
    class CSV_DATA,XLSX_SOURCE,RATE_DATA data
```

### Deployment Options

1. **Local Development**:
   ```bash
   # Direct execution
   python -m mcp_server.server
   
   # Via Cursor IDE integration
   # Configured in settings.json
   ```

2. **Docker Deployment**:
   ```bash
   # Docker Compose
   docker-compose up
   
   # Direct Docker
   docker build -t mcp-server .
   docker run -v $(pwd)/data:/app/data mcp-server
   ```

3. **AI Assistant Integration**:
   ```json
   {
     "mcpServers": {
       "books-mcp": {
         "command": "python",
         "args": ["-m", "mcp_server.server"],
         "cwd": "/path/to/project"
       }
     }
   }
   ```

### Integration Points

- **Cursor IDE**: Direct integration via settings.json configuration
- **GitHub Copilot**: MCP client connection for AI assistant features
- **Docker**: Containerized deployment with volume mounts for data
- **Local Development**: Direct Python execution with conda environment

---

## Conclusion

This architecture provides a robust, session-based authentication system specifically designed for AI assistant compatibility. The design balances security, usability, and simplicity while maintaining clear separation of concerns and comprehensive audit trails.

Key architectural decisions:
- Global session state for AI assistant compatibility
- JWT tokens for secure session management
- 1-hour session expiration for security
- Comprehensive error handling and user feedback
- Modular component design for maintainability
- Docker support for deployment flexibility

The system successfully addresses the core challenge of providing authenticated access to protected operations while maintaining a simple, intuitive workflow for AI assistants.