#!/usr/bin/env python3

from blwwwapi.workers.base import WorkerBase
from typing import Union, List
import requests
import time

class Tracker(WorkerBase):
    _id = "tracker"
    __known_torrents = []

    def main(self):
        self.update_data()
        while not self._waiter.wait(timeout=self._opts.tracker_update_interval):
            if self.is_stopped():
              return
            self.update_data()
        return 0

    def update_data(self):
        queuedata = {"torrents":{}}
        data = self.fetchot("mode=tpbs&format=txt")
        if data is None:
          self.error("Could not fetch data.")
          return
        for line in data:
            [ hash, seeders, leechers ] = line.split(":", 3)
            queuedata["torrents"][hash.lower()] = { "s":int(seeders), "l":int(leechers) }
            if not hash in self._known_torrents:
                self.__known_torrents.append(hash)
                self.log(f"Discovered torrent {hash} having {seeders} seeders and {leechers} leechers")
        for hash in self._known_torrents:
            if not hash in queuedata["torrents"]:
                self.__known_torrents.remove(hash)
                self.log(f"Torrent {hash} vanished")
        queuedata["ts"] = int(time.time())
        self.emit(payload = {
            "endpoint": "/tracker/status",
            "data": queuedata
        })

    def fetchot(self, param: str) -> Union[None, List[str]]:
        records = []
        try:
            data = requests.get("{url}/stats?{params}".format(
              url=self._opts.tracker_url, params=param)).text
        except:
            return None
        for line in data.split('\n'):
            records.append(line)
        return records[:-1]
