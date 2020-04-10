from argparse import Namespace
from queue import Queue
from threading import Thread

from blwwwapi.websocket_server import WebsocketServer

class EventServer(Thread):
  def __init__(self, opts: Namespace, events: Queue):
    self.opts = opts
    self.events = events
    super().__init__()

  def run(self):
    server = WebsocketServer(self.opts.event_server_port, self.events)
    server.serve_forever()
