"""WORK IN PROGRESS: Currently just a copy of the Rcon object from rtvrtm.
A connection to a Movie Battles II Server
"""

raise NotImplementedError  # This is not yet usable.


class Rcon(object):
    """Send commands to the server via rcon. Wrapper class."""
    def __init__(self, address, bindaddr, rcon_pwd):
        self.address = address
        self.bindaddr = bindaddr
        self.rcon_pwd = rcon_pwd

    def _send(self, payload, buffer_size=1024):  # internal fuction
        sock = socket(AF_INET, SOCK_DGRAM)
        sock.bind((self.bindaddr, 0))  # Port 0 will let the OS pick an available port for us.
        sock.settimeout(1)
        sock.connect(self.address)
        send = sock.send
        recv = sock.recv

        while(True):    # Make sure an infinite loop is placed until
                        # the command is successfully received.
            try:
                send(payload)
                recv(buffer_size)
                break
            except socketTimeout:
                continue
            except socketError:
                break
        sock.shutdown(SHUT_RDWR)
        sock.close()

    def say(self, msg):

        self._send("\xff\xff\xff\xffrcon %s say %s" % (self.rcon_pwd, msg),
                   2048)

    def svsay(self, msg):
        if len(msg) > 141:  # Message is too big for "svsay".
            self.say(msg)   # Use "say" instead.

        else:
            self._send("\xff\xff\xff\xffrcon %s svsay %s" % (
                                                            self.rcon_pwd,
                                                            msg))

    def mbmode(self, cmd):
        self._send("\xff\xff\xff\xffrcon %s mbmode %s" % (self.rcon_pwd, cmd))

    def clientkick(self, player_id):
        self._send("\xff\xff\xff\xffrcon %s clientkick %i" % (
                                                             self.rcon_pwd,
                                                             player_id))
