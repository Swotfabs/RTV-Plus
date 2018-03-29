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

    def cmdloop(self, intro=None):
        try:
            super().cmdloop(intro)
            return
        except KeyboardInterrupt as keyError:
            print("\nExiting due to Ctr-C")
            self.do_exit("")

    def do_rcon(self, line):
        """Sends an rcon command to the server"""
        if not self.mbiiserver:
            print("You must first connect to a server")
            return
        try:
            response_type, response_data = self.mbiiserver.server.rcon(line)
            print(response_data)
        except Exception as e:
            print(e)

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
            print("Not currently connected to a server")
        else:
            print("Disconnecting")
            self.mbiiserver.server.socket.close()
            self.mbiiserver = None

    def do_status(self, line):
        """Returns whether the prompt is connected and
        the status of the server"""
        if self.mbiiserver:
            print("Currently Connected to {} on port {} with rcon password {}"
                  .format(self.mbiiserver.server.address,
                          self.mbiiserver.server.port,
                          self.mbiiserver.server.rcon_password))
            try:
                response_type, response_data = self.mbiiserver.server.rcon(
                    "status")
                print(response_data)
            except Exception as e:
                print(e)
        else:
            print("Not currently connected to a server")

    def do_exit(self, line):
        """Closes the socket and exits the prompt"""
        if self.mbiiserver:
            print("Closing Socket")
            self.mbiiserver.server.socket.close()
        print("Exiting Prompt")
        return True

    def emptyline(self):
        pass


if __name__ == "__main__":
    prompt = RTVPrompt()
    prompt.prompt = "> "
    prompt.cmdloop("Starting prompt...")
else:
    raise NotImplementedError  # This is not yet usable.
