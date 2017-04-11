import os
import re
from slackclient import SlackClient
from deck import Deck

class Dealer(object):
    def __init__(self):
        # The dealer's hand
        self.deck = Deck()
        self.hand = []
        self.players = []
        self.in_progress = False
        self.hard = False
        self.slack_client = SlackClient(os.environ.get('SLACK_BOT_TOKEN'))

    # The calling the general game functions
    def do(self, command, user, channel):
        # Functions for the general commands
        def show(self, command, user, channel):
            if len(command.split(' ')) < 2:
                response = "The valid commands for 'show' are scoreboard, balance and hand"
                self.slack_client.api_call("chat.postMessage", text=response,
                                            channel=channel, as_user=True)
            elif command.split(' ')[1] == "scoreboard":
                response = "*Scoreboard*\n===================================================\n"

                # Only sorts the scores if the players list isn't one person long
                if len(self.players) > 1:
                    for index in range(1,len(self.players)):
                        coins = self.players[index].get('balance')
                        position = index

                        while position > 0 and self.players[position-1].get('balance') > coins:
                            self.players[position - 1], self.players[position] = self.players[position], self.players[position - 1]
                            position -= 1

                    self.players = list(reversed(self.players))

                for player in self.players:
                    response += "\n" + player.get('name') + ": " + str(player.get('balance'))


                self.slack_client.api_call("chat.postMessage", text=response,
                                            channel=channel, as_user=True)
            elif command.split(' ')[1] == "balance":
                for player in self.players:
                    # Find the player's data
                    if player.get('id') == user:
                        response = "You have a total of " + str(player.get('balance')) + " coins"
                        self.slack_client.api_call("chat.postMessage", text=response,
                                                channel=user, as_user=True)
            elif command.split(' ')[1] == "hand":
                response = "Temp hand response"
                self.slack_client.api_call("chat.postMessage", text=response,
                                            channel=user, as_user=True)
            else:
                response = "The valid commands for 'show' are scoreboard, and hand"
                self.slack_client.api_call("chat.postMessage", text=response,
                                            channel=channel, as_user=True)

        # Saves your bet to indicate you'll play in the next game
        def bet(self, command, user, channel):
            if self.in_progress == true:
                response = "You cannot place a bet while there is hand going on"
            else:
                digits = re.compile('^\d*?')

                if len(command.split(' ')) != 2:
                    response = "Please enter the command in this format:\n!bet {coins}"
                elif digits.match(command.split(' ')[1]):
                    bet = int(command.split(' ')[1])
                    for player in self.players:
                        # Find the player's data
                        if player.get('id') == user:
                            if player.get('balance') >= bet:
                                player['bet'] = bet

                                response = player.get('name') + " has placed a bet of " + bet + " coins"
                                self.slack_client.api_call("chat.postMessage", text=response,
                                                            channel="C4TTHACG5", as_user=True)

                                response = "You have placed a bet of " + bet + " coins"
                                self.slack_client.api_call("chat.postMessage", text=response,
                                                            channel=user, as_user=True)
                            else:
                                response = "You do not have enough coins to bet that much"
                else:
                    response = "Enter in a valid number to bet"

            self.slack_client.api_call("chat.postMessage", text=response,
                                        channel=user, as_user=True)

        # def play(self, command, user, channel):
        #
        #
        # def hit(self, command, user, channel):
        #
        #
        # def double(self, command, user, channel):
        #
        #
        # def stay(self, command, user, channel):

        # Calling the appropriate function
        actions = {"!show": show,
                   "!bet": bet
                #    "!play": play,
                #    "!hit": hit,
                #    "!double": double,
                #    "!stay": stay
                  }

        actions[command.split(' ', 1)[0]](self, command, user, channel)


    # Game management functions
    # def end_hand(self):
    #
    #
    # def normal(self):
    #
    #
    # def hard(self):
