# Weather Slack Bot 🌤️

A GitHub Actions-powered bot that fetches weather information from multiple cities and sends a beautifully formatted report to Slack.

## Features

- 🌍 Fetches weather data for multiple locations using city names or zip codes
- 📍 Supports precise location targeting with zip/postal codes
- 🎯 Handles ambiguous city names with state/country codes
- 📊 Gets real-time weather information from OpenWeatherMap API
- 💬 Sends formatted messages to Slack via webhook
- ⏰ Runs automatically on a schedule using GitHub Actions
- 🎯 Can be manually triggered with custom location lists
- 🌡️ Shows temperature in both Celsius and Fahrenheit
- 🗺️ Displays coordinates for verification
- 🎨 Uses weather emojis for better visualization

## Prerequisites

Before setting up this project, you'll need:

1. **OpenWeatherMap API Key**
   - Sign up at [OpenWeatherMap](https://openweathermap.org/api)
   - Get your free API key from the API keys section

2. **Slack Webhook URL**
   - Go to your Slack workspace
   - Navigate to [Slack API](https://api.slack.com/apps)
   - Create a new app or use an existing one
   - Go to "Incoming Webhooks" and activate it
   - Add a new webhook to your desired channel
   - Copy the webhook URL

3. **GitHub Repository**
   - Create a new repository or fork this one

## Setup Instructions

### Step 1: Clone or Fork the Repository

```bash
git clone https://github.com/yourusername/weather-slack-bot.git
cd weather-slack-bot
```

### Step 2: Add Repository Secrets

Go to your GitHub repository settings:

1. Navigate to **Settings** → **Secrets and variables** → **Actions**
2. Click **New repository secret**
3. Add the following secrets:

   - **Name:** `OPENWEATHER_API_KEY`
     **Value:** Your OpenWeatherMap API key

   - **Name:** `SLACK_WEBHOOK_URL`
     **Value:** Your Slack webhook URL

### Step 3: Customize the Locations List (Optional)

Edit the `.github/workflows/weather-report.yml` file to change the default locations:

```yaml
LOCATIONS: '10001,US;London,UK;Tokyo,JP;Sydney,AU'  # Add your locations here
```

**Location Format Options:**

1. **US Zip Codes**: `"10001,US"` or just `"10001"`
2. **International Postal Codes**: `"SW1A 1AA,UK"` or `"K1A 0B1,CA"`
3. **City Names**: `"London"` or `"London,UK"` (country code recommended)
4. **City with State**: `"Springfield,IL,US"` (essential for ambiguous US cities)
5. **Mix and Match**: Use semicolons to separate when mixing formats

**Examples:**
```yaml
# US cities using zip codes (most precise)
LOCATIONS: '10001,US;94105,US;60601,US;02101,US'

# International cities with country codes
LOCATIONS: 'London,UK;Paris,FR;Tokyo,JP;Berlin,DE'

# Mixing zip codes and city names
LOCATIONS: '10001,US;London,UK;94105,US;Sydney,AU'

# Handling ambiguous city names
LOCATIONS: 'Springfield,IL,US;Springfield,MA,US;Springfield,MO,US'
```

**Why Use Zip Codes?**
- Eliminates ambiguity (e.g., "Springfield" exists in 34 US states!)
- More precise location targeting
- Consistent results
- Works great for US locations (5-digit codes)

### Step 4: Customize the Schedule (Optional)

The bot runs daily at 8 AM UTC by default. To change this, edit the cron expression in `.github/workflows/weather-report.yml`:

```yaml
schedule:
  - cron: '0 8 * * *'  # Modify this line
```

**Cron Expression Examples:**
- `'0 6 * * *'` - Every day at 6 AM UTC
- `'0 */6 * * *'` - Every 6 hours
- `'0 9 * * 1-5'` - Monday to Friday at 9 AM UTC
- `'0 12 * * 0'` - Every Sunday at noon UTC

Use [crontab.guru](https://crontab.guru/) to help create cron expressions.

## Usage

### Automatic Execution

Once set up, the workflow will run automatically according to your schedule and send weather reports to your Slack channel.

### Manual Execution

You can manually trigger the workflow:

1. Go to the **Actions** tab in your GitHub repository
2. Select **Daily Weather Report** workflow
3. Click **Run workflow**
4. (Optional) Enter a custom list of locations (semicolon-separated for clarity)
5. Click **Run workflow** button

**Manual Trigger Examples:**
- `10001,US;90210,US;60601,US` - Major US cities by zip
- `London,UK;Paris,FR;Tokyo,JP` - International cities
- `Springfield,IL,US;Portland,OR,US;Portland,ME,US` - Specific US cities

### Local Testing

To test the script locally:

```bash
# Install dependencies
pip install -r requirements.txt

# Set environment variables
export OPENWEATHER_API_KEY="your_api_key_here"
export SLACK_WEBHOOK_URL="your_webhook_url_here"

# Using city names
export LOCATIONS="London,UK;Paris,FR;Tokyo,JP"

# Using US zip codes
export LOCATIONS="10001,US;94105,US;60601,US"

# Using semicolon separator for mixed formats
export LOCATIONS="10001,US;London,UK;Springfield,IL,US"

# Run the script
python weather_bot.py
```

## Project Structure

```
weather-slack-bot/
├── .github/
│   └── workflows/
│       └── weather-report.yml    # GitHub Actions workflow
├── weather_bot.py                # Main Python script
├── requirements.txt              # Python dependencies
└── README.md                     # This file
```

## Customization

### Adding More Weather Information

Edit `weather_bot.py` to include additional data points:
- Sunrise/sunset times
- UV index
- Air pressure
- Visibility

### Changing Message Format

Modify the `create_slack_message()` method in `weather_bot.py` to customize the Slack message appearance.

### Adding Error Notifications

You can add another Slack webhook or email notification for when the workflow fails.

## Troubleshooting

### Workflow Not Running

- Check if GitHub Actions is enabled for your repository
- Verify the cron syntax is correct
- Check the Actions tab for any error messages

### API Errors

- Verify your OpenWeatherMap API key is valid
- Check if you've exceeded the API rate limit (60 calls/minute for free tier)
- Ensure city names are spelled correctly

### Slack Messages Not Appearing

- Verify the webhook URL is correct
- Check if the webhook is still active in Slack
- Look at the GitHub Actions logs for error messages

## Contributing

Feel free to open issues or submit pull requests with improvements!

## License

MIT License - feel free to use this project however you'd like!

## Resources

- [OpenWeatherMap API Documentation](https://openweathermap.org/current)
- [Slack Incoming Webhooks](https://api.slack.com/messaging/webhooks)
- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [Cron Expression Generator](https://crontab.guru/)

## Example Output

The bot sends a formatted message to Slack that looks like:

```
🌍 Daily Weather Report
Generated on: December 15, 2024 at 08:00 AM

☀️ New York, NY, US
Search: 10001,US
Condition: Clear sky
Temperature: 12.5°C (54.5°F)
Feels Like: 11.2°C (52.2°F)
Humidity: 65%
Wind Speed: 3.5 m/s
📍 40.75, -73.99

🌧️ London, GB
Search: London,UK
Condition: Light rain
Temperature: 8.3°C (46.9°F)
Feels Like: 6.1°C (43.0°F)
Humidity: 78%
Wind Speed: 5.2 m/s
📍 51.51, -0.13

[... more locations ...]

📊 Data provided by OpenWeatherMap
```

---

Made with ❤️ using GitHub Actions, Python, and APIs