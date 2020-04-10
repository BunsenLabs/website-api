from argparse import Namespace
from queue import Queue, Empty, Full
from threading import Thread, Lock
from typing import Callable, Optional
import json
import os
import pickle
import sys

from blwwwapi.eventserver import EventServer
from blwwwapi.logging import named_logger
from blwwwapi.workers.news import News
from blwwwapi.workers.tracker import Tracker

EMPTY = {}

class Broker(Thread):
  def __init__(self, opts: Namespace = Namespace()):
    self.data = {}
    self.opts = opts
    self.logger = named_logger()
    self.queue = Queue(maxsize=512)
    self.workers = [ News, Tracker ]
    self.event_server: Optional[EventServer] = None
    self.event_server_queue: Optional[Queue] = None
    self.params = (opts,self.queue,)
    self.threads = []
    self.lock = Lock()
    super().__init__()

  def query(self, endpoint):
    with self.lock:
      if endpoint in self.data:
        return self.data[endpoint]
      else:
        return EMPTY

  def run(self):
    for cls in self.workers:
      self.logger.info(f"Starting worker: {cls._id}")
      w = cls(*self.params)
      w.start()
      self.threads.append(w)
    if self.opts.event_server_enable:
      self.event_server_queue = Queue()
      self.event_server = EventServer(self.opts, self.event_server_queue)
      self.event_server.start()
      self.threads.append(self.event_server)
    while True:
      try:
        id, data = self.queue.get(block=True)
        self.queue.task_done()
        try:
          msg = pickle.loads(data)
        except pickle.PickleError as err:
          self.logger.error(f"Failed to unpickle a message from worker: {id}")
          sys.exit(os.EX_PROTOCOL)
        self._put(msg)
      except Empty:
        pass

  def _put(self, msg):
    id = msg.sender
    endpoint = msg.payload["endpoint"]
    data = msg.payload["data"]
    if self._check_namespace_access(id, endpoint):
      with self.lock:
        self.data[endpoint] = data
    if self.event_server_queue is not None:
      try:
        self.event_server_queue.put(json.dumps(msg.payload), block=False)
        self.logger.debug("Added event to event server queue: %s", msg)
      except Full as err:
        self.logger.warning("Failed to submit message to event server: %s", err)

  def _check_namespace_access(self, thread_id: str, endpoint: str) -> bool:
    if not endpoint.startswith(f"/{thread_id}"):
      self.logger.warning(f"Thread {thread_id} tried accessing foreign endpoint {endpoint}")
      return False
    return True
