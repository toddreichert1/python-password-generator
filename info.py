#################################################################################
#   Program name: info.py
#    Description: Python Passcode Generator and Vault
#                 This script was designed to be a stop-gap solution for 
#                 storing passcodes when it is needed to maintain many
#                 unique passcodes that need to be changed frequently.
#                 
#          Usage: It is recommended to create a new directory to run this
#                 script in. It will create a "/data" directory to store
#                 the encrypted passcodes.
#                 The script is additionally protected by a session pin.
#                 Before use, you must create this session pin (option -p).
#################################################################################

import random
import string
import rsa
import getopt, sys
import pathlib
import datetime
import shutil
import os
from os.path import exists

#################################################################################
# validate - make sure the passcode meets the requirements
#            - cannot repeat a character more than twice
#            - make sure it starts with an alpha charater
#################################################################################
def validate(passcode):

  # Make sure the passcode has length and starts with an alpha character
  if len(passcode) <= 0 or not passcode[0].isalpha():
    #print "ERROR: passcode not valid - does not start with alpha, " + passcode
    return False

  # unique list of characters in the passcode
  uniqueCharacters = list(set(passcode))

  # cycle thru the characters and if one of the counts
  #   is greater than 2, return false
  position = 0
  while position < len(uniqueCharacters):
    if passcode.count(uniqueCharacters[position]) > 2:
      #print "ERROR: passcode not valid - character repeats more than twice, " + \
      #        str(uniqueCharacters[position]) + "=" + \
      #        str(passcode.count(uniqueCharacters[position])) + ", " + passcode
      return False
    position += 1

  # all character counts were less or equal to 2
  return True


#################################################################################
# create - create the passcode
#################################################################################
def create():

  # special characters allowed
  special_characters = '!#%'

  # full list of usable characters in the passcode
  random_source = string.ascii_letters + string.digits + special_characters

  # loop thru passcodes until we get a valid passcode
  validPasscode=False
  while not validPasscode:
    # select 2 lowercase
    passcode = random.SystemRandom().choice(string.ascii_lowercase)
    passcode += random.SystemRandom().choice(string.ascii_lowercase)

    # select 3 uppercase
    passcode += random.SystemRandom().choice(string.ascii_uppercase)
    passcode += random.SystemRandom().choice(string.ascii_uppercase)
    passcode += random.SystemRandom().choice(string.ascii_uppercase)

    # select 2 digits
    passcode += random.SystemRandom().choice(string.digits)
    passcode += random.SystemRandom().choice(string.digits)

    # select 1 special character
    passcode += random.SystemRandom().choice(special_characters)

    # get 4 other random characters
    for i in range(4):
      passcode += random.SystemRandom().choice(random_source)

    # shuffle characters
    passcode_list = list(passcode)
    random.SystemRandom().shuffle(passcode_list)
    passcode = ''.join(passcode_list)

    # validate the passcode
    validPasscode = validate(passcode)

  # return the passcode
  return passcode


#################################################################################
# get passcode
#################################################################################
def get_passcode(environment, privateKey, verbose):

  # create the path to the environment file
  location = "data/" + environment

  # check to see if the file exists
  file = pathlib.Path(location)

  # return value
  returnValue = 0
  if file.exists():
    # file exists, so decrypt and display for user
    with open(location, "rb") as message:
      decryptedMessage = rsa.decrypt(message.read(), privateKey).decode()
      if (verbose):
        print("****** ", environment, " ******\t", decryptedMessage)
      else:
        print(decryptedMessage)
  # file did not exist
  else:
    print("ERROR: File does not exist")
    print("option -g requires an existing environment")
    returnValue = 1

  return returnValue

#################################################################################
# load public and private keys
#################################################################################
def load_keys():

  # set variables for filenames
  publicFile = "data.public"
  privateFile = "data.private"

  # check to see if the keys exist, if not create them
  if not(exists(publicFile)) or not(exists(privateFile)):
    # generate new public and private keys with rsa.newkeys method, 
    # this method accepts key length as its parameter and should be at least 16
    publicNewKey, privateNewKey = rsa.newkeys(512)

    # create public key
    public_key_file = open(publicFile, 'w+')
    public_key_file.write(publicNewKey.save_pkcs1('PEM').decode())
    public_key_file.close()

    # create private key
    private_key_file = open(privateFile, 'w+')
    private_key_file.write(privateNewKey.save_pkcs1('PEM').decode())
    private_key_file.close()

  # get the keys
  with open(publicFile, "r") as publicfile:
    public = rsa.PublicKey.load_pkcs1(publicfile.read())

  with open(privateFile, "r") as privatefile:
    private = rsa.PrivateKey.load_pkcs1(privatefile.read())

  # return the keys
  return public, private


#################################################################################
# usage
#################################################################################
def usage():
  print()
  print("usage: python info.py [-c <number of passcodes to create>]\n" +
        "                      [-p <create a numeric session pin>]\n" +
        "                      [-s <start a session with a pin>]\n" +
        "                      [-e <environment to create/update passcode>]\n" +
        "                      [-g <environment to get passcode> or \"all\" for all environments]\n" +
        "\n" +
        "NOTE: Please create a new directory to place and run this script from.\n" +
        "      Also, please create a session pin (option -p) before using the script.\n" +
        "")
  print()

