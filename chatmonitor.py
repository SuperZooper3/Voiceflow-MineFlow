import threading
import re

default_log_path = "minecraft-server/logs/latest.log"
default_check_interval = 1

class ChatLogMonitor():
    def __init__(self,path,check_interval) -> None:
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
        
    def yeild_player_message(self):
        while len(self.message_buffer) > 0:
            candidate = self.message_buffer.pop(0)
            player_message_match = re.match(r"\[\d{2}:\d{2}:\d{2}] \[Server thread/INFO\]: <(.*?)> (.*)", candidate)
            if player_message_match:
                yield (player_message_match.group(1), player_message_match.group(2))

    def start_monitor(self):
        if not self.alive:
            return
        
        threading.Timer(self.check_interval, self.start_monitor).start()
        new_lines = self.get_last_lines()
        self.message_buffer.extend(new_lines)

    def stop_monitor(self):
        self.alive = False

if __name__ == "__main__":
    monitor = ChatLogMonitor(log_path, check_interval)
    print("Starting monitor. Press Enter to stop.")
    monitor.start_monitor()
    input()
    monitor.stop_monitor()