import requests # pip install requests
import os # built-in
from dotenv import load_dotenv # pip install python-dotenv

# override the environment variables with the ones in the .env file
del os.environ['VF_API_KEY']
load_dotenv()

class VoiceFlowInteractor: # A class to interact with the VoiceFlow API
    def __init__(self):
        self.api_key = os.getenv("VF_API_KEY")
        self.users = set()
    
    def send_request(self, user_id, request):
        response = requests.post(
            f'https://general-runtime.voiceflow.com/state/user/{user_id}/interact',
            json={ 'request': request },
            headers={ 'Authorization': self.api_key, 'versionID': 'production', },
        )
        return response.json()

    def user_interact(self, user_id, text):
        if user_id not in self.users: # if a user woke up the voiceflow dialog, create a new user and start the conversation
            if "voiceflow" in text.lower():
                self.users.add(user_id)
                return self.send_request(user_id, {'type': 'launch'}) # send a launch request to the voiceflow API to start the conversation
            else:
                return False
        else: # if the user is already in the conversation, send a text request to the voiceflow API
            return self.send_request(user_id, {'type': 'text', 'payload': text})
        
    def parse_response(self, user_id, response): # extract voiceflow's answers from the response
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