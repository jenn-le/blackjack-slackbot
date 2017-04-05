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

    # Admin commands
    def addplayer(self, command):
        api_call = slack_client.api_call("users.list")
        if api_call.get('ok'):

            # retrieve all users so we can add the desired ones to the players list
            users = api_call.get('members')
            for user in users:
                if 'name' in user and user.get('name') in command:
                    for player in self.players:

                        # Send a message if the player is already in the list
                        if player.get('name') == user.get('name'):
                            response = user.get('name') + " has already been added to the player list."
                            slack_client.api_call("chat.postMessage", text=response, as_user=True)
                            continue

                    # If the player wasn't in the list, add them
                    self.players.append({"name": user.get('name'),
                                         "id": user.get('id'),
                                         "balance": 500,
                                         "hand": []
                                        })

                    response = user.get('name') + " has been added the player list."
                    slack_client.api_call("chat.postMessage", text=response, as_user=True)

    def admin_do(self, command):
        actions = {"addplayer": addplayer
                #    "change_balance": change_balance
                  }

        actions[command.split(' ', 1)[0]](self, command)

    # def change_balance(self, command):
    #
    #
    # The calling the general functions
    # def do(self, command, user, channel):
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
    # # Functions for the general commands
    # def show(self, command, user, channel):
    #
    #
    # def bet(self, command, user, channel):
    #
    #
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
    #
    #
    # # Game management functions
    # def end_turn(self):
    #
    #
    # def end_hand(self):
