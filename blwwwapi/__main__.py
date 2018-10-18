#!/usr/bin/env python3
from argparse import ArgumentParser, Namespace, ArgumentDefaultsHelpFormatter
from blwwwapi.news import News
from blwwwapi.tracker import Tracker
from blwwwapi.logging import named_logger
from bottle import run, route, abort, response, install
from queue import Queue, Empty
from typing import Any
import os
import sys

logger = named_logger()

EMPTY={}
ENDPOINT_DATA = {}

def get_options() -> Namespace:
  def env(opt: str, local_preference: Any, type=str) -> Any:
    key = "WWWAPI_{}".format(opt)
    if key in os.environ:
      return type(os.environ[key])
    else:
      return local_preference

  ap = ArgumentParser(description="""API endpoints for www.bunsenlabs.org""", formatter_class=ArgumentDefaultsHelpFormatter)
  ap.add_argument("--bind-ip", default=env("bind_ip", "127.0.0.1"), help="Bind IP address")
  ap.add_argument("--bind-port", type=int, default=env("bind_port", 10000, type=int), help="Bind IP port")
  ap.add_argument("--forum-url", default=env("forum_url", "https://forums.bunsenlabs.org"), help="URL to the FluxBB forum endpoint to use")
  ap.add_argument("--tracker-url", default=env("tracker_url", "http://127.0.0.1:6969"), help="URL of the OpenTracker HTTP interface")
  ap.add_argument("--news-update-interval", type=int, default=env("news_update_interval", 900, type=int), help="News feed update interval in seconds.")
  ap.add_argument("--tracker-update-interval", type=int, default=env("tracker_update_interval", 10, type=int), help="OpenTracker stats update interval in seconds.")

  return ap.parse_args()

def main() -> int:
  opts = get_options()
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
