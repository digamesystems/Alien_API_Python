# Copyright (c) 2020 John Price <john.price@digamesystems.com>
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Eclipse Public License v1.0
# and Eclipse Distribution License v1.0 which accompany this distribution.
#
# The Eclipse Public License is available at
#    https://eclipse.org/org/documents/epl-v10.php.
# and the Eclipse Distribution License is available at
#   https://eclipse.org/org/documents/edl-v10.php.
#
# Contributors:
#    John Price - committer
#    Joe Sacher - initial implementation  https://github.com/sacherjj/python-AlienRFID
#    And Others.


import socket
import time


class AlienConnection(object):

    def __init__(self):
        self.connected = False
        self.raise_errors = True
        self.sock = None

    def _connect(self, ipaddress='localhost', port=23):
        try:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.sock.connect((ipaddress, port))
            self.connected = True
            print("Connected: {0}".format(self.connected))
            s = self.receive()
            print("received: {0}".format(s))
            if "later." in s:
                raise "Trouble Connecting to #{0}. (Someone else is talking to the reader.)".format(ipaddress)
        except RuntimeError:
            raise

    def receive(self, wait_for_null=True, timeout=40):
        if not self.connected:
            raise Exception("Not Connected to Reader")

        s = []
        if wait_for_null:
            cur_char = self.sock.recv(1)
            while cur_char != "\0":
                s.append(cur_char)
                cur_char = self.sock.recv(1)
            packet = ''.join(s)
            packet = packet.strip()

            if 'Goodbye!' in packet:
                # Response to Quit, so socket will be automatically closed
                self.close(False)

            return packet
        else:
            return self.sock.recv(1024)

    def send(self, msg=""):
        if not self.connected:
            raise Exception("Not Connected to Reader")
        self.sock.send("\1{0}\r\n".format(msg))

    def send_receive(self, msg="", wait_for_null=True, timeout=40):
        if not self.connected:
            raise Exception("Not Connected to Reader")
        self.send(msg)
        return self.receive(wait_for_null=wait_for_null, timeout=timeout)

    def _login(self, username="alien", password="password"):
        if self.connected:
            self.sock.send("{0}\r\n".format(username))
            self.receive()
            self.sock.send("{0}\r\n".format(password))
            s = self.receive()

            if 'Error:' in s:
                errmsg = s.split('Error:')[1]
                self.close()
                self.connected = False
                raise Exception("Trouble logging in: " + errmsg)

    def open(self, ipaddress='localhost', port=12345, username="alien", password="password"):
        self._connect(ipaddress, port)
        if self.connected:
            self._login(username, password)
        return self.connected

    def close(self, send_quit=True):
        if self.connected:
            if send_quit:
                self.sock.send("quit\r\n")
                time.sleep(1)
            self.sock.close()
            self.connected = False

ac = AlienConnection()

ac.open()