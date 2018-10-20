#!/usr/bin/env python3

from argparse import Namespace
from blwwwapi.worker import Worker
from queue import Queue
from typing import Union, List
import requests
import time

class Tracker(Worker):
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
