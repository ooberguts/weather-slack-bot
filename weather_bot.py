#!/usr/bin/env python3
"""
Weather Bot Script
Fetches weather data from OpenWeatherMap API and sends to Slack
"""

import os
import sys
import json
import requests
import pytz
from datetime import datetime
from typing import List, Dict, Any

class WeatherBot:
    def __init__(self, api_key: str, slack_webhook: str):
        """Initialize the weather bot with API credentials"""
        self.api_key = api_key
        self.slack_webhook = slack_webhook
        self.base_url = "https://api.openweathermap.org/data/2.5/weather"
        
    def get_weather(self, location: str) -> Dict[str, Any]:
        """
        Fetch weather data for a specific location.
        Supports:
        - City name: "London" or "London,UK"
        - US Zip code: "10001" or "10001,US"
        - International postal code with country: "SW1A 1AA,UK"
        - City with state and country: "Springfield,IL,US"
        """
        params = {
            'appid': self.api_key,
            'units': 'metric'  # Use metric units (Celsius)
        }
        
        # Check if it's a zip/postal code (starts with a digit)
        if location and location[0].isdigit():
            # It's likely a zip/postal code
            params['zip'] = location
        else:
            # It's a city name
            params['q'] = location
        
        try:
            response = requests.get(self.base_url, params=params)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error fetching weather for {location}: {e}")
            return None
    
    def format_weather_data(self, location: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """Format weather data into a nice structure"""
        if not data:
            return {
                'location': location,
                'error': True,
                'message': f"Could not fetch weather for {location}"
            }
        
        # Convert temperature to both Celsius and Fahrenheit
        temp_c = data['main']['temp']
        temp_f = (temp_c * 9/5) + 32
        feels_like_c = data['main']['feels_like']
        feels_like_f = (feels_like_c * 9/5) + 32
        
        # Create a display name that includes city, state (if US), and country
        display_name = data['name']
        if 'state' in data.get('sys', {}):
            display_name += f", {data['sys']['state']}"
        display_name += f", {data['sys']['country']}"
        
        return {
            'location': location,
            'display_name': display_name,
            'city': data['name'],
            'country': data['sys']['country'],
            'description': data['weather'][0]['description'].capitalize(),
            'emoji': self.get_weather_emoji(data['weather'][0]['main']),
            'temperature': {
                'celsius': round(temp_c, 1),
                'fahrenheit': round(temp_f, 1)
            },
            'feels_like': {
                'celsius': round(feels_like_c, 1),
                'fahrenheit': round(feels_like_f, 1)
            },
            'humidity': data['main']['humidity'],
            'wind_speed': data['wind']['speed'],
            'coordinates': {
                'lat': data['coord']['lat'],
                'lon': data['coord']['lon']
            },
            'error': False
        }
    
    def get_weather_emoji(self, condition: str) -> str:
        """Return an emoji based on weather condition"""
        emoji_map = {
            'Clear': '☀️',
            'Clouds': '☁️',
            'Rain': '🌧️',
            'Drizzle': '🌦️',
            'Thunderstorm': '⛈️',
            'Snow': '❄️',
            'Mist': '🌫️',
            'Fog': '🌫️',
            'Haze': '🌫️'
        }
        return emoji_map.get(condition, '🌡️')
    
    def create_slack_message(self, weather_data: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Create a formatted Slack message with weather data"""
        # Use Mountain Time (handles DST automatically)
        mountain_tz = pytz.timezone('America/Denver')
        current_time = datetime.now(mountain_tz).strftime("%B %d, %Y at %I:%M %p %Z")
        
        blocks = [
            {
                "type": "header",
                "text": {
                    "type": "plain_text",
                    "text": "🌍 Daily Weather Report",
                    "emoji": True
                }
            },
            {
                "type": "context",
                "elements": [
                    {
                        "type": "mrkdwn",
                        "text": f"*Generated on:* {current_time}"
                    }
                ]
            },
            {
                "type": "divider"
            }
        ]
        
        # Add weather data for each location
        for data in weather_data:
            if data['error']:
                blocks.append({
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": f"❌ *{data['location']}*: {data['message']}"
                    }
                })
            else:
                # Include coordinates as a subtle reference
                location_text = f"{data['emoji']} *{data['display_name']}*"
                #if data['location'] != data['city']:
                    #location_text += f"\n_Search: {data['location']}_"
                
                blocks.append({
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": (
                            #f"{location_text}\n"
                            f"*Condition:* {data['description']}\n"
                            #f"*Temperature:* {data['temperature']['celsius']}°C ({data['temperature']['fahrenheit']}°F)\n"
                            f"*Temperature:* {data['temperature']['fahrenheit']}°F ({data['temperature']['celsius']}°C)\n"
                            #f"*Feels Like:* {data['feels_like']['celsius']}°C ({data['feels_like']['fahrenheit']}°F)\n"
                            f"*Feels Like:* {data['feels_like']['fahrenheit']}°F) ({data['feels_like']['celsius']}°C)\n"
                            f"*Humidity:* {data['humidity']}%\n"
                            f"*Wind Speed:* {data['wind_speed']} m/s\n"
                            #f"_📍 {data['coordinates']['lat']:.2f}, {data['coordinates']['lon']:.2f}_"
                        )
                    }
                })
            
            blocks.append({"type": "divider"})
        
        # Add footer
        blocks.append({
            "type": "context",
            "elements": [
                {
                    "type": "mrkdwn",
                    "text": "📊 _Data provided by OpenWeatherMap_"
                }
            ]
        })
        
        return {"blocks": blocks}
    
    def send_to_slack(self, message: Dict[str, Any]) -> bool:
        """Send the formatted message to Slack"""
        try:
            response = requests.post(self.slack_webhook, json=message)
            response.raise_for_status()
            print("✅ Successfully sent weather report to Slack!")
            return True
        except requests.exceptions.RequestException as e:
            print(f"❌ Error sending to Slack: {e}")
            return False
    
    def run(self, locations: List[str]) -> None:
        """Main method to fetch weather and send to Slack"""
        print(f"🔍 Fetching weather for {len(locations)} locations...")
        
        weather_data = []
        for location in locations:
            print(f"  - Fetching weather for {location}...")
            raw_data = self.get_weather(location)
            formatted_data = self.format_weather_data(location, raw_data)
            weather_data.append(formatted_data)
        
        print("📝 Creating Slack message...")
        slack_message = self.create_slack_message(weather_data)
        
        print("📤 Sending to Slack...")
        self.send_to_slack(slack_message)


def main():
    """Main function to run the weather bot"""
    # Get environment variables
    api_key = os.environ.get('OPENWEATHER_API_KEY')
    slack_webhook = os.environ.get('SLACK_WEBHOOK_URL')
    locations_str = os.environ.get('LOCATIONS', os.environ.get('CITIES', '10001,US;London,UK;Tokyo,JP;Sydney,AU;Paris,FR'))
    
    # Validate environment variables
    if not api_key:
        print("❌ Error: OPENWEATHER_API_KEY environment variable not set")
        sys.exit(1)
    
    if not slack_webhook:
        print("❌ Error: SLACK_WEBHOOK_URL environment variable not set")
        sys.exit(1)
    
    # Parse locations list (supports both comma and semicolon separators)
    # Use semicolon for clarity when mixing cities and zip codes
    if ';' in locations_str:
        locations = [loc.strip() for loc in locations_str.split(';')]
    else:
        locations = [loc.strip() for loc in locations_str.split(',')]
    
    print("🚀 Starting Weather Bot")
    print(f"📍 Locations to check: {', '.join(locations)}")
    
    # Create and run the bot
    bot = WeatherBot(api_key, slack_webhook)
    bot.run(locations)
    
    print("✨ Weather Bot completed!")


if __name__ == "__main__":
    main()