# Casino Slackbot

This project is currently being refactored and expaned. The first release ready build
will come with an updated README.

## Environment Variables

These must be stored in a file called ".env" for the bot to work.

SLACK_BOT_TOKEN: This can be found when you have created a bot for your channel and
installed it. It should be under installed app settings.

## Starting the Bot

This app can be deployed anywhere with docker and docker-compose. Just run the following commands within the top-level folder.

`docker-compose up -d` - Starts the bot
`docker-compose run casinobot python set_slack_info.py` - This only needs to be run the first time, it finds and stores all the info the bot needs
