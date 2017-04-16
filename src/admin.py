import os
import re
from slackclient import SlackClient

class Admin(object):
    def __init__(self, dealer):
        # The dealer's hand
        self.dealer = dealer
        self.slack_client = SlackClient(os.environ.get('SLACK_BOT_TOKEN'))

    # Admin commands
    def admin_do(self, command, user):
        def addplayer(self, command, user):
            api_call = self.slack_client.api_call("users.list")
            if api_call.get('ok'):

                # retrieve all users so we can add the desired ones to the players list
                users = api_call.get('members')
                for person in users:
                    if 'name' in person and person.get('name') in command:
                        exists = False
                        for player in self.dealer.players:

                            # Send a message if the player is already in the list
                            if player.get('name') == person.get('name'):
                                self.dealer.message_user(person.get('name') + " has already been added to the player list.", user)
                                exists = True

                        # If the player wasn't in the list, add them
                        if exists == False:
                            self.dealer.players.append({"name": person.get('name'),
                                                        "id": person.get('id'),
                                                        "balance": 500,
                                                        "bet": None,
                                                        "hand": [],
                                                        "status": None,
                                                        "hand_value": 0
                                                        })

                            self.dealer.message_user(person.get('name') + " has been added to the player list", user)

        def change_balance(self, command, user):
            response = "This person isn't in the player list"
            digits = re.compile('^\d*?')

            if len(command.split(' ')) != 4:
                response = "Please enter the command in this format:\n!admin change_balance {player_name} {coins}"
            elif digits.match(command.split(' ')[3]):
                for player in self.dealer.players:
                    if player.get('name') == command.split(' ')[2]:
                        player['balance'] += int(command.split(' ')[3])

                        changed = "added to "
                        if int(command.split(' ')[3]) < 0:
                            changed = "removed from "

                        response = command.split(' ')[3] + " coins have been " + \
                                    changed + player.get('name') + "\'s account"
            else:
                response = "Enter in a valid number to change the balance by"

            self.dealer.message_user(response, user)

        def normal(self, command, user):
            if self.dealer.hard == False:
                self.dealer.message_user("Game difficulty is already set to normal", user)
            else:
                self.dealer.hard = False
                self.dealer.message_user("Game difficulty is now set to normal", user)

        def hard(self, command, user):
            if self.dealer.hard == True:
                self.dealerl.message_user("Game difficulty is already set to hard", user)
            else:
                self.dealer.hard = True
                self.dealer.message_user("Game difficulty is now set to hard", user)

        def reset(self, command, user):
            self.dealer.reset()
            self.dealer.message_user("The game has been reset", user)

        # Calling the appropriate function
        actions = {"addplayer": addplayer,
                   "change_balance": change_balance,
                   "normal": normal,
                   "hard": hard,
                   "reset": reset
                  }

        actions[command.split(' ')[1]](self, command, user)
