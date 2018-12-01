The script root_acess.sh shows how to exploit the failure, in a pratical way.


The idea is to add a new root user without password so we can login.

To do this  you need to:

1. Add this entry to /etc/passwd

guest:x:0:0:root:/root:/bin/bash

2. Add this entry to /etc/shadow

guest:U6aMy0wojraho:::::::

This is only possible because the program "ping" copies the message "as is"
to the log file. The tricky part is that this program needs root access to send
ICMP messages. This way its's possible to edit the file /etc/shadow which contains
the passwords.

Notes:
  - It's only possible to login without password if it's permitted.
  - This string "U6aMy0wojraho" represents the empty password, I found it on the internet.

  The file ping_diff.txt has the modifications made by me to correct this security issue.
  The file ping.pyx has the whole "ping" program with the correction done.
  The file ping_source.pyx is the original "ping" program.
