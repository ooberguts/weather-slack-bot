#!/bin/bash
# Quick script to push to GitHub

echo "What's your GitHub username?"
read GITHUB_USERNAME

cd /Users/brogen.wheeler/weather-slack-bot

echo "Adding GitHub remote..."
git remote add origin https://github.com/$GITHUB_USERNAME/weather-slack-bot.git

echo "Pushing to GitHub..."
git push -u origin main

echo ""
echo "✅ Done! Your project is now at:"
echo "https://github.com/$GITHUB_USERNAME/weather-slack-bot"
