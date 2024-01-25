from mcChatMonitor import ChatLogMonitor
from mcrconSender import RconSender
from voiceflow import VoiceFlowInteractor

import time
import json

monitor = ChatLogMonitor()
monitor.start_monitor()
rcon = RconSender()
interactor = VoiceFlowInteractor()
messages_to_send = {}
while True:
    for user, message in monitor.yield_player_message():
        print("Got message")
        print(f"{user}: {message}")
        messages_to_send[user] = messages_to_send.get(user, []) + [message]
    
    for user, messages in messages_to_send.items():
        grouped_message = " ".join(messages)
        if len(grouped_message) == 0:
            continue
        response = interactor.user_interact(user, grouped_message)
        if response:
            for message in interactor.parse_response(user, response):
                if message:
                    print(message)
                    print(rcon.send(f"tellraw {user} {json.dumps({'text': message})}"))
                    time.sleep(0)
                else:
                    pass
    
    messages_to_send = {}

    time.sleep(0.5)
    print("Looping...")