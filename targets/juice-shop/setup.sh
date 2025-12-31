#!/bin/bash
# Quick setup script for OWASP Juice Shop

set -e

echo "🍹 Setting up OWASP Juice Shop..."
echo ""

# Check if Docker is installed
if command -v docker &> /dev/null; then
    echo "✅ Docker found"
    echo ""
    echo "Starting Juice Shop with Docker..."
    echo "This will run in the background."
    echo ""
    echo "To start: docker run -d --name juice-shop -p 3000:3000 bkimminich/juice-shop"
    echo "To stop:  docker stop juice-shop"
    echo "To view:  docker logs juice-shop"
    echo ""
    echo "Access at: http://localhost:3000"
    echo ""
    
    # Check if already running
    if docker ps -a --format '{{.Names}}' | grep -q "^juice-shop$"; then
        echo "⚠️  Container 'juice-shop' already exists"
        read -p "Remove and recreate? (y/n) " -n 1 -r
        echo
        if [[ $REPLY =~ ^[Yy]$ ]]; then
            docker rm -f juice-shop 2>/dev/null || true
            docker run -d --name juice-shop -p 3000:3000 bkimminich/juice-shop
            echo "✅ Juice Shop started!"
        else
            echo "Starting existing container..."
            docker start juice-shop
            echo "✅ Juice Shop started!"
        fi
    else
        docker run -d --name juice-shop -p 3000:3000 bkimminich/juice-shop
        echo "✅ Juice Shop started!"
    fi
    
    echo ""
    echo "Waiting for service to be ready..."
    sleep 5
    
    # Check if it's running
    if curl -s http://localhost:3000 > /dev/null; then
        echo "✅ Juice Shop is running at http://localhost:3000"
    else
        echo "⏳ Service is starting... check http://localhost:3000 in a few seconds"
    fi
    
elif command -v npm &> /dev/null; then
    echo "✅ npm found"
    echo ""
    echo "Installing Juice Shop globally..."
    npm install -g juice-shop
    echo ""
    echo "✅ Installation complete!"
    echo ""
    echo "To start: juice-shop"
    echo "Access at: http://localhost:3000"
    
else
    echo "❌ Neither Docker nor npm found"
    echo ""
    echo "Please install one of:"
    echo "  - Docker: https://docs.docker.com/get-docker/"
    echo "  - Node.js/npm: https://nodejs.org/"
    echo ""
    echo "Or clone from source:"
    echo "  git clone https://github.com/juice-shop/juice-shop.git"
    echo "  cd juice-shop && npm install && npm start"
    exit 1
fi

echo ""
echo "🎯 Ready for pentesting!"
echo ""
echo "Next steps:"
echo "  1. Access http://localhost:3000"
echo "  2. Start finding vulnerabilities"
echo "  3. Use chain_analyzer.py to document attack chains"
echo "  4. Check example_chain.py for reference"
