import requests # pip install requests
import os # built-in
from dotenv import load_dotenv # pip install python-dotenv

load_dotenv() # load environment variables from .env file

class VoiceFlowInteractor:
    def __init__(self):
        self.api_key = os.getenv("VF_API_KEY")
        self.users = set()
    
    def send_request(self, user_id, request):
        response = requests.post(
            f'https://general-runtime.voiceflow.com/state/user/{user_id}/interact',
            json={ 'request': request },
            headers={ 'Authorization': self.api_key },
        )
        return response.json()

    def user_interact(self, user_id, text):
        if user_id not in self.users: # if a user woke up the voiceflow dialog, create a new user and start the conversation
            if "voiceflow" in text.lower():
                self.users.add(user_id)
                return self.send_request(user_id, {'type': 'launch'})
            else:
                return False
        else:
            return self.send_request(user_id, {'type': 'text', 'payload': text})
        
    def parse_response(self, user_id, response):
        for trace in response:
            if trace['type'] == 'speak' or trace['type'] == 'text':
                yield trace['payload']['message'].replace("\n"," ")
            elif trace['type'] == 'end':
                self.users.remove(user_id)
                yield False



if __name__ == "__main__":
    user_id = "test_user"
    interactor = VoiceFlowInteractor()
    alive = True
    while alive:
        text = input("Enter text: ")
        response = interactor.user_interact(user_id, text)
        for message in interactor.parse_response(user_id, response):
            if message:
                print(message)
            else:
                alive = False