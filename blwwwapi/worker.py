from threading import Thread, Event
from argparse import Namespace
from queue import Queue

class Worker(Thread):
  def __init__(self, id: str, opts: Namespace, queue: Queue):
    self._id = id
    self._opts = opts
    self._queue = queue
    self._stop_event = Event()
    self._waiter = Event()
    super().__init__(daemon=True)

  def log(self, msg):
    print("[{id}] {msg}".format(id=self._id, msg=msg))

  def stop(self) -> None:
    self._stop_event.set()

  def is_stopped(self) -> bool:
    return self._stop_event.is_set()

  def emit(self, payload = { "endpoint": "/", "data": str() }) -> None:
    self._queue.put((self._id, payload,))
