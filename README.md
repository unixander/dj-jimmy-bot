# DJ Jimmy Bot

## Description

Just sample application for getting acquanted with the telegram bots.

#### Supported commands

- Triggers on words `hello`, `hi`, `what's the weather?`, `ping`
- `/start` - start interaction with the bot
- `/hello` - just a greeting
- `/weather`, `/weather New York` - get weather info for the default list of the cities or for the specific city.

## Deploy

- Go to the BotFather in telegram and create new bot. 
- On [openweathermap.org](https://openweathermap.org) create new token for weather commands.
- In `docker-compose.yml` set `BOT_TOKEN` and `WEATHER_TOKEN`
- ```docker-compose up```