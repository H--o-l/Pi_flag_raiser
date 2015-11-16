#!/usr/bin/env python
 
from imapclient import IMAPClient
import sys, getopt
import time
 
# import RPi.GPIO as GPIO
 
HOSTNAME = 'imap.gmail.com'
MAILBOX = 'Inbox'
MAIL_CHECK_FREQ = 60 # check mail every 60 seconds
INIT_WAIT = 10 # Waiting time after start up

def inputHelp():
  print 'main.py -id <identification> -p <password> --debug'
  print 'Manage your google application passwords at https://security.google.com/settings/security/apppasswords'
  sys.exit()

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

  # flush stdout for debug and sleep
  sys.stdout.flush()
  time.sleep(INIT_WAIT)

  try:
    # IO setup
    # GPIO.setwarnings(False)
    # GPIO.setmode(GPIO.BCM)
    # GREEN_LED = 18
    # RED_LED = 23
    # GPIO.setup(GREEN_LED, GPIO.OUT)
    # GPIO.setup(RED_LED, GPIO.OUT)

    # Loop
    while True:
      # New server and log in server (imap forbid server reopen)
      server = IMAPClient(HOSTNAME, use_uid=True, ssl=True)
      server.login(identification, password)
     
      # Unseen mail
      folder_status = server.folder_status(MAILBOX, 'UNSEEN')
      newmails = int(folder_status['UNSEEN'])
     
      if debug:
        print 'You have', newmails, 'new emails'
    
      # IO update
      # if newmails > 0:
      #   GPIO.output(GREEN_LED, True)
      #   GPIO.output(RED_LED, False)
      # else:
      #   GPIO.output(GREEN_LED, False)
      #   GPIO.output(RED_LED, True)

      # Logout
      #server.logout()

      # flush stdout for debug and sleep
      sys.stdout.flush()
      time.sleep(MAIL_CHECK_FREQ)

  finally:
    print '#--- Stop'
    # GPIO.cleanup()

if __name__ == '__main__':
  main(sys.argv[1:])
