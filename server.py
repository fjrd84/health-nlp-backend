from flask import Flask, render_template
from flask_socketio import SocketIO, send

app = Flask(__name__)

app.config['SECRET_KEY'] = 'secret!'

socketio = SocketIO(app)

app.debug = True

@app.route('/')
def base_route():
    return 'health-nlp-backend'

if __name__ == '__main__':
    """app.run()"""
    socketio.run(app)

@socketio.on('message')
def handle_message(message):
    send(message)

@socketio.on('json')
def handle_json(json):
    print('received json: ' + str(json))