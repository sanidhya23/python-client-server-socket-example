import os
import time
import json
from multiprocessing.connection import Client

class FileMon(object):
    """Class for monitroing file and store its content"""
    def __init__(self):
        self.cached_mtime = 0
        self.is_updated = True
        self.filename = './ssid.json'
        self.content = json.loads('{}')

    def file_checker(self):
        """Check if file last modified time is different than recorded one"""
        stamp = os.stat(self.filename).st_mtime
        if stamp != self.cached_mtime:
            self.cached_mtime = stamp
            self.is_updated = True
            self.content = json.load(open(self.filename))
        else:
            self.is_updated = False


if __name__ == '__main__':
    sleep_interval_sec = 5
    # Create file monitoring object
    f = FileMon()
    # Initialise client 
    conn = Client(('localhost', 6000), authkey=b'secret-password')
    
    # Keep monitoring the file after set interval
    while True:
        f.file_checker()
        if f.is_updated:
            print(f"Sending: {f.content}")
            conn.send(f.content)
        time.sleep(sleep_interval_sec)



