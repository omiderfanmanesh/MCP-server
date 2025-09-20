FROM python:3.12-slim

WORKDIR /app

# Copy requirements first for better caching
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application
COPY . .

# Ensure Python outputs are not buffered (important for stdio communication)
ENV PYTHONUNBUFFERED=1
ENV PYTHONIOENCODING=utf-8

# MCP servers use stdio for communication, not network ports
# No EXPOSE needed

# Use exec form to avoid shell wrapper that might interfere with signals
CMD ["python", "-m", "mcp_server.server"]
