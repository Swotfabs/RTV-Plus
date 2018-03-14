"""This will handle the status of the MBII server.
Number of players, what map it is on, etcetera.

"""
from PyQuake3 import PyQuake3


class mbiiserver:
    def __init__(self, server, rconpassword=''):
        self.players = []
        self.map = None
        self.server = PyQuake3(server, rconpassword)
