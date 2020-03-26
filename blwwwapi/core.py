from blwwwapi.broker import Broker
from blwwwapi.logging import named_logger
from blwwwapi.options import get as getopts
from flask import Flask, Response, make_response
from flask_restful import Resource, Api

opts = getopts()
broker = Broker(opts)
broker.start()

app = Flask('blwwwapi')
api = Api(app)

class Newsfeed(Resource):
  def get(self, format: str = 'json'):
    if format == 'json':
      return broker.query('/feed/news')
    elif format == 'atom':
      return broker.query('/feed/news/atom'), 200, {'Content-Type':'application/atom+xml; charset=utf-8'}
    return 'Bad request.', 400

class TrackerStatus(Resource):
  def get(self):
    return broker.query('/tracker/status')

api.add_resource(Newsfeed,
    '/api/v2/feed/news',
    '/api/v2/feed/news/<string:format>'
)

api.add_resource(TrackerStatus,
    '/api/v2/tracker/status'
)

if __name__ == "__main__":
  app.run()
