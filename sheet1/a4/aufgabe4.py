#!/usr/bin/python3
import socket
import ssl
import threading
import time
import sys

"""
    Algorithm Idea
    Create socket
    Connect
    ->sucess
        send the connection to thread so it can keep it open
        ...
    ->fail
        add 1 to failuresCounter
    ->5 failures in sequence
        stop program and show the maximum number of threads opened

//5 is a arbitrary number I chose.
"""

#adapted from https://stackoverflow.com/questions/23547604/python-counter-atomic-increment
class AtomicInteger():
    def __init__(self, value=0):
        self._value = value
        self._lock = threading.Lock()
        self._maxNumber = 0

    def inc(self):
        with self._lock:
            self._value += 1
            if(self._value > self._maxNumber):
                self._maxNumber = self._value
            return self._value

    def dec(self):
        with self._lock:
            self._value -= 1
            return self._value

    def getMaxValue(self):
        with self._lock:
            return self._maxNumber

    @property
    def value(self):
        with self._lock:
            return self._value

    @value.setter
    def value(self, v):
        with self._lock:
            self._value = v
            return self._value


class keepConnectionThread (threading.Thread):
    def __init__(self, threadID, wrappedSocket, globalCounter):
      threading.Thread.__init__(self)
      self.threadID = threadID
      self._stop_event = threading.Event()
      self.thread_socket = wrappedSocket
      self.counter = globalCounter

    def stop(self):
        self._stop_event.set()

    def stopped(self):
        return self._stop_event.is_set()

    def run(self):
      print ("Starting {0}".format(self.threadID))
      while True:
          if(self.stopped()):
              self.close_connection()
              break
          try:
              # send message to keep connection alive
              self.thread_socket.send("dummy message".encode())
          except Exception as ex:
              #connection lost, close socket and update failuresCounter of connections
              self.stop()
          finally:
              time.sleep(3)

    def close_connection(self):
        self.counter.dec()
        self.thread_socket.close()
        print('Closing thread {0}'.format(self.threadID))


ip = sys.argv[-1]
atomicCounter =  AtomicInteger()
failuresCounter = 0
threads = []
threadID = 1
__max_failures__ = 5
# arbitrary number to know if the server can still accept connections and it was not a coincidence
while failuresCounter < __max_failures__:
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(5)
    # WRAP SOCKET
    wrappedSocket = ssl.wrap_socket(sock, ssl_version=ssl.PROTOCOL_TLSv1_2)
    try:
        result = wrappedSocket.connect_ex((ip, 443))
        # start thread to keep connection open
        thread = keepConnectionThread(threadID, wrappedSocket, atomicCounter)
        threadID += 1
        atomicCounter.inc()
        # Add thread to threads list
        threads.append(thread)
        thread.start()
        failuresCounter = 0
    except socket.timeout:
        # increment failuresCounter
        failuresCounter+=1

# Wait for all threads to complete
for t in threads:
    t.stop()
    t.join()

print('Number of spawned threads: {0}'.format(threadID-1))
print('Total number of simultaneous connections: {0}'.format(atomicCounter.getMaxValue()))
print ("Exiting benchmark")
