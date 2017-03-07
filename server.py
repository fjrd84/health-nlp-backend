from flask import Flask, render_template
from flask_socketio import SocketIO, send, emit

app = Flask(__name__)

app.config['SECRET_KEY'] = 'secret!'

socketio = SocketIO(app)

app.debug = True


@app.route('/')
def base_route():
    return 'health-nlp-backend'


@socketio.on('testnlp')
def handle_message(message):
    print('Message received: ' + message)
    emit('message', message)


if __name__ == '__main__':
    socketio.run(app)
