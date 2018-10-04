# Blackjack Slackbot
This project was reverted to working state with the docker updates so I have an easier time refactoring.

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

`!show [scoreboard/hand/balance]`: Displays the scoreboard in the desired channel or your hand in your DMs with blackjack

`!bet [num of coins]`: Placing a bet tells blackjack that you’re in on the next hand

`!play`: Once every player that wants to play has placed their bet, type this command to start the hand. At this point, blackjack will send each player their hands and send the entire table to the main channel

`!hit`: Asks blackjack to deal you another card

`!double`: This command is to double down. That means you will double your bet and stay after blackjack deals you one other card. This command can only be called during the first turn

`!stay`: If you are happy with your hand, tell blackjack that you are done for this hand

Once every player has either busted or stayed, blackjack will announce the results of the hand in the main channel
