#!/bin/bash
# Quick setup script for DVWA (Damn Vulnerable Web Application)

set -e

echo " Setting up DVWA (Damn Vulnerable Web Application)..."
echo ""

# Check if Docker is installed
if command -v docker &> /dev/null; then
 echo " Docker found"
 echo ""
 echo "Starting DVWA with Docker..."
 echo "This will run in the background."
 echo ""
 
 # Check if already running
 if docker ps -a --format '{{.Names}}' | grep -q "^dvwa$"; then
 echo " Container 'dvwa' already exists"
 read -p "Remove and recreate? (y/n) " -n 1 -r
 echo
 if [[ $REPLY =~ ^[Yy]$ ]]; then
 docker rm -f dvwa 2>/dev/null || true
 docker run -d --name dvwa -p 8080:80 vulnerables/web-dvwa
 echo " DVWA started!"
 else
 echo "Starting existing container..."
 docker start dvwa
 echo " DVWA started!"
 fi
 else
 docker run -d --name dvwa -p 8080:80 vulnerables/web-dvwa
 echo " DVWA started!"
 fi
 
 echo ""
 echo "Waiting for service to be ready..."
 sleep 8
 
 # Check if it's running
 if curl -s http://localhost:8080 > /dev/null; then
 echo " DVWA is running at http://localhost:8080"
 echo ""
 echo " Default credentials:"
 echo " Username: admin"
 echo " Password: password"
 echo ""
 echo " Note: You may need to click 'Create / Reset Database' on first visit"
 else
 echo " Service is starting... check http://localhost:8080 in a few seconds"
 fi
 
else
 echo " Docker not found"
 echo ""
 echo "Please install Docker: https://docs.docker.com/get-docker/"
 echo ""
 echo "Or use alternative setup:"
 echo " git clone https://github.com/digininja/DVWA.git"
 echo " cd DVWA && docker-compose up"
 exit 1
fi

echo ""
echo " Ready for pentesting!"
echo ""
echo "Next steps:"
echo " 1. Access http://localhost:8080"
echo " 2. Login with admin/password"
echo " 3. Click 'Create / Reset Database' if needed"
echo " 4. Start finding vulnerabilities"
echo " 5. Use chain_analyzer.py to document attack chains"
echo ""

