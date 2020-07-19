from flask import Flask, Response, make_response
from flask_restful import Resource, Api

from .broker import Broker
from .logging import named_logger
from .settings import Settings

settings = Settings()
broker = Broker(settings)
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

api.add_resource(Newsfeed, '/feed/news', '/feed/news/<string:format>')
api.add_resource(TrackerStatus, '/tracker/status')

if __name__ == "__main__":
  app.run()
