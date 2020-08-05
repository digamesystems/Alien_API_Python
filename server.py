#!/usr/bin/python           # This is server.py file

'''
server.py -- A test server to emulate messages to/from an Alien RFID reader. 
'''


import socket               # Import socket module
import sys

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # Create a socket object

host = 'localhost' #socket.gethostname() # Get local machine name

port = 12345                # Reserve a port for your service.
s.bind((host, port))        # Bind to the port

s.listen(1)                 # Now wait for client connection.

while True:

   c, addr = s.accept()     # Establish connection with client.
   print('Got connection from:', addr)

   c.send('Username:\0')    # Manage the user login
   print(c.recv(1024))
   c.send('Password:\0')
   print(c.recv(1024))
   
   c.send('Alien>\0')       # Send prompt

   while True: # Emulate Processing commands
      cmd = c.recv(1024)
      print(cmd)
      c.send("{0}\r\n\0".format(cmd))


   c.close()                # Close the connection