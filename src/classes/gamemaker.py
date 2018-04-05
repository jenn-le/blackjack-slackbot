import os
from .player import Player
from slackclient import SlackClient


class GameMaker(object):
    """ GameMaker class handles state for the application """
    _state = None

    def __init__(self):
        if not self._state:
            self._state = {
                # instantiate Slack
                "slack_client": SlackClient(
                    os.environ.get('SLACK_BOT_TOKEN')),

                "dealers": {
                    "blackjack": None
                }
            }

            self._state["players"] = self._add_players()

    # ------------- APPLICATION DATA ------------- #
    @property
    def slack_client(self):
        """ Gives other modules access to the slack client """
        return self._state["slack_client"]

    @property
    def dealers(self):
        """ Gives other modules access to the dealer data """
        return self._state["dealers"]

    @property
    def players(self):
        """ Gives other modules access to the player data """
        return self._state["players"]

    # ------------- PUBLIC FUNCTIONS ------------- #
    def send_message(self, message, channel=os.environ.get('CHANNEL_ID')):
        """ Interface for posting a message. Default channel is casino """
        self.slack_client.api_call("chat.postMessage", text=message,
                                   channel=channel, as_user=True)

    # ------------ PRIVATE FUNCTIONS ------------- #
    def _add_players(self):
        """ ATM this application is volatile so new data is added each time.
            This function goes through all the users and adds them to the 
            player list with a default of 50 coins.
        """
        players = []
        api_call = self.slack_client.api_call("users.list")

        if api_call.get('ok'):

            # Retrieve all users and add them to the list
            users = api_call.get('members')
            for person in users:
                # Make sure we don't add our bot to the list
                if 'name' in person and person.get('name') is not 'casino_bot':
                    players.append(
                        Player(person.get('name'), person.get('id'), 500)
                    )

                    self.send_message(
                        "Added " + person.get('name') + " to the players list"
                    )

        return players
