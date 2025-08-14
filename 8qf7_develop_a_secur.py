import getpass
import os
import hashlib
import argparse
import crypt

class SecurCLI:
    def __init__(self):
        self.parser = argparse.ArgumentParser(description='Secure CLI Tool Simulator')
        self.parser.add_argument('-u', '--username', help='Username', required=True)
        self.parser.add_argument('-p', '--password', help='Password', required=True)
        self.parser.add_argument('-c', '--command', help='Command to execute', required=True)
        self.args = self.parser.parse_args()

    def hash_password(self, password):
        salt = os.urandom(16)
        hashed_password = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt, 100000)
        return salt + hashed_password

    def verify_password(self, stored_password, input_password):
        salt = stored_password[:16]
        hashed_input_password = hashlib.pbkdf2_hmac('sha256', input_password.encode('utf-8'), salt, 100000)
        return hashed_input_password == stored_password[16:]

    def execute_command(self, command):
        try:
            output = os.popen(command).read()
            return output
        except Exception as e:
            return str(e)

    def authenticate(self):
        username = self.args.username
        password = self.args.password
        stored_password = crypt.crypt(password, salt=crypt.mksalt(crypt.METHOD_SHA256))
        if self.verify_password(stored_password, password):
            return True
        else:
            return False

    def run(self):
        if self.authenticate():
            command = self.args.command
            output = self.execute_command(command)
            print(output)
        else:
            print("Invalid credentials")

if __name__ == '__main__':
    cli = SecurCLI()
    cli.run()