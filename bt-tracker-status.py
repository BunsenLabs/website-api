#!/usr/bin/env python3

from bottle import run, route, abort
import threading
import time
import requests

PUBLIC = {}

class Fetcher(threading.Thread):
    
    def run(self):
        self.evt = threading.Event()
        self.update_data()
        while not self.evt.wait(timeout=10):
            self.update_data()

    def update_data(self):
        _public = {"torrents":{}}
        data = self.fetchot("mode=tpbs&format=txt")
        if data is None:
          print("No data")
          return True
        for line in data:
            [ hash, seeders, leechers ] = line.split(":", 3)
            _public["torrents"][hash.lower()] = { "s":seeders, "l":leechers }

        _public["completed"] = int(self.fetchot("mode=completed")[0])
        _public["ts"] = int(time.time())

        global PUBLIC
        PUBLIC = _public

    def fetchot(self, param):
        records = []
        try:
            data = requests.get("""http://127.0.0.1:6969/stats?{}""".format(param)).text
        except:
            return None
        for line in data.split('\n'):
            records.append(line)
        return records[:-1]

@route('/tracker/status')
def torrent_status():
    return PUBLIC

if __name__ == "__main__":
  fetcher = Fetcher()
  fetcher.start()
  run(host="localhost", port=10101, server="cherrypy")