#################################################################################
# main
#################################################################################
def main():
  try:
    opts, args = getopt.getopt(
      sys.argv[1:],
      "hc:p:s:e:g:",
      ["help","create","pin","session","environment","get"]
    )
  except getopt.GetoptError as err:
    print(err)
    usage()
    sys.exit(2)

  # no arguments
  if not opts:
    usage()
    sys.exit(3)

  # variables
  sessionPinFile = "session.pin"
  sessionFile = "session"

  for opt, arg in opts:
    #####################################################
    # display usage/help
    #####################################################
    if opt in ("-h", "--help"):
      usage()
      sys.exit(1)

    #####################################################
    # create passcode(s)
    #####################################################
    elif opt in ("-c", "--create"):
      # check to see if numeric argument
      if arg.isnumeric():
        # set the number to create
        numberToCreate = int(arg)

        # create the passcodes
        for i in range(numberToCreate):
          print(create())
      else:
        print("option -c requires a numeric argument, ie number of passcodes to create")
        usage()
        sys.exit(4)

    #####################################################
    # create a session pin
    #####################################################
    elif opt in ("-p", "--pin"):
      # get the keys
      publicKey, privateKey = load_keys()
      
      # check to see if numeric argument
      if arg.isnumeric():
        # get the passed in pin
        pin = arg

        # create the session pin file
        encryptedMessage = rsa.encrypt(pin.encode(), publicKey)
        encryptedFile = open(sessionPinFile, 'wb+')
        encryptedFile.write(encryptedMessage)
        encryptedFile.close()

        # create the data directory if it does not exist
        if not os.path.exists("data"):
          os.makedirs("data")

      else:
        print("option -p requires a numeric argument, ie number of passcodes to create")
        usage()
        sys.exit(8)

    #####################################################
    # start a session
    #####################################################
    elif opt in ("-s", "--session"):
      # get the keys
      publicKey, privateKey = load_keys()

      # get the passed in pin
      pin = arg

      # get the encrypted pin
      with open(sessionPinFile, "rb") as message:
        decryptedMessage = rsa.decrypt(message.read(), privateKey).decode()
      
      # if they match, set a session timeout 5 minutes in the future
      if decryptedMessage == pin:
        # get the future timestamp
        future = datetime.datetime.now() + datetime.timedelta(seconds=5*60)

        # format it
        message = future.strftime("%Y%m%d%H%M%S")

        # encrypt it and write to the file
        encryptedMessage = rsa.encrypt(message.encode(), publicKey)
        encryptedFile = open(sessionFile, 'wb+')
        encryptedFile.write(encryptedMessage)
        encryptedFile.close()

      # the pin did not match
      else:
        print("ERROR: Invalid session pin")
        usage()
        sys.exit(6)

    #####################################################
    # create/update passcode for an environment
    #####################################################
    elif opt in ("-e", "--environment"):
      # get the keys
      publicKey, privateKey = load_keys()

      # check to see if the session is active
      if not(exists(sessionFile)):
        print("ERROR: Please create a session pin and/or session (see option -p and -s)")
        usage()
        sys.exit(10)
      timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
      with open(sessionFile, "rb") as message:
        sessionTimestamp = rsa.decrypt(message.read(), privateKey).decode()
      if timestamp > sessionTimestamp:
        print("ERROR: Session timed out")
        usage()
        sys.exit(9)
      
      # get the environment
      environment = arg

      # create the path to the environment file
      location = "data/" + environment

      # check to see if the file exists, if so create a backup since updating
      file = pathlib.Path(location)
      if file.exists ():
        timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
        print("Creating a backup: " + shutil.copyfile(location, location + "." + timestamp))

      # update passcode
      message = create()
      encryptedMessage = rsa.encrypt(message.encode(), publicKey)
      encryptedFile = open(location, 'wb+')
      encryptedFile.write(encryptedMessage)
      encryptedFile.close()

      # print the udpated passcode for the user
      print(message)

    #####################################################
    # get passcode(s)
    #####################################################
    elif opt in ("-g", "--get"):
      # get the keys
      publicKey, privateKey = load_keys()

      # check to see if the session is active
      if not(exists(sessionFile)):
        print("ERROR: Please create a session pin and/or session (see option -p and -s)")
        usage()
        sys.exit(11)
      timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
      with open(sessionFile, "rb") as message:
        sessionTimestamp = rsa.decrypt(message.read(), privateKey).decode()
      if timestamp > sessionTimestamp:
        print("ERROR: Session timed out")
        usage()
        sys.exit(7)
      
      # get the environment
      environment = arg
      if arg == "all":
        # call listdir(path) to get a list of all environments
        directory = os.listdir("data")

        # get and print passcodes
        for file in directory:
          get_passcode(file, privateKey, True)
      else:
        # get and print passcode
        if get_passcode(environment, privateKey, False):
          usage()
          sys.exit(5)

# Run main()
if __name__ == '__main__':
  main()

