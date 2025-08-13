#!/bin/bash

echo "==================================="
echo "   GitHub CLI Login Instructions"
echo "==================================="
echo ""
echo "I'm going to run 'gh auth login' for you."
echo ""
echo "You'll be asked a few questions:"
echo "1. What account? Choose: GitHub.com"
echo "2. Protocol? Choose: HTTPS"
echo "3. Authenticate? Choose: Login with a web browser"
echo "4. It will give you a code - press Enter to open browser"
echo "5. Paste the code in your browser"
echo "6. Authorize in browser"
echo ""
echo "Ready? Press Enter to start..."
read

gh auth login
