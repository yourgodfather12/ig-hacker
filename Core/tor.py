import os
import time
import socks
import socket
import subprocess
from concurrent.futures import ThreadPoolExecutor

class TorManager(object):
    def __init__(self):
        self.devnull = open(os.devnull, 'w')

    def installTor(self):
        subprocess.run(['clear'])
        print('Installing Tor, Please Wait...')
        time.sleep(3)
        cmd = ['apt-get', 'install', 'tor', '-y']
        subprocess.run(cmd, stdout=self.devnull, stderr=self.devnull)

    def restartTor(self):
        cmd = ['service', 'tor', 'restart']
        subprocess.run(cmd, stdout=self.devnull, stderr=self.devnull)
        time.sleep(0.5)

    def stopTor(self):
        cmd = ['service', 'tor', 'stop']
        subprocess.run(cmd, stdout=self.devnull, stderr=self.devnull)

    def updateIp(self):
        with ThreadPoolExecutor() as executor:
            executor.submit(self.restartTor)
            socks.setdefaultproxy(socks.PROXY_TYPE_SOCKS5, '127.0.0.1', 9050, True)
            socket.socket = socks.socksocket
