#!/usr/bin/env python3

import sys

EMPTY={}
ENDPOINT_DATA = {}

def main() -> int:
  # Load options early to handle --help efficiently.
  import blwwwapi.options
  opts = blwwwapi.options.get()

  from blwwwapi.logging import named_logger
  from blwwwapi.message import Message
  from blwwwapi.workers.news import News
  from blwwwapi.workers.tracker import Tracker
  from bottle import run, route, abort, response, install
  from queue import Queue, Empty
  from typing import Any
  import os
  import pickle

  logger = named_logger()
  queue = Queue()
  whitelist = opts.workers.split(",")
  classes = [ News, Tracker ]
  params = (opts,queue,)
  threads = []

  def check_namespace_access(thread_id: str, endpoint: str) -> bool:
    if not endpoint.startswith(f"/{thread_id}"):
      logger.warning(f"Thread {thread_id} tried accessing foreign endpoint {endpoint}")
      return False
    return True

  def _put(msg):
    id = msg.sender
    endpoint = msg.payload["endpoint"]
    data = msg.payload["data"]
    if check_namespace_access(id, endpoint):
      ENDPOINT_DATA[endpoint] = data

  def _clear(msg):
    id = msg.sender
    endpoint = msg.payload["endpoint"]
    if check_namespace_access(id, endpoint):
      ENDPOINT_DATA[endpoint] = EMPTY

  jump = { "PUT": _put, "CLEAR": _clear }

  def poll_queue(key):
    while True:
      try:
        id, data = queue.get(block=False)
        queue.task_done()
        try:
          msg = pickle.loads(data)
        except pickle.PickleError as err:
          logger.error(f"Failed to unpickle a message from worker: {id}")
          sys.exit(os.EX_PROTOCOL)
        try:
          jump[msg.verb](msg)
        except KeyError:
          logger.error(f"Received message with unknown verb: {msg.verb}")
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

 
  for cls in classes:
    if cls._id in whitelist:
      logger.info(f"Starting worker: {cls._id}")
      thread = cls(*params)
      thread.start()
      threads.append(thread)
    else:
      logger.info(f"Worker is disabled: {cls._id}")

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
      logger.warning(f"Worker is still alive after joining: {t._id}")

  return 0

if __name__ == "__main__":
  sys.exit(main())
