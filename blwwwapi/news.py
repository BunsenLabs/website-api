#!/usr/bin/env python3

from argparse import Namespace
from blwwwapi.worker import Worker
from bs4 import BeautifulSoup
from django.utils import feedgenerator
from queue import Queue
from typing import List
import datetime
import feedparser
import requests
import time

class News(Worker):
  def run(self):
    self._announcement_url = "{base_url}/extern.php?action=feed&fid=12&type=atom".format(
        base_url=self._opts.forum_url)
    self._info_forum_url = "{base_url}/viewforum.php?id=12".format(
        base_url=self._opts.forum_url)
    self.update_feed_data()
    while not self._waiter.wait(timeout=self._opts.news_update_interval):
      if self.is_stopped():
        return
      self.update_feed_data()

  def retrieve_op_data(self, topic_url: str) -> dict:
    text = ""
    date = "2017-01-01T00:00:00Z"
    try:
      body = requests.get(topic_url).text
      soup = BeautifulSoup(body, "html.parser")
      op = soup.find("div", { "class": "blockpost1" })
      # Summary
      p = op.find("div", { "class":"postmsg"}).find("p")
      for br in p.findAll("br"):
        br.replace_with(' ')
      text = p.prettify(formatter="html")
      # Full text
      fulltext = op.find("div", { "class":"postmsg"}).prettify(formatter="html")
      date = op.find("h2").find("a").text
      date = date.replace(" ", "T") + "Z"
      if "Today" in date:
        date = date.replace("Today", datetime.datetime.utcnow().strftime("%Y-%m-%d"))
      elif "Yesterday" in date:
        date = date.replace("Yesterday", (datetime.datetime.utcnow() - datetime.timedelta(days=1)).strftime("%Y-%m-%d"))
    except BaseException as e:
      self.error(e)
    return { "updated": date, "summary": text, "fulltext": fulltext }

  def update_feed_data(self) -> None:
    feed = feedparser.parse(self._announcement_url)
    refeed = feedgenerator.Atom1Feed('BunsenLabs Linux News', self._info_forum_url, "")
    json_entries = []

    for entry in feed.entries:
      self.log("Loading {link}".format(link = entry['link']))
      entry_data = self.retrieve_op_data(entry['link'])

      title = " ".join(entry['title'].split())
      link = self.head(entry['link'], '&')
      date = self.head(entry['updated'], 'T')
      updated = date
      op_summary = entry_data['summary']
      fulltext = entry_data['fulltext']

      refeed.add_item(title, link, fulltext,
          updateddate = datetime.datetime.strptime(updated, "%Y-%m-%d"))
      json_entries.append({ "link":       link,
                            "date":       date,
                            "updated":    updated,
                            "op_summary": op_summary,
                            "title":      title })

    self.emit(payload = {
      "endpoint": "/feed/news",
      "data": { "entries": json_entries, "ts": int(time.time()) }
    })
    self.emit(payload = {
      "endpoint": "/feed/news/atom",
      "data": refeed.writeString("utf-8"),
      "content_type": "application/atom+xml; charset=utf-8"
    })

  @staticmethod
  def head(s: str, sep: str) -> List[str]:
    return s.split(sep)[0]
