#!/usr/bin/env python

from imapclient import IMAPClient
import sys, getopt
import time
from RPIO import PWM

# Init servo
servo = PWM.Servo()

HOSTNAME = 'imap.gmail.com'
MAILBOX = 'Inbox'
MAIL_CHECK_FREQ     = 20 # check mail every 60 seconds
INIT_WAIT           = 10 # 10s Waiting time after start up
SERVO_LATENCY       = 1 # 1s
SERVO_TIME_BETWEEN  = 0.01
SERVO_UP_VALUE      = 1200
SERVO_DOWN_VALUE    = 660
SERVO_STEP_VALUE    = 10

flag_state = "down"

def inputHelp():
  print 'main.py -id <identification> -p <password> --debug'
  print 'Manage your google application passwords at https://security.google.com/settings/security/apppasswords'
  sys.exit()

def raiseFlag():
  global flag_state
  if flag_state == "down":
    for i in range(SERVO_DOWN_VALUE, SERVO_UP_VALUE, SERVO_STEP_VALUE):
      servo.set_servo(18, i)
      time.sleep(SERVO_TIME_BETWEEN)
  servo.set_servo(18, SERVO_UP_VALUE)
  time.sleep(SERVO_LATENCY)
  flag_state = "up"  

def lowerFlag():
  global flag_state
  if flag_state == "up":
    for i in range(SERVO_UP_VALUE, SERVO_DOWN_VALUE, -SERVO_STEP_VALUE):
      servo.set_servo(18, i)
      time.sleep(SERVO_TIME_BETWEEN)
    servo.set_servo(18, SERVO_DOWN_VALUE)
    servo.stop_servo(18)
    time.sleep(SERVO_LATENCY)
    flag_state = "down"


def main(argv):
  debug = False
  identification = ''
  password = ''
  new_mails_count = -1
  previous_new_mails_count = -1

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

  # Test servo
  raiseFlag()
  lowerFlag()
  
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
      previous_new_mails_count = new_mails_count
      new_mails_count = int(folder_status['UNSEEN'])
      server.logout()

      if debug:
        print 'You have', new_mails_count, 'new emails'

      # IO update
      if previous_new_mails_count != new_mails_count:
        if new_mails_count > 0:
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
