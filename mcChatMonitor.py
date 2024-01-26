import threading
import re

default_log_path = "minecraft-server/logs/latest.log"
default_check_interval = 0.5

printing=False

class ChatLogMonitor(): # A class to monitor the Minecraft chat log for player messages
    def __init__(self,path=default_log_path,check_interval=default_check_interval) -> None:
        self.path = path
        self.check_interval = check_interval
        self.last_line_read = 0
        self.message_buffer = []
        self.alive = True

    def get_last_lines(self):
        with open(self.path, 'r') as f:
            lines = f.readlines()
            lines = [line.strip().replace("\n","") for line in lines]
            new_lines = lines[self.last_line_read:]
            self.last_line_read = len(lines)
            return new_lines
        
    def yield_player_message(self):
        # print("buffer2", self.message_buffer, len(self.message_buffer))
        while len(self.message_buffer) > 0:
            candidate = self.message_buffer.pop(0)

            # Use a regular expression to check if the line is a player message
            player_message_match = re.match(r"\[\d{2}:\d{2}:\d{2}] \[Server thread/INFO\]: <(.*?)> (.*)", candidate)
            if player_message_match:
                yield (player_message_match.group(1), player_message_match.group(2)) # return the player name and message
        
        self.message_buffer = []
        
    def start_monitor(self): # Initialize the monitor
        # Skip to the end of the log file
        with open(self.path, 'r') as f:
            lines = f.readlines()
            lines = [line.strip().replace("\n"," ") for line in lines]
            self.last_line_read = len(lines)
        self.monitor()

    def monitor(self): # A looping function to monitor the log file every check_interval seconds
        if not self.alive:
            return
        
        new_lines = self.get_last_lines()
        self.message_buffer.extend(new_lines)

        if printing and self.message_buffer:
            message_generator = self.yield_player_message()
            for player, message in message_generator:
                print(f"{player}: {message}")
                
        threading.Timer(self.check_interval, self.monitor).start()

    def stop_monitor(self):
        self.alive = False

if __name__ == "__main__":
    monitor = ChatLogMonitor()
    printing = True
    print("Starting monitor. Press Enter to stop.")
    monitor.start_monitor()
    input()
    monitor.stop_monitor()