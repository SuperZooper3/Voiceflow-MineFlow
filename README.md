# Voiceflow-MineFlow

A Minecraft integration for Voiceflow!

Built based off the Python example from Voiceflow's [Python API Example](https://github.com/voiceflow/api-examples/tree/master/python).

We connect to the Minecraft server's RCON interface to send commands to the server, and monitor the server's log file to get player messages.

## Setup

### Python and Voiceflow

1. Install [Python 3.8](https://www.python.org/downloads/release/python-380/) or higher.
2. Install the required packages with `pip install -r requirements.txt`.
3. Create a `.env` file in the root directory of the project and set the your Voiceflow API key as `VF_API_KEY="VF.DM.XXXXXXXXXX`

### Minecraft Server

1. Download the Minecraft server application from [here](https://www.minecraft.net/en-us/download/server). Follow the installation instructions, run the server once, accept the ELUA, and then close the server.
2. In `server.properties`, set `enable-rcon=true` and `rcon.password=yourpasswordhere` to enable RCON. Be sure to take note of the RCON port in `rcon.port` (usually 25575).
3. In `mrcon.py` set the `RCON_HOST` (the server's IP), `RCON_PORT`, and `RCON_PASSWORD` variables to the values you set in `server.properties`.
