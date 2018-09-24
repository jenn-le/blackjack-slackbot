# Blackjack Slackbot

This project was reverted to working state with the docker updates because I won't be working on it anymore.

## Environment Variables

These must be stored in a file called ".env" for the bot to work.

SLACK_BOT_TOKEN: This can be found when you have created a bot for your channel and
installed it. It should be under installed app settings.

ADMIN_ID: This must be set for admin functionality. IDs can be found be modifying set_slack_info.py.

## Starting the Bot

This app can be deployed anywhere with docker and docker-compose. Just run the following commands within the top-level folder.

`docker build -t casinobot .` - Builds the docker image if you want to make any changes, otherwise you can just use the next command.

`docker run --env-file .env --name casinobot thakugan/casinobot` - Creates and runs a container named 'casinobot' using the image located at 'thakugan/casinobot'. If you had built a different image, just replace it here. Add the `-d` flag to run the container in detached mode.

## Game Commands

### General

`join [game]`: This adds you to the player list for the specified game. At this point, follow the prompts to play.
