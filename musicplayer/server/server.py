import socket
import json

from server.commands import COMMANDS
from server.exceptions import (MusicPlayerException, UnknownCommandException, NoCommandSpecifiedException,
                               InvalidJSONException)
from server.music_player import MusicPlayer
from common import MAX_MESSAGE_SIZE, ENCODING


class Server(object):

    def __init__(self, hostname, port, music_directory):
        """Create a socket and bind to the specified hostname and port"""
        self.hostname = hostname
        self.port = port
        self.socket = socket.socket()
        self.socket.settimeout(0)  # non-blocking mode
        self.socket.bind((self.hostname, self.port))

        self.player = MusicPlayer(music_directory)

    def start(self):
        """Start accepting connections"""
        self.socket.listen(1)
        print("Starting...")

        while True:

            try:
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

                conn.sendall(json.dumps(reply).encode(ENCODING))

            except BlockingIOError:
                pass

            self.player.main_loop()

    def handle_request(self, conn, address):
        """Handle a request and return a message to return to the client"""
        raw_message = conn.recv(MAX_MESSAGE_SIZE).decode(ENCODING).strip()

        print("{}: {}".format(address[0], raw_message))

        # Try to load raw_message as JSON
        try:
            data = json.loads(raw_message)
        except ValueError:
            raise InvalidJSONException("Invalid JSON")

        # Check a command has been specified
        if type(data) != dict or "command" not in data:
            raise NoCommandSpecifiedException("No command specified")

        # Try to get the actual function for the command
        try:
            command = COMMANDS[data["command"]]
        except KeyError:
            raise UnknownCommandException("No such command '{}'".format(data["command"]))

        return command(data, self.player)
