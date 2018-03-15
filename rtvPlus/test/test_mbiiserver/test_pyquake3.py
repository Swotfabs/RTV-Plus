"""Unit tests for rtvPlus.mbiiserver.pyquake3.py
"""

from unittest import TestCase
from unittest.mock import patch
from rtvPlus.mbiiserver.pyquake3 import PyQuake3


class TestSetServer(TestCase):
    """
    Test the set_server function in pyquake3
    """

    def setUp(self):
        socket_patcher = patch("socket.socket")
        self.addCleanup(socket_patcher.stop)
        self.mock_socket = socket_patcher.start()

        server = "127.0.0.1:22"
        self.py = PyQuake3(server)

    def test_set_server(self):
        server = "127.0.0.2:23"
        self.py.set_server(server)
        self.assertEqual(self.py.port, 23)
        self.assertEqual(self.py.address, "127.0.0.2")

    def test_set_server_invalid(self):
        server = "Invalid"
        with self.assertRaises(ValueError):
            self.py.set_server(server)

    def tearDown(self):
        pass
