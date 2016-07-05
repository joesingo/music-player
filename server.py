import socket
import json
import sys

from commands import COMMANDS
from exceptions import (MusicPlayerException, UnknownCommandException, NoCommandSpecifiedException,
                        InvalidJSONException)
from music_player import MusicPlayer


class Server(object):

    MAX_MESSAGE_SIZE = 1024
    ENCODING = "UTF-8"

    def __init__(self, hostname, port, music_directory):
        """Create a socket and bind to the specified hostname and port"""
        self.hostname = hostname
        self.port = port
        self.socket = socket.socket()
        self.socket.bind((self.hostname, self.port))

        self.player = MusicPlayer(music_directory)

    def start(self):
        """Start accepting connections"""
        self.socket.listen(1)
        print("Starting...")

        while True:
            conn, addr = self.socket.accept()

            # Template for the reply
            reply = {
                "status": "",
                "message": ""
            }

            try:
                reply_message = self.handle_request(conn, addr)
                # If above line went without raising an exception then everything has gone fine
                reply["status"] = "okay"
                reply["message"] = reply_message or ""

            except MusicPlayerException as e:
                reply["status"] = "error"
                # Set the message to the error message from the exception
                reply["message"] = e.args[0]

            conn.sendall(json.dumps(reply).encode(Server.ENCODING))

    def handle_request(self, conn, address):
        """Handle a request and return a message to return to the client"""
        raw_message = conn.recv(Server.MAX_MESSAGE_SIZE).decode(Server.ENCODING).strip()

        print("{}: {}".format(address[0], raw_message))

        # Try to load raw_message as JSON
        try:
            data = json.loads(raw_message)
        except ValueError:
            raise InvalidJSONException("Invalid JSON")

        # Check a command has been specified
        if "command" not in data:
            raise NoCommandSpecifiedException("No command specified")

        # Try to get the actual function for the command
        try:
            command = COMMANDS[data["command"]]
        except KeyError:
            raise UnknownCommandException("No such command '{}'".format(data["command"]))

        return command(data, self.player)

if __name__ == "__main__":
    with open("server_config.json") as config_file:
        config = json.load(config_file)

    # Read the config file
    hostname = config["hostname"]
    port = config["port"]
    music_directory = config["music_directory"]

    s = Server(hostname, port, music_directory)
    s.start()
