#!/bin/bash
# Quick setup script for bWAPP (Buggy Web Application)

set -e

echo "🐛 Setting up bWAPP (Buggy Web Application)..."
echo ""

# Check if Docker is installed
if command -v docker &> /dev/null; then
    echo "✅ Docker found"
    echo ""
    echo "Starting bWAPP with Docker..."
    echo "This will run in the background."
    echo ""
    
    # Check if already running
    if docker ps -a --format '{{.Names}}' | grep -q "^bwapp$"; then
        echo "⚠️  Container 'bwapp' already exists"
        read -p "Remove and recreate? (y/n) " -n 1 -r
        echo
        if [[ $REPLY =~ ^[Yy]$ ]]; then
            docker rm -f bwapp 2>/dev/null || true
            docker run -d --name bwapp -p 80:80 raesene/bwapp
            echo "✅ bWAPP started!"
        else
            echo "Starting existing container..."
            docker start bwapp
            echo "✅ bWAPP started!"
        fi
    else
        docker run -d --name bwapp -p 80:80 raesene/bwapp
        echo "✅ bWAPP started!"
    fi
    
    echo ""
    echo "Waiting for service to be ready..."
    sleep 8
    
    # Check if it's running
    if curl -s http://localhost > /dev/null; then
        echo "✅ bWAPP is running at http://localhost"
        echo ""
        echo "📝 Default credentials:"
        echo "   Username: bee"
        echo "   Password: bug"
        echo ""
        echo "   Or try: admin/admin"
    else
        echo "⏳ Service is starting... check http://localhost in a few seconds"
    fi
    
else
    echo "❌ Docker not found"
    echo ""
    echo "Please install Docker: https://docs.docker.com/get-docker/"
    exit 1
fi

echo ""
echo "🎯 Ready for pentesting!"
echo ""
echo "Next steps:"
echo "  1. Access http://localhost"
echo "  2. Login with bee/bug or admin/admin"
echo "  3. Explore 100+ vulnerabilities"
echo "  4. Use chain_analyzer.py to document attack chains"
echo ""


