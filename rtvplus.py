"""This brings everything together.
It will be the thing the server executes.
It is currently empty.
"""

from cmd import Cmd
from rtvPlus.mbiiserver.mbiiserver import mbiiserver


class RTVPrompt(Cmd):
    """This is a custom prompt that allows command line users to send
    rcon commands to the server"""

    def __init__(self):
        super().__init__()
        self.mbiiserver = None

    def do_rcon(self, line):
        """Sends an rcon command to the server"""
        if not self.mbiiserver:
            print("You must first connect to a server")
            return
        print(self.mbiiserver.server.rcon(line))

    def do_connect(self, line):
        """Connect to an MBII Server
        Usage: connect ip:port rconpassword"""
        if self.mbiiserver:
            print("Already connected, please disconnect first")
            return
        server, rconpassword = line.split()
        self.mbiiserver = mbiiserver(server, rconpassword)

    def do_disconnect(self, line):
        """Disconnects from the server"""
        if not self.mbiiserver:
            try:
                print("Not currently connected to a server")
            except Exception as e:
                print(e)
        else:
            print("Disconnecting")
            self.mbiiserver = None

    def do_status(self, line):
        """Returns whether the prompt is connected and
        the status of the server"""
        if self.mbiiserver:
            print("Currently Connected to {}".format(
                self.mbiiserver.server.address))
            print("On Port {}".format(self.mbiiserver.server.port))
            print("With rcon password {}".format(
                self.mbiiserver.server.rcon_password))
            try:
                print(self.mbiiserver.server.rcon("status"))
            except Exception as e:
                print(e)
        else:
            print("Not currently connected to a server")


if __name__ == "__main__":
    prompt = RTVPrompt()
    prompt.prompt = "> "
    prompt.cmdloop("Starting prompt...")
else:
    raise NotImplementedError  # This is not yet usable.
