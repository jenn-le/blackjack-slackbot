Blackjack Slack Bot
===================

Spring 2017 CSE3353 Final Project

This is a slack bot that allows any number of players to play blackjack in an indicated channel. Players play against a dealer that doesn't follow typical rules for dealers.

[![Deploy my app to Heroku](https://www.herokucdn.com/deploy/button.png)](https://heroku.com/deploy?)

Installation Instructions:
--------------------------

1.	Fork this repo
2.	Press the button above to deploy to Heroku
3.	Create a bot in a slack channel
4.	Add the following env variables to Heroku: ADMIN_ID, BOT_ID, SLACK_BOT_TOKEN, DEALER_ID, CHANNEL_ID

Command List:
-------------

*!show [scoreboard/hand/balance]*: Displays the scoreboard in the desired channel or your hand in your DMs with blackjack

*!bet [num of coins]*: Placing a bet tells blackjack that you’re in on the next hand

*!play*: Once every player that wants to play has placed their bet, type this command to start the hand. At this point, blackjack will send each player their hands and send the entire table to the main channel

*!hit*: Asks blackjack to deal you another card

*!double*: This command is to double down. That means you will double your bet and stay after blackjack deals you one other card. This command can only be called during the first turn

*!stay*: If you are happy with your hand, tell blackjack that you are done for this hand

Once every player has either busted or stayed, blackjack will announce the results of the hand in the main channel
