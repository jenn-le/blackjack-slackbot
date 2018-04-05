import os
from slackclient import SlackClient


BOT_NAME = 'casino_bot'
CHANNEL_NAME = 'casino'
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


def set_channel_id():
    api_call = slack_client.api_call("channels.list")

    if api_call.get('ok'):

        # retrieve all channels so we can get the id for the casino channel
        channels = api_call.get('channels')

        for channel in channels:
            if 'name' in channel and channel.get('name') == CHANNEL_NAME:
                os.environ['CHANNEL_ID'] = channel.get('id')
                print("Channel ID for '" +
                      channel['name'] + "' is " + channel.get('id'))

                return

        # if the channel doesn't exist, create it
        api_call = slack_client.api_call("channels.create", name="casino")
        os.environ['CHANNEL_ID'] = api_call.get('channel').get('id')

    print("Could not find bot user with the name " + BOT_NAME)


if __name__ == "__main__":
    print(os.environ.get('SLACK_BOT_TOKEN'))
    set_bot_id()
