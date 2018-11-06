#!/usr/bin/env python3
#coding: utf-8
import sys
import socket
import re
import ftplib

def check_httpserver(sock, port):
    is_http = False
    try:
        sock.send("GET / HTTP/1.0\r\n\r\n'".encode())
        response = sock.recv(1024).decode()
        if "HTTP" in response:
            is_http = True
            word = 'Server:'
            # parse response to find specific server
            lines = response.split("\n")

            for i,line in enumerate(lines):
                if word in line: # or word in line.split() to search for full words
                    serverName = re.sub('Server:\s+','',line)
                    serverName = serverName.replace('\r','')
                    if serverName in httpServerPorts:
                        httpServerPorts[serverName].append(port)
                    else:
                        httpServerPorts[serverName] = [port]
                    break

    except Exception as ex:
        template = "An exception of type {0} occurred. Arguments:\n{1!r}"
        message = template.format(type(ex).__name__, ex.args)
        print (message)
    finally:
        return is_http

def check_ftp_fingerprint(port):
    """
        I've connected to a know ProFTPd server and saw the response:
        -> http://www.proftpd.org/sites.html
        -> ftp.freeradius.org
        -> type rhelp the answer is exactly the same
    """
    ProFTPd_answer = """214-The following commands are recognized (* =>'s unimplemented):
    214-CWD     XCWD    CDUP    XCUP    SMNT*   QUIT    PORT    PASV
    214-EPRT    EPSV    ALLO*   RNFR    RNTO    DELE    MDTM    RMD
    214-XRMD    MKD     XMKD    PWD     XPWD    SIZE    SYST    HELP
    214-NOOP    FEAT    OPTS    AUTH*   CCC*    CONF*   ENC*    MIC*
    214-PBSZ*   PROT*   TYPE    STRU    MODE    RETR    STOR    STOU
    214-APPE    REST    ABOR    USER    PASS    ACCT*   REIN*   LIST
    214-NLST    STAT    SITE    MLSD    MLST"""
    # I had a problem with losse \r and spaces.... took me a few hours
    ProFTPd_answer = ProFTPd_answer.replace('\r','')
    ProFTPd_answer = ProFTPd_answer.replace(' ', '')

    """
        According to this post: https://www.linuxquestions.org/questions/linux-server-73/problem-with-ssl-and-vsftpd-receiving-error-530-this-ftp-server-is-anonymous-only-562839/
        Someone was trying to install vsftpd but had a problem and the message for login error was
        "530 Please login with USER and PASS."
        I also connected to ftp.redhat.com (from the list of servers from https://security.appspot.com/vsftpd.html#people)
        and the message I got from rhelp was this one.
        So I'll assume the server which gave me this message is a vsftpd

    """
    vsftpd_answer = "530 Please login with USER and PASS."
    found_type = False
    try:
        ftp = ftplib.FTP()
        ftp.connect(host=ip, port=port, timeout=5)
        answer = ftp.sendcmd('help')
        answer_proftpd = answer.replace('\r','')
        answer_proftpd = answer_proftpd.replace(' ', '')
        if 'Pure-FTPd' in answer:
            found_type = True
            if 'Pure-FTPd' in ftpServerPorts:
                ftpServerPorts['Pure-FTPd'].append(port)
            else:
                ftpServerPorts['Pure-FTPd'] = [port]
        elif answer_proftpd.find(ProFTPd_answer) is not -1:
            found_type = True
            if 'ProFTPd' in ftpServerPorts:
                ftpServerPorts['ProFTPd'].append(port)
            else:
                ftpServerPorts['ProFTPd'] = [port]

    except Exception as ex:
        if vsftpd_answer in ex.args:
            found_type = True
            if 'vsftpd' in ftpServerPorts:
                ftpServerPorts['vsftpd'].append(port)
            else:
                ftpServerPorts['vsftpd'] = [port]
    finally:
        #As the last possibility it can only be this type of ftp (in this context)
        if not found_type:
            if 'py-ftpd' in ftpServerPorts:
                ftpServerPorts['py-ftpd'].append(port)
            else:
                ftpServerPorts['py-ftpd'] = [port]
        ftp.close()


""" Getting list of open ports and checking for http and ftp servers """
httpServerPorts = {}
ftpServerPorts = {}
ip = sys.argv[-1]
closed_ports = 0
print('Running scan on host:{}'.format(ip))
for port in range(0,65536):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(2)
    result = sock.connect_ex((ip,port))
    if result == 0:
        if check_httpserver(sock, port):
            continue
        check_ftp_fingerprint(port);
    else:
        closed_ports +=1
    sock.close()


print('Services and the ports they\'re listening to:\n')
print('Total of services found: {0}'.format(len(httpServerPorts) + len(ftpServerPorts)))
print('Number of closed ports: {}'.format(closed_ports))
print('HTTP services: {0}'.format(len(httpServerPorts)))
print('\n------------------------')
for x in httpServerPorts.keys():
    print(str(x) + ': ', end='')
    for p in sorted(httpServerPorts[x]):
        print(str(p) + ' ',end='')
    print('\n------------------------')

print('\nFTP services: {0}'.format(len(ftpServerPorts)))
print('\n------------------------')
for x in ftpServerPorts.keys():
    print(str(x) + ': ', end='')
    for p in sorted(ftpServerPorts[x]):
        print(str(p) + ' ',end='')
    print('\n------------------------')
