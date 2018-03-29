"""This brings everything together.
It will be the thing the server executes.
It is currently empty.
"""

from cmd import Cmd
import argparse
import time
from rtvPlus.mbiiserver.mbiiserver import mbiiserver


class RTVPrompt(Cmd):
    """This is a custom prompt that allows command line users to send
    rcon commands to the server"""

    def __init__(self, server=None, rconpassword=None):
        super().__init__()
        if server:
            print("Connecting to {} with rconpassword {}".format(server,
                                                                 rconpassword))
            self.mbiiserver = mbiiserver(server, rconpassword)
        else:
            print("Starting unconnected")
            self.mbiiserver = None

    def cmdloop(self, intro=None):
        try:
            super().cmdloop(intro)
            return
        except KeyboardInterrupt as keyError:
            print("\nExiting due to Ctr-C")
            self.postloop()

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

    def do_login(self, line):
        if not self.mbiiserver:
            print("Not currently connected to a server")
            return
        self.mbiiserver.server.set_rcon_password(line)

    def do_connect(self, line):
        """Connect to an MBII Server
        Usage: connect ip:port rconpassword"""
        if self.mbiiserver:
            print("Already connected, please disconnect first")
            return
        try:
            server, rconpassword = line.split()
        except ValueError as value:
            self.mbiiserver = mbiiserver(line, None)
        else:
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
        """Closes the socket and exits the prompt
        Offloads the work to postloop"""
        return True

    def emptyline(self):
        pass

    def postloop(self):
        """Closes the socket and exits the prompt"""
        if self.mbiiserver:
            print("Closing Socket")
            self.mbiiserver.server.socket.close()
        print("Exiting Prompt")


def add_arguments(parser):
    parser.add_argument('mode', choices=['cmd', 'command'], help=(
            "'cmd' launches a command line interface,"
            " 'command' sends one command to the server"))
    parser.add_argument('--server', '-s',
                        help="the server to connect to in the form of ip:port")
    parser.add_argument('--rconpassword', '-rcon',
                        help="the rcon password for the server")
    parser.add_argument('--command', '-com',
                        help=("The command to send to the server, do not"
                              " prefix with 'rcon'"))
    parser.add_argument('--retries', '-ret', default=1,
                        help=("in command mode, the number of times"
                              " to attempt sending the command. The default"
                              " is 1"))


def main():
    pass
    parser = argparse.ArgumentParser(
        description="A tool to communicate with a pyquake3 server via rcon",
        formatter_class=argparse.RawTextHelpFormatter,
        epilog=(
            "In cmd mode specifying --server will start the command prompt"
            " connected to that server.\nSpecifying --rconpassword as well"
            " will start the command prompt logged in to that server.\n"
            "In command mode --server, --rconpassword, and --command are"
            " required."))
    add_arguments(parser)
    args = parser.parse_args()

    if args.mode == 'cmd':
        prompt = RTVPrompt(server=args.server, rconpassword=args.rconpassword)
        prompt.prompt = "> "
        prompt.cmdloop()
    elif args.mode == 'command':
        if not args.server and args.rconpassword and args.command:
            print("You must set the server and the password for command mode")
            return
        server = mbiiserver(args.server, args.rconpassword)
        while args.retries > 0:
            try:
                response_type, response_data = server.server.rcon(args.command)
                print(response_data)
            except Exception as e:
                print(e)
            finally:
                if args.retries > 0:
                    time.sleep(1)
                args.retries -= 1


if __name__ == "__main__":
    main()
else:
    raise NotImplementedError  # This module is not intedned to be imported
