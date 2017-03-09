"""
This script starts the flask server, setting up the socket.io listeners.
"""
from flask import Flask
from flask_socketio import SocketIO, emit
from src.config import CONFIG

APP = Flask(__name__)

APP.config['SECRET_KEY'] = CONFIG['secretKey']

SOCKETIO = SocketIO(APP)

APP.debug = True


@APP.route('/')
def base_route():
    """ Return the name of the project on the base route """
    return 'health-nlp-backend'


@SOCKETIO.on('testnlp')
def test_message(message):
    """ Test socket.io connection: emit the received message """
    print 'Message received: ' + message
    emit('message', message)


if __name__ == '__main__':
    SOCKETIO.run(APP)
