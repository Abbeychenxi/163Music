import re
from multiprocessing import Pool


# import SQLAlchemy


from crawler import Crawler


START_URL = 'http://music.163.com'
PLAYLIST_URL = 'http://music.163.com/discover/playlist'
USER_URL = 'http://music.163.com/usr/home?id='
MUSIC_URL = 'http://music.163.com/song?id='


class MusicCrawl(Crawler):
    def __init__(self, start_url=START_URL):
        Crawler.__init__(self, start_url)
        self.tasks = []

    def get_playLists(self, url=PLAYLIST_URL):
        return self._crawl(url)

    def get_playList(self, url):
        url = START_URL + url
        return (url, self._crawl)

    def get_id(self, document, dom=None):
        for index in self._query(document)(dom):
            if index.attrib['class'] == 'msk':
                self.tasks.append(
                    self.get_playList(index.attrib['href'])
                    )

    def get_target(self, document):
        dom = self._query(document)
        title = dom("h2.f-ff2.f-brk").text()
        authorInfo = dom("div.user.f-cb a.s-fc7")
        id = re.search('\d+', authorInfo.attr['href']).group()
        author = (authorInfo.text(), id)
        collection = dom('div.btns.f-cb.j-action a i').text().split(' ')[1:]
        collection = [re.search('\d+', i).group() for i in collection]
        tags = dom('div.tags.f-cb a').text()
        description = dom('div.cntc p.intr.f-brk').text()
        playNum = dom('strong.s-fc6.j-play-count').text()
        listLen = re.search('\d+',
                            dom('span.sub.s-fc3.j-track-count').text()).group()
        musicList = dom('span.txt a')
        musics = []
        for i in musicList:
            if i.attrib['href'].startswith('/song?id='):
                musics.append(re.search('\d+', i.attrib['href']).group())
        result = (title, author, tags, description,
                  playNum, listLen, musics)
        print(result)

    def assign_task(self):
        pool = Pool(processes=4)
        pool.map(self.process_tasks, self.tasks)

    def process_tasks(self, task=tuple):
        url, handler = task
        text = handler(url).encode('utf-8')
        self.get_target(text)

    def save_info(self, result):
        pass


def main():
    c = MusicCrawl(START_URL)
    res = c.get_playLists()
    text = res.encode('utf-8')
    c.get_id(text, "a[href*=\/playlist\?id]")
    c.assign_task()


if __name__ == '__main__':
    main()
