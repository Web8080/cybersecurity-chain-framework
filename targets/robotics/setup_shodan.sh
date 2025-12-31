#!/bin/bash
# Setup script for Shodan/Censys Search

set -e

echo " Setting up Shodan/Censys Search Tools..."
echo ""

# Check for Python
if command -v python3 &> /dev/null; then
 echo " Python found: $(python3 --version)"
else
 echo " Python 3 not found"
 exit 1
fi

echo ""
echo " Installing Shodan CLI..."
echo ""

# Check if shodan is installed
if command -v shodan &> /dev/null; then
 echo " Shodan CLI already installed"
else
 echo "Installing Shodan CLI..."
 pip3 install --user shodan
 echo " Shodan CLI installed"
fi

echo ""
echo " Installing Censys tools..."
echo ""

# Check if censys is installed
if pip3 show censys &> /dev/null; then
 echo " Censys Python library already installed"
else
 echo "Installing Censys Python library..."
 pip3 install --user censys
 echo " Censys library installed"
fi

echo ""
echo " LEGAL WARNING"
echo "=============="
echo "Only search for and test devices you own or have explicit written permission to test!"
echo "Unauthorized access to computer systems is illegal."
echo ""

echo " Setup Steps:"
echo ""
echo "1. Get Shodan API Key:"
echo " - Sign up at: https://account.shodan.io/register"
echo " - Get API key from: https://account.shodan.io/"
echo " - Configure: shodan init YOUR_API_KEY"
echo ""
echo "2. Get Censys API Credentials:"
echo " - Sign up at: https://search.censys.io/register"
echo " - Get API ID and Secret from: https://search.censys.io/account/api"
echo " - Configure: export CENSYS_API_ID='your_id'"
echo " - Configure: export CENSYS_API_SECRET='your_secret'"
echo ""

echo " Example Queries:"
echo ""
echo "Shodan:"
echo " shodan search 'robot controller'"
echo " shodan search 'modbus' port:502"
echo " shodan search 'ros master' port:11311"
echo ""
echo "Censys:"
echo " python3 censys_search.py 'services.service_name:MODBUS'"
echo ""

echo " Setup complete!"
echo ""
echo " See: docs/shodan_censys_guide.md for detailed instructions"

