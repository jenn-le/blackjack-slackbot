import os
import re
from slackclient import SlackClient

class Admin(object):
    def __init__(self, dealer):
        # The dealer's hand
        self.dealer = dealer
        self.slack_client = SlackClient(os.environ.get('SLACK_BOT_TOKEN'))

    # Admin commands
    def admin_do(self, command):
        def addplayer(self, command):
            api_call = self.slack_client.api_call("users.list")
            if api_call.get('ok'):

                # retrieve all users so we can add the desired ones to the players list
                users = api_call.get('members')
                for user in users:
                    if 'name' in user and user.get('name') in command:
                        exists = False
                        for player in self.dealer.players:

                            # Send a message if the player is already in the list
                            if player.get('name') == user.get('name'):
                                response = user.get('name') + " has already been added to the player list."
                                self.slack_client.api_call("chat.postMessage", text=response,
                                                            channel="D4TU5BYN6", as_user=True)
                                exists = True

                        # If the player wasn't in the list, add them
                        if exists == False:
                            self.dealer.players.append({"name": user.get('name'),
                                                        "id": user.get('id'),
                                                        "balance": 500,
                                                        "hand": []
                                                        })

                            response = user.get('name') + " has been added to the player list"
                            self.slack_client.api_call("chat.postMessage", text=response,
                                                        channel="D4TU5BYN6", as_user=True)

        def change_balance(self, command):
            response = "This person isn't in the player list"
            digits = re.compile('^\d*?')

            if p.match(command.split(' ')[3]):
                for player in self.dealer.players:
                    if player.get('name') == command.split(' ')[2]:
                        player['balance'] += int(command.split(' ')[3])

                        changed = "added"
                        if int(command.split(' ')[3]) < 0:
                            changed = "removed"

                        response = command.split(' ')[3] + " coins have been " + \
                                    changed + " to " + player.get('name') + "\'s account"
            else:
                response = "Enter in a valid number to change the balance by"

            self.slack_client.api_call("chat.postMessage", text=response,
                                        channel="D4TU5BYN6", as_user=True)


        # Calling the appropriate function
        actions = {"addplayer": addplayer,
                   "change_balance": change_balance
                  }

        actions[command.split(' ')[1]](self, command)
