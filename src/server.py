"""
This script starts the flask server, setting up the socket.io listeners.
"""
from flask import Flask
from flask_socketio import SocketIO, emit
from nlp_socketio import echo_message
from config import CONFIG


APP = Flask(__name__)

APP.config['SECRET_KEY'] = CONFIG['secretKey']

SOCKETIO = SocketIO(APP)

APP.debug = True


@APP.route('/')
def base_route():
    """ Return the name of the project on the base route """
    return 'health-nlp-backend'

@SOCKETIO.on('testnlp')
def testnlp_listener(message):
    """ Wrap echo_message into a socket io decorator """
    return echo_message(message, emit)

if __name__ == '__main__':
    SOCKETIO.run(APP)
