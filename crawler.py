import requests
from pyquery import PyQuery


class Crawler(object):
    def __init__(self, start_url):
        self._s = requests.Session()
        self._s.get(start_url)

    def _crawl(self, url):
        return self._s.get(url).text

    def _query(self, document):
        return PyQuery(document)


