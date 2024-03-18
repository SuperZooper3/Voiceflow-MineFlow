from mcChatMonitor import ChatLogMonitor
from mcrconSender import RconSender
from voiceflow import VoiceFlowInteractor

import time
import json

# Start the chat monitor, rcon sender, and voiceflow interactor
monitor = ChatLogMonitor()
monitor.start_monitor()
rcon = RconSender()
interactor = VoiceFlowInteractor()
messages_to_send = {}
alive = True

# Send a message to all players that the voiceflow integration is active
rcon.send("tellraw @a [\"\",{\"text\":\"Voiceflow is now active! Type '!stop' to stop it.\",\"color\":\"dark_aqua\"}]")

print("Starting...")

while alive:
    # Get messages from in-game chat
    for user, message in monitor.yield_player_message():
        # Check if user wants to stop the voiceflow integration
        if "!stop" in message.lower():
            alive = False
            break
        
        # Add the message to the list of messages to send to voiceflow
        print(f"{user}: {message}")
        messages_to_send[user] = messages_to_send.get(user, []) + [message]
    
    for user, messages in messages_to_send.items():
        # Group all of the player's messages into one message
        grouped_message = " ".join(messages)
        if len(grouped_message) == 0:
            continue

        # Send the message to voiceflow and get the response
        response = interactor.user_interact(user, grouped_message)
        if response:
            for message in interactor.parse_response(user, response):
                if message:
                    # Check if the message is a command, and if so, run it
                    if message.startswith("COMMAND: "):
                        raw_command = message.replace("COMMAND: ","").replace("/","")
                        if "`" in raw_command:
                            raw_command = raw_command.split("`")[1]
                        command = f"execute as {user} at {user} run {raw_command}"
                        print(f"Sending command: {command}")
                        print(rcon.send(command))

                    # Otherwise, send the message to the user
                    else:
                        print(message)
                        message_command = f"tellraw {user} {json.dumps(['', {'text': 'Voiceflow: ', 'color': 'dark_aqua'}, {'text': message}])}"
                        print(rcon.send(message_command))
                else:
                    pass
    
    # Clear the list of messages to send
    messages_to_send = {}

    time.sleep(0.5)
    # print("Looping...")

# Confrimg stop and close the connections
print("Stopping...")
rcon.send("tellraw @a [\"\",{\"text\":\"Voiceflow is now inactive.\",\"color\":\"dark_aqua\"}]")
monitor.stop_monitor()
rcon.disconnect()