import os
import re
import json
from slackclient import SlackClient
from deck import Deck
from image_manager import handImage
from dealerbrain import DealerBrain

class Dealer(object):
    def __init__(self):
        # The dealer's hand
        self.dealer_brain = DealerBrain()
        self.deck = Deck()
        self.hand = []
        self.status = None
        self.hand_value = 0
        self.players = []
        self.in_progress = False
        self.hard = False
        self.main_channel = "C4TTHACG5"
        self.slack_client = SlackClient(os.environ.get('SLACK_BOT_TOKEN'))

    # The calling the general game functions
    def do(self, command, user, channel):
        # Functions for the general commands
        def show(self, command, user, channel):
            if len(command.split(' ')) < 2:
                response = "The valid commands for 'show' are scoreboard, balance, table, and hand"
                self.slack_client.api_call("chat.postMessage", text=response,
                                            channel=channel, as_user=True)
            elif command.split(' ')[1] == "scoreboard":
                response = "*Scoreboard*\n==============================================\n"

                # Only sorts the scores if the players list isn't one person long
                if len(self.players) > 1:
                    for index in range(1,len(self.players)):
                        coins = self.players[index].get('balance')
                        position = index

                        while position > 0 and self.players[position-1].get('balance') < coins:
                            self.players[position - 1], self.players[position] = self.players[position], self.players[position - 1]
                            position -= 1

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
            elif command.split(' ')[1] == "table":
                if len(command.split(' ')) != 2:
                    response = "The show table command doesn't take any arguments"
                    self.slack_client.api_call("chat.postMessage", text=response,
                                                channel=user, as_user=True)
                else:
                    self.show_table(False)

            elif command.split(' ')[1] == "hand":
                for player in self.players:
                    if player.get('bet') != None and player.get('id') == user:
                        self.show_hand(player, player.get('name') + "'s hand'", self.main_channel, True)
            else:
                response = "The valid commands for 'show' are scoreboard, and hand"
                self.slack_client.api_call("chat.postMessage", text=response,
                                            channel=channel, as_user=True)

        # Saves your bet to indicate you'll play in the next game
        def bet(self, command, user, channel):
            response = ""
            if self.in_progress == True:
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

                                response = player.get('name') + " has placed a bet of " + str(bet) + " coins"
                                self.slack_client.api_call("chat.postMessage", text=response,
                                                            channel=self.main_channel, as_user=True)

                                response = "You have placed a bet of " + str(bet) + " coins"
                                self.slack_client.api_call("chat.postMessage", text=response,
                                                            channel=user, as_user=True)

                                return
                            else:
                                response = "You do not have enough coins to bet that much"
                else:
                    response = "Enter in a valid number to bet"

            self.slack_client.api_call("chat.postMessage", text=response,
                                        channel=user, as_user=True)

        def play(self, command, user, channel):
            if len(command.split(' ')) != 1:
                response = "The play command doesn't take any arguments"
                self.slack_client.api_call("chat.postMessage", text=response,
                                            channel=user, as_user=True)
            elif self.in_progress == True:
                response = "Game already in progress"
                self.slack_client.api_call("chat.postMessage", text=response,
                                            channel=user, as_user=True)
            else:
                # New deck for each hand
                self.deck = Deck()
                self.in_progress = True
                self.deal()

        def hit(self, command, user, channel):
            for player in self.players:
                if player.get('bet') != None and player.get('id') == user:
                    if self.deck.empty():
                        self.deck = Deck()

                    if player.get('status') != None:
                        response = "You are done for this hand. Wait for every player to finish to see the results"
                        self.slack_client.api_call("chat.postMessage", text=response,
                                                    channel=user, as_user=True)
                        return

                    player.get('hand').append(self.deck.draw())

                    self.show_hand(player, "Your hand", player.get('id'), True)

                    player['hand_value'] = self.dealer_brain.calculate_value(player.get('hand'), player['status'])
                    print(player.get('status'))
                    self.check_end()

        def double(self, command, user, channel):
            for player in self.players:
                if player.get('bet') != None and player.get('id') == user:
                    if player.get('status') != None:
                        response = "You are done for this hand. Wait for every player to finish to see the results"
                        self.slack_client.api_call("chat.postMessage", text=response,
                                                    channel=user, as_user=True)
                        return

                    if len(player.get('hand')) > 2:
                        response = "You can no longer double down. Just hit or stay"
                        self.slack_client.api_call("chat.postMessage", text=response,
                                                    channel=user, as_user=True)
                        return

                    if self.deck.empty():
                        self.deck = Deck()

                    player.get('hand').append(self.deck.draw())
                    player['bet'] = player.get('bet') * 2


                    response = "Your bet is now " + str(bet) + " coins"
                    self.slack_client.api_call("chat.postMessage", text=response,
                                                channel=user, as_user=True)
                    self.show_hand(player, "Your hand", player.get('id'), True)

                    player['hand_value'] = self.dealer_brain.calculate_value(player.get('hand'), player['status'])
                    self.check_end()

        def stay(self, command, user, channel):
            for player in self.players:
                if player.get('bet') != None and player.get('id') == user:
                    player['status'] = "stayed"

                    self.check_end()

        # Calling the appropriate function
        actions = {"!show": show,
                   "!bet": bet,
                   "!play": play,
                   "!hit": hit,
                   "!double": double,
                   "!stay": stay
                  }

        actions[command.split(' ', 1)[0]](self, command, user, channel)

    # Deals first two cards to each player that has made a bet and sends the necessary messages
    def deal(self):
        if self.deck.empty():
            self.deck = Deck()

        self.hand.append(self.deck.draw())
        self.hand.append(self.deck.draw())

        self.hand_value = self.dealer_brain.calculate_value(self.hand, self.status)

        for player in self.players:
            if player.get('bet') != None:
                if self.deck.empty():
                    self.deck = Deck()

                player.get('hand').append(self.deck.draw())

                if self.deck.empty():
                    self.deck = Deck()

                player.get('hand').append(self.deck.draw())

                player['hand_value'] = self.dealer_brain.calculate_value(player.get('hand'), player['status'])
                self.show_hand(player, "Your hand", player.get('id'), True)

        # After dealing each player their hand, show the entire table
        self.show_table(False)

    # Show indicated player's hand
    def show_hand(self, player, title, channel, show_all):
        fallback = ""
        for card in player.get('hand'):
            fallback += card + " "

        temp_hand = player.get('hand')[:]
        if show_all == False:
            temp_hand[1] = "back"

        hand = [{"fallback": fallback,
                "title": title,
                "image_url": handImage(temp_hand)
               }]

        self.slack_client.api_call("chat.postMessage", attachments=hand,
                                    channel=channel, as_user=True)

    # Shows the hands of everyone, hides the 2nd card if it is not the end of the hand
    def show_table(self, end):
        response = "*The current table:*"
        self.slack_client.api_call("chat.postMessage", text=response,
                                    channel=self.main_channel, as_user=True)

        # Showing the dealer's hand
        fallback = ""
        for card in self.hand:
            fallback += card + " "

        temp_hand = self.hand[:]
        if end == False:
            temp_hand[1] = "back"

        hand = [{"fallback": fallback,
                "title": "Dealer's hand",
                "image_url": handImage(temp_hand)
               }]

        self.slack_client.api_call("chat.postMessage", attachments=hand,
                                channel=self.main_channel, as_user=True)

        for player in self.players:
            if player.get('bet') != None:
                self.show_hand(player, player.get('name') + "'s hand'", self.main_channel, end)

    def check_end(self):
        ended = True

        for player in self.players:
            if player.get('bet') != None and player.get('status') == None:
                ended = False

        if ended == True:
            self.in_progress = False
            response = "The hand has ended temp response"
            self.slack_client.api_call("chat.postMessage", text=response,
                                        channel=self.main_channel, as_user=True)

    def reset(self):
        self.deck = Deck()
        self.hand = []
        self.players = []
        self.in_progress = False
        self.hard = False
