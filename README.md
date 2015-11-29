# Pi_flag_raiser
Python scripts for raising a flag when new gmail mail is received.

# Dependencies
Install python imap client:
```
sudo apt-get install -y python-pip
sudo pip install imapclient
```
Install RPIO python lib for raspberry:
```
sudo apt-get install -y python2.7-dev
git clone https://github.com/metachris/RPIO.git
cd RPIO
sudo python setup.py install
```

# Use
To start:
```
python main.py -id <identification> -p <password> --debug
```
For starting script just after network connexion, you can edit /etc/network/interfaces and add the following line with right path and ids:
```
post-up python /home/user/git_rep_directory/main.py -i identification -p password > /home/user/git_rep_directory/Log 2>&1 &
```
Last part will create a Log file in your git repository.

You can restart network interface with:
```
sudo /etc/init.d/networking restart
```

# Links
Based on:
[Adafruit email notifier](https://learn.adafruit.com/raspberry-pi-e-mail-notifier-using-leds/overview)

Documentation:
[Imap client documentation](https://imapclient.readthedocs.org/en/stable/)
[RPIO lib documentation](https://github.com/metachris/RPIO)
