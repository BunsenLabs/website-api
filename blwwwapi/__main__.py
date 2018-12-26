#!/usr/bin/env python3
from argparse import ArgumentParser, Namespace, ArgumentDefaultsHelpFormatter
from blwwwapi.logging import named_logger
from blwwwapi.news import News
from blwwwapi.tracker import Tracker
from bottle import run, route, abort, response, install
from queue import Queue, Empty
from typing import Any
import blwwwapi.options
import os
import sys

logger = named_logger()

EMPTY={}
ENDPOINT_DATA = {}

def main() -> int:
  opts = blwwwapi.options.get()
  queue = Queue()
  threads = [
    News("news", opts, queue),
    Tracker("tracker", opts, queue),
  ]

  def poll_queue(key):
    while True:
      try:
        (id, payload) = queue.get(block=False)
        ENDPOINT_DATA[payload["endpoint"]] = payload["data"]
        queue.task_done()
      except Empty:
        break
    if key in ENDPOINT_DATA:
      return ENDPOINT_DATA[key]
    else:
      return EMPTY

  @route("/feed/news")
  def r_feed_news():
    return poll_queue("/feed/news")

  @route("/feed/news/atom")
  def r_feed_news_atom():
    response.content_type = "application/atom+xml; charset=utf-8"
    return poll_queue("/feed/news/atom")

  @route("/tracker/status")
  def r_tracker_status():
    return poll_queue("/tracker/status")

  for t in threads:
    t.start()

  run(
      host=opts.bind_ip,
      port=opts.bind_port,
      server="tornado",
      quiet=True
  )

  for t in threads:
    t.stop()
    t.join(timeout=.1)
    if t.is_alive():
      logger.warning("Thread [{id}] is still alive".format(id=t._id))

  return 0

if __name__ == "__main__":
  sys.exit(main())
