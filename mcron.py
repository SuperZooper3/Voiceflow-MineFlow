from mcrcon import MCRcon

# Replace these with your server details
RCON_IP = "localhost"
RCON_PORT = 25575
RCON_PASSWORD = "voiceflow"

# Establishing a connection
with MCRcon(RCON_IP, RCON_PASSWORD, RCON_PORT) as mcr:
    # Sending a command
    resp = mcr.command("/say Hello, Minecraft World!")
    print(resp)
