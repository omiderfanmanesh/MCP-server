#!/bin/bash
# Simple Docker setup script for MCP Books Server

set -e

echo "🐳 MCP Books Server Docker Setup"
echo "================================"

# Build Docker image
echo "🔨 Building Docker image..."
docker build -t mcp-books-server .

echo "✅ Docker image built successfully!"
echo ""
echo "🚀 Next steps:"
echo "1. Start server: docker-compose up mcp-server"
echo "2. Test JWT: Call the 'get_jwt_token' tool with username parameter"
echo ""
echo "📖 The server now includes a simple JWT token generator tool"