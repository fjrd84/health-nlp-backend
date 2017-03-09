"""
server_test.py
"""
from server import base_route

def test_base_route():
    """ Testing the base route """
    assert base_route() == 'health-nlp-backend'
