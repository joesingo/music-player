import socket
from flask import Flask, request, render_template


app = Flask(__name__)

@app.route("/")
def home_page():
    sock = socket.create_connection(("localhost", 9092))
    sock.sendall(b"yp")
    reply = sock.recv(1024)
    print(str(reply))
    return render_template("home.html")


@app.route("/send", methods=["POST"])
def send():
    print(dir(request))

if __name__ == "__main__":
    app.run(port=5000, debug=True)