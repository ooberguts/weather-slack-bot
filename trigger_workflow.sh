#!/bin/bash

echo "Triggering GitHub Actions workflow..."
gh workflow run weather-report.yml --repo ooberguts/weather-slack-bot

echo ""
echo "✅ Workflow triggered!"
echo ""
echo "Watch it run at:"
echo "https://github.com/ooberguts/weather-slack-bot/actions"
echo ""
echo "Or check status with:"
echo "gh run list --repo ooberguts/weather-slack-bot"
