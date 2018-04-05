import os
import time
from classes.gamemaker import GameMaker
from helper.handle_command import handle_command

gm = GameMaker()


def parse_slack_output(slack_rtm_output):
    output_list = slack_rtm_output

    if output_list and len(output_list) > 0:
        for output in output_list:
            if output and 'text' in output:
                output['text'] = output['text'].lower()
                return output['text'], output['user'], output['channel']

    return None, None, None


def main():
    READ_WEBSOCKET_DELAY = 1  # 1 second delay between reading from firehose

    if gm.slack_client.rtm_connect():
        print("Casino Bot connected and running!")
        while True:
            command, user, channel = parse_slack_output(
                gm.slack_client.rtm_read())
            if command and channel:
                handle_command(gm, command, user, channel)
            time.sleep(READ_WEBSOCKET_DELAY)
    else:
        print("Connection failed. Invalid Slack token or bot ID?")


if __name__ == '__main__':
    main()
