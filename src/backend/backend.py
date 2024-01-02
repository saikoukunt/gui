from flask import Flask
from flask_socketio import SocketIO

app = Flask(__name__)
socket = SocketIO(app, cors_allowed_origins=['http://localhost:5173'])

@socket.on('connect')
def handle_connect():
    print("frontend connected!")

@socket.on('frontend-msg')
def handle_message(msg):
    print("Message from frontend: " + msg['str'])
    socket.emit("backend-msg", "uwu hewwo")

@app.route('/')
def hello():
    return '<h1>Hello World!'

if __name__ == '__main__':
    socket.run(app, port=3000)

