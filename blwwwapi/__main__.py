from argparse import ArgumentParser
from blwwwapi.news import News
from blwwwapi.tracker import Tracker
from bottle import run, route, abort, response, install
from queue import Queue, Empty
import os
import sys

EMPTY={}
ENDPOINT_DATA = {}

def main():
  ap = ArgumentParser(description="""API endpoints for www.bunsenlabs.org""")
  ap.add_argument("--bind-ip", default="0.0.0.0")
  ap.add_argument("--bind-port", type=int, default=10000)
  ap.add_argument("--forum-url", default="https://forums.bunsenlabs.org")
  ap.add_argument("--tracker-url", default="http://127.0.0.1:6969")

  opts = ap.parse_args()
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

  run(host=opts.bind_ip, port=opts.bind_port, server="auto")

  for t in threads:
    t.stop()
    t.join()

  return 0

if __name__ == "__main__":
  sys.exit(main())
