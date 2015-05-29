import requests
from pyquery import PyQuery
from celery import Celery


START_URL = 'http://music.163.com'
PLAYLISTS_URL = 'http://music.163.com/discover/playlist'

redis = Celery('playlist', broker='redis://local')


class Crawler(object):
    def __init__(self, start_url):
        self._s = requests.Session()
        self._s.get(start_url)

    def _crawl(self, url):
        return self._s.get(url).text

    def _query(slef, document):
        return PyQuery(document)


class MusicCrawl(Crawler):
    def __init__(self, start_url=START_URL):
        Crawler.__init__(self, start_url)
        self.tasks = []

    def get_playLists(self, url=PLAYLISTS_URL):
        return self._crawl(url)

    @redis.task
    def get_playList(self, url):
        url = START_URL + url
        return (url, self._crawl)

    def get_id(self, document, dom=None):
        for index in self._query(document)(dom):
            if index.attrib['class'] == 'msk':
                self.tasks.append(
                    self.get_playList(self, index.attrib['href'])
                    )

    def get_target(self, document, dom=None):
        return self._query(document)(dom)

    def process_tasks(self, task=tuple):
        i, j = task
        text = j(i).encode('utf-8')
        print text
        self.get_target(text, dom="")


def main():
    c = MusicCrawl(START_URL)
    res = c.get_playLists()
    text = res.encode('utf-8')
    c.get_id(text, "a[href*=\/playlist\?id]")
    i, j = c.tasks[0]
    print j(i).encode('utf-8')


if __name__ == '__main__':
    main()
