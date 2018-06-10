import os
from urllib import parse
from bs4 import BeautifulSoup
import requests


class EpisodeImage:
    def __init__(self, episode, url):
        self.episode = episode
        self.url = url

class Episode:
    def __init__(self, webtoon, no, url_thumbnail, title, rating, created_date):
        self.webtoon = webtoon
        self.no = no
        self.url_thumbnail = url_thumbnail
        self.title = title
        self.rating = rating
        self.created_date = created_date
        self.image_list = list()

    @property
    def url(self):
        url = 'http://comic.naver.com/webtoon/detail.nhn?'
        params = {
            'titleId': self.webtoon.webtoon_id,
            'no': self.no
        }

        episode_url = url + parse.urlencode(params)
        return episode_url

    def get_image_url_list(self):
        file_path = f'./data/{self.webtoon.webtoon_id}_{self.no}.html'

        if not os.path.exists(file_path):
            response = requests.get(self.url)
            html = response.text
            open(file_path, 'wt').write(html)
        else:
            html = open(file_path, 'rt').read()
        soup = BeautifulSoup(html, 'lxml')
        wt_viewer = soup.select_one('div.wt_viewer').select('img')

        for img in wt_viewer:
            new_ep_imge = EpisodeImage(
                episode=self.no,
                url=img.get('src')
            )
            self.image_list.append(new_ep_imge)
        return self.image_list

    def download_all_images(self):
        for url in self.get_image_url_list():
            self.download(url)

    def download(self, url_img):
        url_referer = f'http://comic.naver.com/webtoon/list.nhn?titleId={self.webtoon}'
        headers = {
            'Referer': url_referer,
        }
        response = requests.get(url_img.url, headers=headers)
        file_name = url_img.url.rsplit('/', 1)[-1]

        dir_path = f'data/{self.webtoon.webtoon_id}/{self.no}'
        os.makedirs(dir_path, exist_ok=True)

        file_path = f'{dir_path}/{file_name}'
        open(file_path, 'wb').write(response.content)

        with open(f'data/{self.webtoon.webtoon_id}/{self.no}.html') as f:
            f.write(f'<img src = {self.no}/{file_name}>')

class Webtoon:
    def __init__(self, webtoon_id):
        self.webtoon_id = webtoon_id
        self._title = None
        self._author = None
        self._description = None
        self._episode_list = list()
        self._html = ''
        self.page = 1

    @property
    def html(self):
        file_path = f'data/_episode_list-{self.webtoon_id}-{self.page}.html'
        url_episode_list = 'http://comic.naver.com/webtoon/list.nhn'
        params = {
            'titleId':self.webtoon_id,
            'page': self.page,
        }

        if os.path.exists(file_path):
            html = open(file_path, 'rt').read()
        else:
            response = requests.get(url_episode_list, params)
            html = response.text
            open(file_path, 'wt').write(html)
        self._html = html
        return self._html

    def set_info(self):
        soup = BeautifulSoup(self.html, 'lxml')

        h2_title = soup.select_one('div.detail > h2')
        title = h2_title.contents[0].strip
        author = h2_title.contents[1].get_text(strip=True)
        description = soup.select_one('div.detail > p').get_text(strip=True)

        self._title = title
        self._author = author
        self._description = description

    def _get_info(self, attr_name):
        if not getattr(self, attr_name):
            self.set_info()
        return getattr(self, attr_name)

    @property
    def title(self):
        return self._get_info('_title')
    @property
    def author(self):
        return self._get_info('_author')
    @property
    def description(self):
        return self._get_info('_description')

    @property
    def episode_list(self):
        if not self._episode_list:
            self.crawl_episode_list()
        return self._episode_list

    @property
    def info(self):
        return f'{self.title}\n' \
               f'작가 : {self.author}\n' \
               f'스토리 : {self.description}\n' \
               f'총 편수{len(self.episode_list)}'

    @classmethod
    def all_webtoon_crawler(cls, keyword):
        url = 'https://comic.naver.com/webtoon/weekday.nhn'
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'lxml')
        all_webtoon_list = soup.select('div.col_inner > ul > li > a')
        result = list()

        for webtoon in all_webtoon_list:
            title = webtoon.get_text()
            if keyword in title:
                href = webtoon.get('href', '')
                query_string = parse.urlsplit(href).query
                query_dict = dict(parse.parse_qsl(query_string))
                titleId = query_dict['titleId']
                check = [item for item in result if item['titleId'] == titleId]
                if not check:
                    result.append({
                        'titleId': titleId,
                        'title': title,
                    })
        return result

    @classmethod
    def search_webtoon(cls, keyword):
        search_result = cls.all_webtoon_crawler(keyword)
        result_list = list()
        if search_result:
            for webtoon in search_result:
                webtoon_title_id = cls(webtoon_id=webtoon['titleId'])
                result_list.append(webtoon_title_id)
        return result_list

    def crawl_episode_list(self):
        while True:
            soup = BeautifulSoup(self.html, 'lxml')
            table = soup.select_one('table.viewList')
            tr_list = table.select('tr')
            episode_list = list()

            for index, tr in enumerate(tr_list[1:]):
                if tr.get('class'):
                    continue
                url_thumbnail = tr.select_one('td:nth-of-type(1) img').get('src')
                url_detail = tr.select_one('td:nth-of-type(1) > a').get('href')
                query_string = parse.urlsplit(url_detail).query
                query_dict = parse.parse_qs(query_string)
                no = query_dict['no'][0]

                title = tr.select_one('td:nth-of-type(2) > a').get_text(strip=True)
                rating = tr.select_one('td:nth-of-type(3) strong').get_text(strip=True)
                created_date = tr.select_one('td:nth-of-type(4)').get_text(strip=True)

                new_episode = Episode(
                    webtoon=self,
                    no=no,
                    url_thumbnail=url_thumbnail,
                    title=title,
                    rating=rating,
                    created_date=created_date,
                )
                self._episode_list.append(new_episode)
            if no == '1':
                break
            else:
                self.page += 1

