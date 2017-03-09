"""
Functions to be used together with socket io
"""

def echo_message(message, emit):
    """ Test socket.io connection: emit the received message """
    print 'Message received: ' + message
    emit('message', message)
    return True

