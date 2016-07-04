import socket
import json
import sys

from commands import (COMMAND_INDEX, MusicPlayerException, UnknownCommandException,
                      NoCommandSpecifiedException, InvalidJSONException)

class Server(object):

    MAX_MESSAGE_SIZE = 1024
    ENCODING = "UTF-8"

    def __init__(self, hostname, port):
        """Create a socket and bind to the specified hostname and port"""
        self.hostname = hostname
        self.port = port
        self.socket = socket.socket()
        self.socket.bind((self.hostname, self.port))

    def start(self):
        """Start accepting connections"""
        self.socket.listen(1)
        print("Starting...")

        while True:
            conn, addr = self.socket.accept()

            try:
                self.handle_request(conn, addr)

            except MusicPlayerException as e:
                # If an exception occured handling the request, send back a JSON object detailing
                # what went wrong
                reply_dict = {
                    "status": "error",
                    "message": e.args[0]
                }
                reply = json.dumps(reply_dict)
                conn.sendall(reply.encode(Server.ENCODING))

    def handle_request(self, conn, address):
        """Handle a request"""
        raw_message = conn.recv(Server.MAX_MESSAGE_SIZE).decode(Server.ENCODING)

        print("{}: {}".format(address[0], raw_message))

        # Try to load raw_message as JSON
        try:
            data = json.loads(raw_message)
        except ValueError:
            raise InvalidJSONException("Invalid JSON")

        # Check a command has been specified
        if "command" not in data:
            raise NoCommandSpecifiedException("No command specified")

        try:
            # Get the class for the command to be run, and run it
            command = COMMAND_INDEX[data["command"]]
            command.run(data)
        except KeyError:
            raise UnknownCommandException("No such command '{}'".format(data["command"]))


if __name__ == "__main__":
    hostname = "localhost"
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 9090

    s = Server(hostname, port)
    s.start()
