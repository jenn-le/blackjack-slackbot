import os
import time
from slackclient import SlackClient

# possible commands, dealer will handle what to do with them
actions = ['show',
           'play',
           'bet',
           'hit',
           'double',
           'stay']

# instantiate Slack
slack_client = SlackClient(os.environ.get('SLACK_BOT_TOKEN'))

def handle_command(command, channel):
    response = "Not sure what you mean. Please refer to the pinned post for " + \
                "instructions on how to play."

    # Show command - will show the scoreboard, your chips, your hand, or the current
    # table based on the 2nd part of the command
    if command.split(' ', 1)[0] in actions:
        response = "The command is: " + command.split(' ', 1)[0]
    slack_client.api_call("chat.postMessage", channel=channel,
                          text=response, as_user=True)


def parse_slack_output(slack_rtm_output):
    output_list = slack_rtm_output
    if output_list and len(output_list) > 0:
        for output in output_list:
            if output and 'text' in output:
                return output['text'], output['channel']
    return None, None


def main():
    READ_WEBSOCKET_DELAY = 1 # 1 second delay between reading from firehose
    if slack_client.rtm_connect():
        print("StarterBot connected and running!")
        while True:
            command, channel = parse_slack_output(slack_client.rtm_read())
            if command and channel:
                handle_command(command, channel)
            time.sleep(READ_WEBSOCKET_DELAY)
    else:
        print("Connection failed. Invalid Slack token or bot ID?")


if __name__ == '__main__':
    main()
