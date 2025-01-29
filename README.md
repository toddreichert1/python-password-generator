# Python Password Generator and Vault

## Installation:
- Create a directory
- Copy the python file in 
- Run by reviewing the usage()

---
**Overview**: There was a requirement to maintain ~12 passwords across 12 environments.

## Requirements:
- Passwords had to be unique across all environments.
- Passwords had a criteria for each environment.
- Passwords must be changed on a monthly basis.

## Implementation:
- Need to be able to create valid passwords.
- Need to be able to store and associate those passwords with an environment.
- Need to add security.

## Implementation Details:

### Step 1: Create valid passwords
- The most stringent criteria was able to work for the rest of the environments.

### Step 2: Store the passwords
- Accomplished by naming the file the environment name and storing the password inside of it.
- Made sure to have a history by creating a copy of the old file with a timestamp.

### Step 3: Security
- Encrypt the passwords in the files.
- Encrypt the script by creating a “session” that makes the passwords accessible for 5 minutes after a PIN is provided.

### Other:

- Decided to keep this as a “one-file” implementation.
- A simple “install”, just create a directory, copy the file in and run by reviewing the usage().

- A few co-workers showed interest in learning Python, so it felt like this was a good on-ramp that had a lot of the basics to help them get over the learning hump and starting getting real world efforts out of it.

### Enhancements:
- Develop an install step
- Make the PIN interactive, so as not to expose it to the command line
- Pull the create_password procedure out and create a python library
