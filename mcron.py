from mcrcon import MCRcon

class RconSender():
    def __init__(self, ip, port, password):
        self.ip = ip
        self.port = port
        self.password = password
        self.mcr = MCRcon(self.ip, self.password, self.port)
        self.mcr.connect()

    def disconnect(self):
        self.mcr.disconnect()

    def send(self, command):
        try:
            resp = self.mcr.command(command)
            return resp
        except:
            return f"Error connecting to server {self.ip}:{self.port} with password = {self.password}."

if __name__ == "__main__":
    RCON_IP = "localhost"
    RCON_PORT = 25575
    RCON_PASSWORD = "voiceflow"
    rcon = RconSender(RCON_IP, RCON_PORT, RCON_PASSWORD)
    print(rcon.send("say Hello, Minecraft World!"))
    print(rcon.send("say Hello, Minecraft World!"))
    print(rcon.send("say Hello, Minecraft World!"))