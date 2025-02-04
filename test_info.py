# tests for the password generation and retrieving

import pytest
import subprocess

# create and retrieve a password
def test_system_command():
    subprocess.run(["python3", "info.py", "-p", "1234"], capture_output=True, text=True)
    subprocess.run(["python3", "info.py", "-s", "1234"], capture_output=True, text=True)
    password = subprocess.run(["python3", "info.py", "-e", "ENV1"], capture_output=True, text=True)
    password2 = subprocess.run(["python3", "info.py", "-g", "ENV1"], capture_output=True, text=True)
    assert password.stdout == password2.stdout 
