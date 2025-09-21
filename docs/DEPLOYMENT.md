# Deployment Guide

Complete deployment guide for the Session-Based Authenticated MCP Server across different environments.

## Table of Contents

1. [Deployment Overview](#deployment-overview)
2. [Local Development Setup](#local-development-setup)
3. [Docker Deployment](#docker-deployment)
4. [AI Assistant Integration](#ai-assistant-integration)
5. [Production Deployment](#production-deployment)
6. [Configuration Management](#configuration-management)
7. [Monitoring and Maintenance](#monitoring-and-maintenance)
8. [Troubleshooting](#troubleshooting)

---

## Deployment Overview

The MCP Server supports multiple deployment methods:

- **Local Development**: Direct Python execution with conda environment
- **Docker**: Containerized deployment with docker-compose
- **AI Assistant Integration**: Cursor IDE and GitHub Copilot configuration
- **Production**: Scalable deployment with proper security measures

### System Requirements

**Minimum Requirements**:
- Python 3.12+ or Docker 20.10+
- 512MB RAM
- 100MB disk space

**Recommended Requirements**:
- Python 3.12+ with conda environment
- 2GB RAM for Docker deployment
- 1GB disk space for full development setup
- SSD storage for better performance

### Port Requirements

- **MCP Protocol**: Uses stdio transport (no network ports)
- **Docker Internal**: Container-internal communication only
- **Development**: No external port exposure required

---

## Local Development Setup

### Prerequisites

1. **Python Environment**:
   ```bash
   # Using conda (recommended)
   conda create -n mcp-server python=3.12
   conda activate mcp-server
   
   # Or using venv
   python3.12 -m venv venv
   source venv/bin/activate  # On macOS/Linux
   # venv\Scripts\activate  # On Windows
   ```

2. **Clone Repository**:
   ```bash
   git clone <repository-url>
   cd MCP-server
   ```

### Installation Steps

1. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Verify Installation**:
   ```bash
   python -c "import mcp; print('MCP package installed successfully')"
   ```

3. **Prepare Data**:
   ```bash
   # Ensure sample data exists
   ls sample-data/BooksDatasetClean.xlsx
   
   # Create data directory (will be created automatically)
   mkdir -p data
   ```

### Running the Server

1. **Direct Execution**:
   ```bash
   # Method 1: Module execution
   python -m mcp_server.server
   
   # Method 2: Direct script execution
   python mcp_server/server.py
   ```

2. **Test Basic Functionality**:
   ```bash
   # In another terminal, test with curl (example only - actual MCP uses stdio)
   echo '{"method": "tools/list", "params": {}}' | python -m mcp_server.server
   ```

### Development Workflow

```bash
# 1. Activate environment
conda activate mcp-server

# 2. Make code changes
vim mcp_server/server.py

# 3. Run tests
python -m pytest tests/ -v

# 4. Test server
python -m mcp_server.server

# 5. Commit changes
git add .
git commit -m "Add new feature"
```

---

## Docker Deployment

### Docker Setup

1. **Build Image**:
   ```bash
   # Build from Dockerfile
   docker build -t mcp-server:latest .
   
   # Verify build
   docker images | grep mcp-server
   ```

2. **Run Container**:
   ```bash
   # Basic run
   docker run --rm -v $(pwd)/data:/app/data mcp-server:latest
   
   # Interactive run for testing
   docker run --rm -it -v $(pwd)/data:/app/data mcp-server:latest bash
   ```

### Docker Compose Deployment

1. **Start Services**:
   ```bash
   # Start in foreground
   docker-compose up
   
   # Start in background
   docker-compose up -d
   
   # View logs
   docker-compose logs -f
   ```

2. **Service Management**:
   ```bash
   # Stop services
   docker-compose down
   
   # Rebuild and restart
   docker-compose up --build
   
   # Scale services (if configured)
   docker-compose up --scale mcp-server=3
   ```

3. **Data Persistence**:
   ```yaml
   # docker-compose.yml volumes configuration
   services:
     mcp-server:
       volumes:
         - ./data:/app/data
         - ./sample-data:/app/sample-data
   ```

### Docker Configuration

**Dockerfile Customization**:
```dockerfile
# Custom environment variables
ENV JWT_SECRET_KEY="your-secure-secret-key"
ENV SESSION_TIMEOUT="3600"

# Additional packages
RUN pip install redis boto3

# Custom entrypoint
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh
ENTRYPOINT ["/entrypoint.sh"]
```

**Environment Variables**:
```bash
# .env file for docker-compose
JWT_SECRET_KEY=your-secure-secret-key-here
SESSION_TIMEOUT=3600
DEBUG=false
LOG_LEVEL=INFO
```

---

## AI Assistant Integration

### Cursor IDE Setup

1. **Configuration File**:
   ```json
   // .cursor/settings.json or VS Code settings.json
   {
     "mcpServers": {
       "books-mcp": {
         "command": "python",
         "args": ["-m", "mcp_server.server"],
         "cwd": "/absolute/path/to/MCP-server",
         "env": {
           "PYTHONPATH": "/absolute/path/to/MCP-server"
         }
       }
     }
   }
   ```

2. **Alternative Docker Configuration**:
   ```json
   {
     "mcpServers": {
       "books-mcp-docker": {
         "command": "docker",
         "args": [
           "run", "--rm", "-i",
           "-v", "/absolute/path/to/MCP-server/data:/app/data",
           "mcp-server:latest"
         ],
         "cwd": "/absolute/path/to/MCP-server"
       }
     }
   }
   ```

### GitHub Copilot Integration

1. **MCP Client Configuration**:
   ```json
   // mcp-config.json
   {
     "servers": {
       "books-mcp": {
         "command": "python",
         "args": ["-m", "mcp_server.server"],
         "env": {}
       }
     }
   }
   ```

2. **Integration Testing**:
   ```bash
   # Test MCP server connectivity
   python -c "
   import asyncio
   from mcp_server.server import server
   print('MCP Server configured successfully')
   "
   ```

### Integration Verification

1. **Authentication Flow Test**:
   ```json
   // Test sequence in AI assistant
   1. Call: authenticate {"username": "test_user"}
   2. Call: session_status {}
   3. Call: books_query {"limit": 3}
   4. Call: logout {}
   ```

2. **Error Handling Test**:
   ```json
   // Test authentication requirement
   1. Call: books_query {"title": "python"}  // Should fail
   2. Call: authenticate {"username": "test"}
   3. Call: books_query {"title": "python"}  // Should succeed
   ```

---

## Production Deployment

### Security Hardening

1. **Environment Variables**:
   ```bash
   # Secure JWT secret
   export JWT_SECRET_KEY=$(openssl rand -hex 32)
   
   # Session configuration
   export SESSION_TIMEOUT=3600
   export MAX_SESSIONS=1000
   
   # Logging
   export LOG_LEVEL=INFO
   export LOG_FILE=/var/log/mcp-server.log
   ```

2. **File Permissions**:
   ```bash
   # Secure file permissions
   chmod 600 .env
   chmod 755 mcp_server/
   chmod 644 mcp_server/*.py
   chown mcp-user:mcp-group -R /app/
   ```

### Database Integration

1. **Redis Session Storage**:
   ```python
   # Production session storage
   import redis
   
   redis_client = redis.Redis(
       host='redis-server',
       port=6379,
       db=0,
       decode_responses=True
   )
   
   # Replace global session storage
   def store_session(session_id, session_data):
       redis_client.setex(
           f"session:{session_id}",
           3600,  # 1 hour TTL
           json.dumps(session_data)
       )
   ```

2. **Database Configuration**:
   ```yaml
   # docker-compose.prod.yml
   services:
     redis:
       image: redis:7-alpine
       volumes:
         - redis_data:/data
       command: redis-server --appendonly yes
   
     mcp-server:
       depends_on:
         - redis
       environment:
         - REDIS_URL=redis://redis:6379/0
   
   volumes:
     redis_data:
   ```

### Load Balancing

1. **Multiple Instances**:
   ```yaml
   # docker-compose.scale.yml
   services:
     mcp-server:
       deploy:
         replicas: 3
       environment:
         - INSTANCE_ID=${HOSTNAME}
   ```

2. **Health Checks**:
   ```yaml
   services:
     mcp-server:
       healthcheck:
         test: ["CMD", "python", "-c", "import mcp_server.server"]
         interval: 30s
         timeout: 10s
         retries: 3
   ```

### Monitoring Setup

1. **Prometheus Metrics**:
   ```python
   # Add to server.py
   from prometheus_client import Counter, Histogram, start_http_server
   
   REQUEST_COUNT = Counter('mcp_requests_total', 'Total requests', ['tool', 'status'])
   REQUEST_DURATION = Histogram('mcp_request_duration_seconds', 'Request duration')
   
   # Start metrics server
   start_http_server(8000)
   ```

2. **Logging Configuration**:
   ```python
   import logging
   import structlog
   
   # Structured logging
   structlog.configure(
       processors=[
           structlog.processors.JSONRenderer()
       ],
       logger_factory=structlog.stdlib.LoggerFactory(),
   )
   ```

---

## Configuration Management

### Environment Configuration

1. **Development (.env.dev)**:
   ```bash
   DEBUG=true
   LOG_LEVEL=DEBUG
   JWT_SECRET_KEY=demo-secret-key-123
   SESSION_TIMEOUT=3600
   MAX_SESSIONS=10
   ```

2. **Production (.env.prod)**:
   ```bash
   DEBUG=false
   LOG_LEVEL=INFO
   JWT_SECRET_KEY=${SECURE_JWT_SECRET}
   SESSION_TIMEOUT=3600
   MAX_SESSIONS=1000
   REDIS_URL=redis://redis:6379/0
   ```

### Configuration Files

1. **Server Configuration (config.yaml)**:
   ```yaml
   server:
     name: "books-mcp"
     transport: "stdio"
     
   authentication:
     jwt_algorithm: "HS256"
     session_timeout: 3600
     max_sessions: 1000
     
   data:
     books_csv: "data/books.csv"
     excel_source: "sample-data/BooksDatasetClean.xlsx"
     
   logging:
     level: "INFO"
     format: "json"
     file: "/var/log/mcp-server.log"
   ```

2. **Docker Configuration (docker-compose.override.yml)**:
   ```yaml
   # Local development overrides
   services:
     mcp-server:
       volumes:
         - .:/app
       environment:
         - DEBUG=true
       command: python -m mcp_server.server --reload
   ```

---

## Monitoring and Maintenance

### Health Monitoring

1. **Application Health**:
   ```bash
   # Health check script
   #!/bin/bash
   python -c "
   import sys
   try:
       from mcp_server.server import server
       print('✓ MCP Server healthy')
       sys.exit(0)
   except Exception as e:
       print(f'✗ MCP Server unhealthy: {e}')
       sys.exit(1)
   "
   ```

2. **Resource Monitoring**:
   ```bash
   # Monitor resource usage
   docker stats mcp-server
   
   # Memory usage
   ps aux | grep python | grep mcp_server
   
   # Disk usage
   du -sh data/
   ```

### Log Management

1. **Log Rotation**:
   ```bash
   # logrotate configuration
   /var/log/mcp-server.log {
       daily
       missingok
       rotate 30
       compress
       notifempty
       create 644 mcp-user mcp-group
   }
   ```

2. **Log Analysis**:
   ```bash
   # Analyze authentication patterns
   grep "authenticate" /var/log/mcp-server.log | wc -l
   
   # Error analysis
   grep "ERROR" /var/log/mcp-server.log | tail -10
   
   # Session analytics
   grep "session_expired" /var/log/mcp-server.log | wc -l
   ```

### Backup Procedures

1. **Data Backup**:
   ```bash
   # Backup data directory
   tar -czf mcp-server-backup-$(date +%Y%m%d).tar.gz data/
   
   # Automated backup script
   #!/bin/bash
   BACKUP_DIR="/backups/mcp-server"
   DATE=$(date +%Y%m%d_%H%M%S)
   tar -czf "$BACKUP_DIR/backup_$DATE.tar.gz" data/ sample-data/
   find "$BACKUP_DIR" -name "backup_*.tar.gz" -mtime +7 -delete
   ```

2. **Configuration Backup**:
   ```bash
   # Backup configuration
   cp .env .env.backup.$(date +%Y%m%d)
   cp docker-compose.yml docker-compose.backup.yml
   ```

---

## Troubleshooting

### Common Issues

1. **Authentication Failures**:
   ```bash
   # Problem: "authentication_required" errors
   # Solution: Check session state
   python -c "
   from mcp_server.server import _USER_SESSIONS, _CURRENT_SESSION
   print(f'Sessions: {len(_USER_SESSIONS)}')
   print(f'Current: {_CURRENT_SESSION}')
   "
   ```

2. **Session Expiration**:
   ```bash
   # Problem: Frequent session expires
   # Solution: Check system time and JWT validation
   python -c "
   import time
   from mcp_server.server import validate_jwt_token, create_jwt_token
   token = create_jwt_token('test', 'test')
   print(f'Token valid: {validate_jwt_token(token) is not None}')
   "
   ```

3. **Data Loading Issues**:
   ```bash
   # Problem: Books data not loading
   # Solution: Check file permissions and paths
   ls -la data/books.csv
   ls -la sample-data/BooksDatasetClean.xlsx
   
   # Test CSV conversion
   python -c "
   from mcp_server.server import _prepare_books_csv
   csv_path = _prepare_books_csv()
   print(f'CSV prepared at: {csv_path}')
   "
   ```

### Docker Issues

1. **Container Startup Problems**:
   ```bash
   # Check container logs
   docker logs mcp-server
   
   # Debug container
   docker run --rm -it mcp-server:latest bash
   
   # Check volume mounts
   docker inspect mcp-server | grep -A 10 Mounts
   ```

2. **Permission Issues**:
   ```bash
   # Fix volume permissions
   docker exec mcp-server chown -R app:app /app/data
   
   # Run with user mapping
   docker run --user $(id -u):$(id -g) mcp-server:latest
   ```

### Integration Issues

1. **Cursor IDE Problems**:
   ```json
   // Check settings.json format
   {
     "mcpServers": {
       "books-mcp": {
         "command": "python",
         "args": ["-m", "mcp_server.server"],
         "cwd": "/absolute/path/to/project"
       }
     }
   }
   ```

2. **Path Resolution**:
   ```bash
   # Verify Python path
   which python
   python -c "import sys; print(sys.path)"
   
   # Test module import
   python -c "from mcp_server import server; print('Import successful')"
   ```

### Performance Issues

1. **Memory Usage**:
   ```bash
   # Monitor memory
   ps aux | grep mcp_server
   
   # Optimize session storage
   python -c "
   from mcp_server.server import _USER_SESSIONS
   print(f'Active sessions: {len(_USER_SESSIONS)}')
   "
   ```

2. **Response Time**:
   ```bash
   # Profile requests
   time python -c "
   import asyncio
   from mcp_server.server import handle_call_tool
   async def test():
       result = await handle_call_tool('session_status', {})
       print('Response received')
   asyncio.run(test())
   "
   ```

### Diagnostic Commands

```bash
# Complete system check
#!/bin/bash
echo "=== MCP Server Diagnostics ==="

echo "1. Python Environment:"
python --version
pip list | grep mcp

echo "2. Module Import Test:"
python -c "import mcp_server.server; print('✓ Server module OK')"

echo "3. Data Files:"
ls -la data/ sample-data/

echo "4. Docker Status:"
docker ps | grep mcp-server

echo "5. Recent Logs:"
tail -5 /var/log/mcp-server.log 2>/dev/null || echo "No log file found"

echo "6. Port Usage:"
lsof -i :8000 2>/dev/null || echo "No ports in use"

echo "=== Diagnostics Complete ==="
```

---

## Deployment Checklist

### Pre-Deployment

- [ ] Python 3.12+ installed
- [ ] Dependencies installed (`pip install -r requirements.txt`)
- [ ] Data files present (`sample-data/BooksDatasetClean.xlsx`)
- [ ] Environment variables configured
- [ ] Tests passing (`pytest tests/`)

### Local Development

- [ ] Server starts without errors
- [ ] Authentication flow works
- [ ] Books query returns data
- [ ] Currency conversion works
- [ ] Session expiration handles correctly

### Docker Deployment

- [ ] Docker image builds successfully
- [ ] Container runs without errors
- [ ] Volume mounts work correctly
- [ ] Environment variables passed
- [ ] Health check passes

### AI Assistant Integration

- [ ] Configuration file syntax valid
- [ ] Absolute paths configured correctly
- [ ] MCP client connects successfully
- [ ] Tools accessible from AI assistant
- [ ] Authentication flow works in AI context

### Production Deployment

- [ ] Security measures implemented
- [ ] Monitoring configured
- [ ] Logging working
- [ ] Backup procedures tested
- [ ] Performance benchmarks met
- [ ] Documentation updated

This comprehensive deployment guide ensures successful setup across all supported environments and use cases.