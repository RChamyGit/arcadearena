from flask import Flask, session, Markup, Response
from flask_socketio import *
app = Flask(__name__)
socketio = SocketIO(app, async_handlers=True)

if __name__ == '__main__':
    """ Run the app. """
    socketio.run(app)