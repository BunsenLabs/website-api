from argparse import Namespace
from queue import Queue, Empty
from threading import Thread, Lock
import os
import pickle
import sys

from .logging import named_logger
from .settings import Settings
from .workers.news import News
from .workers.tracker import Tracker

EMPTY = {}

class Broker(Thread):
  def __init__(self, settings: Settings):
    self.data = {}
    self.logger = named_logger()
    self.queue = Queue()
    self.workers = [ News, Tracker ]
    self.params = (settings, self.queue,)
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
    while True:
      try:
        id, data = self.queue.get(block=True)
        self.queue.task_done()
        try:
          msg = pickle.loads(data)
        except pickle.PickleError as err:
          self.logger.error(f"Failed to unpickle a message from worker: {id}")
          sys.exit(os.EX_PROTOCOL)
        if msg.verb == 'PUT':
          self._put(msg)
        elif msg.verb == 'CLEAR':
          self._clear(msg)
        else:
          self.logger.error(f"Received message with unknown verb: {msg.verb}")
      except Empty:
        pass

  def _put(self, msg):
    id = msg.sender
    endpoint = msg.payload["endpoint"]
    data = msg.payload["data"]
    if self._check_namespace_access(id, endpoint):
      with self.lock:
        self.data[endpoint] = data

  def _clear(self, msg):
    id = msg.sender
    endpoint = msg.payload["endpoint"]
    if self._check_namespace_access(id, endpoint):
      with self.lock:
        self.data[endpoint] = EMPTY

  def _check_namespace_access(self, thread_id: str, endpoint: str) -> bool:
    if not endpoint.startswith(f"/{thread_id}"):
      self.logger.warning(f"Thread {thread_id} tried accessing foreign endpoint {endpoint}")
      return False
    return True
