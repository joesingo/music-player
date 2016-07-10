import json
import socket
from flask import Flask, request, render_template

from common import MAX_MESSAGE_SIZE, ENCODING

app = Flask(__name__)

def send_command(command):
    """"Send the provided command (as a string) to the music player server, and return the reply
    as a string"""
    # Create socket to connect to server
    sock = socket.create_connection(("localhost", 9099))

    # Run the command
    sock.sendall(command.encode(ENCODING))
    reply = sock.recv(MAX_MESSAGE_SIZE).decode(ENCODING).strip()
    return reply


@app.route("/")
def home_page():
    song_list = send_command('{"command": "list"}')
    return render_template("home.html", list=song_list)


@app.route("/send", methods=["POST"])
def send():
    """Take a command as JSON and run on the music player server, returning the reply"""
    command = json.dumps(request.json)
    return send_command(command)
