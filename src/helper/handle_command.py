import os

gm_commands = {

}


def handle_command(gm, command, user, channel):
    if user != os.environ.get('BOT_ID'):
        response = user + " said: " + command + " in channel: " + channel
        gm.send_message(response, channel)
