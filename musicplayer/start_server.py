import os
import json

from server.server import Server

if __name__ == "__main__":
    directory = os.path.dirname(os.path.realpath(__file__))

    # Read the config file
    with open(directory + "/server/server_config.json") as config_file:
        config = json.load(config_file)

    hostname = config["hostname"]
    port = config["port"]
    music_directory = config["music_directory"]

    s = Server(hostname, port, music_directory)
    s.start()
