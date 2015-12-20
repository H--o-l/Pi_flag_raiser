#!/usr/bin/env python

from imapclient import IMAPClient
import sys, getopt
import time
from RPIO import PWM

# Init servo
servo = PWM.Servo()

HOSTNAME = 'imap.gmail.com'
MAILBOX = 'Inbox'
MAIL_CHECK_FREQ = 20 # check mail every 60 seconds
INIT_WAIT       = 10 # 10s Waiting time after start up
SERVO_LATENCY   = 1 # 1s

def inputHelp():
  print 'main.py -id <identification> -p <password> --debug'
  print 'Manage your google application passwords at https://security.google.com/settings/security/apppasswords'
  sys.exit()

def raiseFlag():
  servo.set_servo(18, 2000)

def lowerFlag():
  servo.set_servo(18, 1250)
  time.sleep(SERVO_LATENCY)
  servo.stop_servo(18)

def main(argv):
  debug = False
  identification = ''
  password = ''

  # Get identification and password from command line argument
  try:
    opts, args = getopt.getopt(argv,'hi:p:d',['identification=','password=','debug'])
  except getopt.GetoptError:
    inputHelp()
  for opt, arg in opts:
    if opt == '-h':
      inputHelp()
    elif opt in ('-i', '--identification'):
      identification = arg
    elif opt in ('-p', '--password'):
      password = arg
    elif opt in ('-d', '--debug'):
      debug = True
    else:
      print opt + ' unknown option.'
      inputHelp()
  if identification == '' or password == '':
    inputHelp()

  print '#--- Start\nId is: ' + identification
  if debug:
    if INIT_WAIT != 0:
      print 'Waiting ' + str(INIT_WAIT) + 's before first connexion'

  # Init servo
  servo = PWM.Servo()

  # Flush stdout for debug and sleep
  sys.stdout.flush()
  time.sleep(INIT_WAIT)

  try:
    # Loop
    while True:
      # New server and log in server (imap forbid server reopen)
      server = IMAPClient(HOSTNAME, use_uid=True, ssl=True)
      server.login(identification, password)

      # Unseen mail
      folder_status = server.folder_status(MAILBOX, 'UNSEEN')
      newmails = int(folder_status['UNSEEN'])
      server.logout()

      if debug:
        print 'You have', newmails, 'new emails'

      # IO update
      if newmails > 0:
        raiseFlag()
      else:
        lowerFlag()

      # Flush stdout for debug and sleep
      sys.stdout.flush()
      time.sleep(MAIL_CHECK_FREQ)

  finally:
    print '#--- Stop'
    lowerFlag()
    time.sleep(SERVO_LATENCY)

if __name__ == '__main__':
  main(sys.argv[1:])
