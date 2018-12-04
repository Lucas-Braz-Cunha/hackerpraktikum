import socket, string, time, IN, struct, select, time

class ICMP:

    ICMP_ECHO_REQUEST = 8
    ICMP_ECHO_ANSWER = 0

    def __init__(self, origin, dest, ID = 0, interface=False):
        self.origin = origin
        self.dest = dest
        self.ID = ID
        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_RAW,  socket.getprotobyname("icmp"))
            self.socket.bind((origin, 1))
        except socket.error, (errno, msg):
            if errno == 1:
                msg = msg + ( ": You have to be root.")
                raise socket.error(msg)

    def checksum(self, source_string):
        sum = 0
        countTo = (len(source_string)/2)*2
        count = 0
        while count<countTo:
            thisVal = ord(source_string[count + 1])*256 + ord(source_string[count])
            sum = sum + thisVal
            sum = sum & 0xffffffff
            count = count + 2
        if countTo<len(source_string):
            sum = sum + ord(source_string[len(source_string) - 1])
            sum = sum & 0xffffffff
        sum = (sum >> 16)  +  (sum & 0xffff)
        sum = sum + (sum >> 16)
        answer = ~sum
        answer = answer & 0xffff
        answer = answer >> 8 | (answer << 8 & 0xff00)
        return answer


    def send(self, msg):
        header = struct.pack("bbHHh", self.ICMP_ECHO_ANSWER, 0, 0, self.ID, 1)
        my_checksum = self.checksum(header + msg)
        header = struct.pack("bbHHh", self.ICMP_ECHO_ANSWER, 0, socket.htons(my_checksum), self.ID, 1)
        # 1 + 1 + 2 + 2 + 2 = 8 bytes
        packet = header + msg
        # print repr(packet)
        self.socket.sendto(packet, (self.dest, 1))

    def receive(self, timeout):
        timeLeft = timeout
        # timeLeft = 30
        while True:
            if timeLeft <= 0:
                return -1
            startedSelect = time.time()
            whatReady = select.select([self.socket], [], [], timeLeft)
            howLongInSelect = (time.time() - startedSelect)
            if whatReady[0] == []:
                timeLeft = timeLeft - howLongInSelect
                continue
            timeReceived = time.time()
            recPacket, addr = self.socket.recvfrom(4096)
            icmpHeader = recPacket[20:28]
            type, code, checksum, packetID, sequence = struct.unpack(
                "bbHHh", icmpHeader)
            message = recPacket[28:]
            if("H4CK3D" in message and self.ID == 0):
                # print "Atualizando ID"
                self.ID = packetID
                self.dest = addr[0]
                # print "First message"
                # print repr(message)
                return message
            else:
                if packetID == self.ID:
                    # print "Package ID equal:"
                    # print repr(message)
                    return message
                else:
                    print "Id diferente"
                    return 0
            timeLeft = timeLeft - howLongInSelect

    def close(self):
        self.socket.close()

    def clearID(self):
        self.ID = 0
