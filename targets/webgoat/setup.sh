#!/bin/bash
# Quick setup script for OWASP WebGoat

set -e

echo " Setting up OWASP WebGoat..."
echo ""

# Check if Docker is installed
if command -v docker &> /dev/null; then
 echo " Docker found"
 echo ""
 echo "Starting WebGoat with Docker..."
 echo "This will run in the background."
 echo ""
 
 # Check if already running
 if docker ps -a --format '{{.Names}}' | grep -q "^webgoat$"; then
 echo " Container 'webgoat' already exists"
 read -p "Remove and recreate? (y/n) " -n 1 -r
 echo
 if [[ $REPLY =~ ^[Yy]$ ]]; then
 docker rm -f webgoat 2>/dev/null || true
 docker run -d --name webgoat -p 8080:8080 webgoat/goatandwolf
 echo " WebGoat started!"
 else
 echo "Starting existing container..."
 docker start webgoat
 echo " WebGoat started!"
 fi
 else
 docker run -d --name webgoat -p 8080:8080 webgoat/goatandwolf
 echo " WebGoat started!"
 fi
 
 echo ""
 echo "Waiting for service to be ready (this may take 30-60 seconds)..."
 sleep 10
 
 # Check if it's running
 max_attempts=12
 attempt=0
 while [ $attempt -lt $max_attempts ]; do
 if curl -s http://localhost:8080/WebGoat > /dev/null; then
 echo " WebGoat is running at http://localhost:8080/WebGoat"
 echo ""
 echo " First time setup:"
 echo " 1. Visit http://localhost:8080/WebGoat"
 echo " 2. Register a new account"
 echo " 3. Start with the lessons"
 break
 fi
 attempt=$((attempt + 1))
 echo " Waiting... ($attempt/$max_attempts)"
 sleep 5
 done
 
 if [ $attempt -eq $max_attempts ]; then
 echo " Service is still starting... check http://localhost:8080/WebGoat in a minute"
 fi
 
else
 echo " Docker not found"
 echo ""
 echo "Please install Docker: https://docs.docker.com/get-docker/"
 echo ""
 echo "Or download standalone JAR:"
 echo " wget https://github.com/WebGoat/WebGoat/releases/download/v8.2.2/webgoat-server-8.2.2.jar"
 echo " java -jar webgoat-server-8.2.2.jar"
 exit 1
fi

echo ""
echo " Ready for pentesting!"
echo ""
echo "Next steps:"
echo " 1. Access http://localhost:8080/WebGoat"
echo " 2. Register a new account"
echo " 3. Complete guided lessons"
echo " 4. Use chain_analyzer.py to document attack chains"
echo ""


