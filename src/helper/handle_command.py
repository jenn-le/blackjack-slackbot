def handle_command(slack_client, command, user, channel):
    response = "You said: " + command
    slack_client.api_call("chat.postMessage", channel=channel,
                          text=response, as_user=True)
