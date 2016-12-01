#!/usr/bin/env python3

from bottle import run, route, abort
import requests

def fetchot(param):
    records = []
    try:
        data = requests.get("""http://127.0.0.1:6969/stats?{}""".format(param)).text
    except:
        return None
    for line in data.split('\n'):
        records.append(line)
    return records[:-1]

@route('/tracker/status')
def torrent_status():
    data = fetchot("mode=tpbs&format=txt")
    if data is None:
        abort(500, "You know")
    public = {}
    for line in data:
        [ hash, seeders, leechers ] = line.split(":", 3)
        public[hash.lower()] = { "s":seeders, "l":leechers }
    return public

if __name__ == "__main__":
    run(host="localhost", port=10101)
