#!/bin/bash

# Replace YOUR_USERNAME with your actual GitHub username
GITHUB_USERNAME="YOUR_USERNAME"

echo "Setting up GitHub remote for weather-slack-bot..."
cd /Users/brogen.wheeler/weather-slack-bot

# Add the remote origin
git remote add origin https://github.com/$GITHUB_USERNAME/weather-slack-bot.git

# Verify remote was added
echo "Remote added. Verifying..."
git remote -v

# Push to GitHub
echo "Pushing to GitHub..."
git branch -M main
git push -u origin main

echo "Done! Your code is now on GitHub."
echo "Next steps:"
echo "1. Go to https://github.com/$GITHUB_USERNAME/weather-slack-bot/settings/secrets/actions"
echo "2. Add your secrets:"
echo "   - OPENWEATHER_API_KEY"
echo "   - SLACK_WEBHOOK_URL"
