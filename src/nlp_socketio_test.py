"""
nlp_socketio_test.py
"""
from nlp_socketio import echo_message

def dummy_emit(message, value):
    """ Dummy emit to emulate socket.io's emit """
    return message + value

def test_echo_message():
    """ Testing the echo message """
    assert echo_message('Some message', dummy_emit)
