"""Python Quake 3 Library

Updated to work with Python 3 by Fabian Junge

http://misc.slowchop.com/misc/wiki/pyquake3
Copyright (C) 2006-2007 Gerald Kaszuba
This program is free software; you can redistribute it and/or
modify it under the terms of the GNU General Public License
as published by the Free Software Foundation; either version 2
of the License, or (at your option) any later version.
This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.
You should have received a copy of the GNU General Public License
along with this program; if not, write to the Free Software
Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.
"""

import socket
import re


class Player:
    def __init__(self, name, frags, ping, address=None, bot=-1):
        self.name = name
        self.frags = frags
        self.ping = ping
        self.address = address
        self.bot = bot

    def __str__(self):
        return self.name

    def __repr__(self):
        return str(self)


class PyQuake3:
    packet_prefix = '\xff' * 4
    player_reo = re.compile(r'^(\d+) (\d+) "(.*)"')

    def __init__(self, server, rcon_password=''):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.set_server(server)
        self.set_rcon_password(rcon_password)
        self.players = []

    def set_server(self, server):
        try:
            self.address, self.port = server.split(':')
        except ValueError:
            raise ValueError('Server address must be in the format of \
                    "address:port"')
        self.port = int(self.port)
        self.socket.connect((self.address, self.port))

    def get_address(self):
        return '{}:{}'.format(self.address, self.port)

    def set_rcon_password(self, rcon_password):
        self.rcon_password = rcon_password

    def send_packet(self, data):
        packet = '{}{}\n'.format(self.packet_prefix, data).encode('ISO-8859-1')
        self.socket.send(packet)

    def recv(self, timeout=1):
        self.socket.settimeout(timeout)
        try:
            return self.socket.recv(4096)
        except socket.error as exception:
            print('Error receiving the packet: {}'.format(exception))
            raise

    def command(self, cmd, timeout=1, retries=3):
        while retries:
            self.send_packet(cmd)
            try:
                data = self.recv(timeout)
            except socket.error:
                data = None
            if data:
                return self.parse_packet(data)
            retries -= 1
        raise Exception('Server response timed out')

    def rcon(self, cmd):
        r = self.command('rcon {} {}'.format(self.rcon_password, cmd))
        if r[1] == 'No rconpassword set on the server.\n' or r[1] == \
                'Bad rconpassword.\n':
            raise Exception(r[1][:-1])
        return r

    def parse_packet(self, data):
        data = data.decode('ISO-8859-1')
        if data.find(self.packet_prefix) != 0:
            raise Exception('Malformed packet')
        first_line_length = data.find('\n')
        if first_line_length == -1:
            raise Exception('Malformed packet')
        response_type = data[len(self.packet_prefix):first_line_length]
        response_data = data[first_line_length + 1:]
        return response_type, response_data

    def parse_status(self, data):
        split = data[1:].split('\\')
        values = dict(zip(split[::2], split[1::2]))
        # if there are \n's in one of the values, it's the list of players
        for var, val in values.items():
            pos = val.find('\n')
            if pos == -1:
                continue
            split = val.split('\n', 1)
            values[var] = split[0]
            self.parse_players(split[1])
        return values

    def parse_players(self, data):
        self.players = []
        for player in data.split('\n'):
            if not player:
                continue
            match = self.player_reo.match(player)
            if not match:
                print('couldnt match', player)
                continue
            frags, ping, name = match.groups()
            self.players.append(Player(name, frags, ping))

    def update(self):
        cmd, data = self.command('getstatus')
        self.vars = self.parse_status(data)

    def rcon_update(self):
        cmd, data = self.rcon('status')
        lines = data.split('\n')
        players = lines[3:]
        self.players = []
        for p in players:
            while p.find('  ') != -1:
                p = p.replace('  ', ' ')
            while p.find(' ') == 0:
                p = p[1:]
            if p == '':
                continue
            p = p.split(' ')
            self.players.append(Player(p[3][:-2], p[0], p[1], p[5], p[6]))
