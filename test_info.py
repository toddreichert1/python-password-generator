# tests for the password generation and retrieving

import pytest
import subprocess
from info import *

# create and retrieve a password
def test_creation_and_retrieval():
    subprocess.run(["python3", "info.py", "-p", "1234"], capture_output=True, text=True)
    subprocess.run(["python3", "info.py", "-s", "1234"], capture_output=True, text=True)
    password = subprocess.run(["python3", "info.py", "-e", "ENV1"], capture_output=True, text=True)
    password2 = subprocess.run(["python3", "info.py", "-g", "ENV1"], capture_output=True, text=True)
    assert password.stdout == password2.stdout 

# create and retrieve a password
def test_password_validation():
    subprocess.run(["python3", "info.py", "-p", "1234"], capture_output=True, text=True)
    subprocess.run(["python3", "info.py", "-s", "1234"], capture_output=True, text=True)
    password = subprocess.run(["python3", "info.py", "-e", "ENV2"], capture_output=True, text=True)
    assert validate(password.stdout) == True 
