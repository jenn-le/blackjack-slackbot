import os
from slackclient import SlackClient


BOT_NAME = 'casino_bot'
slack_client = SlackClient(os.environ.get('SLACK_BOT_TOKEN'))


def set_bot_id():
    api_call = slack_client.api_call("users.list")

    if api_call.get('ok'):

        # retrieve all users so we can find our bot
        users = api_call.get('members')

        for user in users:
            if 'name' in user and user.get('name') == BOT_NAME:
                os.environ['BOT_ID'] = user.get('id')
                print("Bot ID for '" + user['name'] + "' is " + user.get('id'))
                return

    print("Could not find bot user with the name " + BOT_NAME)


if __name__ == "__main__":
    print(os.environ.get('SLACK_BOT_TOKEN'))
    set_bot_id()
