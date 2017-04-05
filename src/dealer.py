import os
from slackclient import SlackClient

class Dealer(object):
    def __init__(self):
        # The dealer's hand
        self.hand = []
        self.players = []
        self.table = []
        self.in_progress = False
        self.slack_client = SlackClient(os.environ.get('SLACK_BOT_TOKEN'))

    # # The calling the general game functions
    # def do(self, command, user, channel):
    #     # Functions for the general commands
    #     def show(self, command, user, channel):
    #
    #
    #     def bet(self, command, user, channel):
    #
    #
    #     def play(self, command, user, channel):
    #
    #
    #     def hit(self, command, user, channel):
    #
    #
    #     def double(self, command, user, channel):
    #
    #
    #     def stay(self, command, user, channel):
    #
    #     # Calling the appropriate function
    #     actions = {"show": show,
    #                "bet": bet,
    #                "play": play,
    #                "hit": hit,
    #                "double": double,
    #                "stay": stay
    #               }
    #
    #     actions[command.split(' ', 1)[0]](self, command, user, channel)
    #
    #
    # # Game management functions
    # def end_turn(self):
    #
    #
    # def end_hand(self):
