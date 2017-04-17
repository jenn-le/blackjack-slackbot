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
        self.players = []
        self.players.append({"name": "Dealer",
                             "id": "U4TS5RXU3",
                             "balance": 500,
                             "bet": 50,
                             "hand": [],
                             "status": None,
                             "hand_value": 0
                             })
        self.in_progress = False
        self.hard = False
        self.main_channel = "C4TTHACG5"
        self.slack_client = SlackClient(os.environ.get('SLACK_BOT_TOKEN'))

    # The calling the general game functions
    def do(self, command, user, channel):
        # Functions for the general commands
        def show(self, command, user, channel):
            if len(command.split(' ')) < 2:
                self.message_user("The valid commands for 'show' are scoreboard, balance, table, and hand", channel)
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

                self.message_user(response, channel)

            elif command.split(' ')[1] == "balance":
                for player in self.players:
                    # Find the player's data
                    if player.get('id') == user:
                        self.message_user("You have a total of " + str(player.get('balance')) + " coins", user)
            elif command.split(' ')[1] == "table":
                if len(command.split(' ')) != 2:
                    self.message_user("The show table command doesn't take any arguments", channel)
                else:
                    self.show_table(False)

            elif command.split(' ')[1] == "hand":
                for player in self.players:
                    if player.get('bet') != None and player.get('id') == user:
                        self.show_hand(player, player.get('name') + "'s hand'", player.get('id'), True)
            else:
                self.message_user("The valid commands for 'show' are scoreboard, balance, table, and hand", channel)

        # Saves your bet to indicate you'll play in the next game
        def bet(self, command, user, channel):
            if self.in_progress == True:
                self.message_user("You cannot place a bet while there is hand going on", user)
            else:
                digits = re.compile('^\d*?')

                if len(command.split(' ')) != 2:
                    self.message_user("Please enter the command in this format:\n!bet {coins}", user)
                elif digits.match(command.split(' ')[1]):
                    bet = int(command.split(' ')[1])

                    # Find the player's data
                    for player in self.players:
                        if player.get('id') == user:
                            if player.get('balance') >= bet:
                                player['bet'] = bet
                                self.message_channel(player.get('name') + " has placed a bet of " + str(bet) + " coins")
                                self.message_user("You have placed a bet of " + str(bet) + " coins", user)
                                return
                            else:
                                self.message_user("You do not have enough coins to bet that much", user)
                else:
                    self.message_user("Enter in a valid number to bet", user)

        def play(self, command, user, channel):
            if self.in_progress == True:
                self.message_user("Game already in progress", user)
            else:
                # New deck for each hand
                self.deck = Deck()
                self.in_progress = True
                self.deal()

        def hit(self, command, user, channel):
            if self.in_progress == False:
                self.message_user("There is no game going on right now", user)
                return
            for player in self.players:
                if player.get('bet') != None and player.get('id') == user:
                    if self.deck.empty():
                        self.deck = Deck()

                    if player.get('status') != None:
                        self.message_user("You are done for this hand. Wait for every player to finish to see the results", user)
                        return

                    player.get('hand').append(self.deck.draw())

                    self.show_hand(player, "Your hand", player.get('id'), True)

                    player['hand_value'], player['status'], response = self.dealer_brain.calculate_value(player.get('hand'))
                    if response != None:
                        self.message_user(response, user)

            self.check_end()

        def double(self, command, user, channel):
            if self.in_progress == False:
                self.message_user("There is no game going on right now", user)
                return
            for player in self.players:
                if player.get('bet') != None and player.get('id') == user:
                    if player.get('status') != None:
                        self.message_user("You are done for this hand. Wait for every player to finish to see the results", user)
                        return

                    if len(player.get('hand')) > 2:
                        self.message_user("You can no longer double down. Just hit or stay", user)
                        return

                    if self.deck.empty():
                        self.deck = Deck()

                    player.get('hand').append(self.deck.draw())
                    player['bet'] = player.get('bet') * 2

                    self.message_user("Your bet is now " + str(player.get('bet')) + " coins", user)
                    self.show_hand(player, "Your hand", player.get('id'), True)
                    player['status'] = "stayed"

                    player['hand_value'], player['status'], response = self.dealer_brain.calculate_value(player.get('hand'))
                    if response != None:
                        self.message_user(response, user)
            self.check_end()

        def stay(self, command, user, channel):
            if self.in_progress == False:
                self.message_user("There is no game going on right now", user)

                return
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
        for player in self.players:
            if player.get('bet') != None:
                if self.deck.empty():
                    self.deck = Deck()

                player.get('hand').append(self.deck.draw())

                if self.deck.empty():
                    self.deck = Deck()

                player.get('hand').append(self.deck.draw())

                player['hand_value'], player['status'], response = self.dealer_brain.calculate_value(player.get('hand'))
                if response != None:
                    self.message_user(response, user)
                self.show_hand(player, "Your hand", player.get('id'), True)

        self.check_end()

        # After dealing each player their hand, show the entire table
        self.show_table(False)

    # Show indicated player's hand
    def show_hand(self, player, title, channel, show_all):
        temp_hand = player.get('hand')[:]
        if show_all == False:
            temp_hand[1] = "back"

        hand = [{"fallback": player.get('name') + "'s hand'",
                "title": title,
                "image_url": handImage(temp_hand)
               }]

        self.slack_client.api_call("chat.postMessage", attachments=hand,
                                    channel=channel, as_user=True)

    # Shows the hands of everyone, hides the 2nd card if it is not the end of the hand
    def show_table(self, end):
        self.message_channel("*The current table:*")
        for player in self.players:
            if player.get('bet') != None:
                self.show_hand(player, player.get('name') + "'s hand'", self.main_channel, end)

    def check_end(self):
        ended = True

        for player in self.players:
            if player.get('bet') != None and player.get('name') != "Dealer":
                if player.get('bet') != None and player.get('status') == None:
                    ended = False

        if ended == True:
            self.end(self.hard)

    def end(self, hard):
        for player in self.players:
            if player.get('name') == "Dealer":
                while player.get('status') == None:
                    decision = self.dealer_brain.calculate_decision(self.players, hard)

                    if decision == 0:
                        player['status'] = "stayed"
                    elif decision == 1:
                        player.get('hand').append(self.deck.draw())
                        player['hand_value'], player['status'], response = self.dealer_brain.calculate_value(player.get('hand'))

        self.show_table(True)
        self.calculate_scores()
        self.in_progress = False
        for player in self.players:
            if player.get('name') != "Dealer":
                player['bet'] = None
            player['hand'] = []
            player['status'] = None
            player['hand_value'] = 0

    def calculate_scores(self):
        for Dealer in self.players:
            if Dealer.get('name') == "Dealer":
                for player in self.players:
                    if player.get('name') != "Dealer":
                        if self.is_loss(player, Dealer):
                            player['balance'] -= player.get('bet')
                            Dealer['balance'] += player.get('bet')
                            self.message_channel(player.get('name') + " loses " + str(player.get('bet')) + " coins")
                        elif player.get('status') == "five-card" and Dealer.get('status') != "five-card":
                            player['balance'] += player.get('bet') * 4
                            Dealer['balance'] -= player.get('bet') * 4
                            self.message_channel(player.get('name') + " wins " + str(player.get('bet') * 4) + " coins")
                        elif player.get('status') == "blackjack" and Dealer.get('status') != "blackjack":
                            player['balance'] += player.get('bet') * 3
                            Dealer['balance'] -= player.get('bet') * 3
                            self.message_channel(player.get('name') + " wins " + str(player.get('bet') * 3) + " coins")
                        elif player.get('status') == "21" and Dealer.get('status') != "21":
                            player['balance'] += player.get('bet') * 2
                            Dealer['balance'] -= player.get('bet') * 2
                            self.message_channel(player.get('name') + " wins " + str(player.get('bet') * 2) + " coins")
                        elif player.get('hand_value') > Dealer.get('hand_value'):
                            player['balance'] += player.get('bet')
                            Dealer['balance'] -= player.get('bet')
                            self.message_channel(player.get('name') + " wins " + str(player.get('bet')) + " coins")
                        else:
                            self.message_channel(player.get('name') + " doesn't lose any coins")

        self.message_channel("The hand is over. Make a bet to join the next hand")

    def is_loss(self, player, Dealer):
        return ( (Dealer.get('status') == "five-card" and player.get('status') != "five-card")
            or (player.get('status') != "blackjack" and Dealer.get('status') == "blackjack")
            or player.get('hand_value') < Dealer.get('hand_value') and Dealer.get('status') != "busted"
            or player.get('status') == "busted" )

    def message_channel(self, response):
        self.slack_client.api_call("chat.postMessage", text=response,
                                    channel=self.main_channel, as_user=True)

    def message_user(self, response, user):
        self.slack_client.api_call("chat.postMessage", text=response,
                                    channel=user, as_user=True)

    def reset(self):
        self.deck = Deck()
        self.players = []
        self.players.append({"name": "Dealer",
                             "id": "U4TS5RXU3",
                             "balance": 500,
                             "bet": 50,
                             "hand": [],
                             "status": None,
                             "hand_value": 0
                             })
        self.in_progress = False
        self.hard = False
