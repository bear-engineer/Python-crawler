import os
from urllib import parse
import requests
from bs4 import BeautifulSoup

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
        """
        self.webtoon, self.no 요소를 사용하여
        실제 에피소드 페이지 URL을 리턴
        :return:
        """
        url = 'http://comic.naver.com/webtoon/detail.nhn?'
        params = {
            'titleId': self.webtoon.webtoon_id,
            'no':self.no,
        }

        episode_url = url + parse.urlencode(params)
        return episode_url

    def get_image_url_list(self):
        file_path = f'./data/{self.webtoon.webtonn_id}-{self.no}.html'

        if not os.path.exists(file_path):
            with open(file_path, 'wt') as f:
                response = requests.get(self.url)
                f.write(response.text)
            html = response.text
        else:
            html = open(file_path, 'rt').read()

        soup = BeautifulSoup(html, 'lxml')
        wt_viewer = soup.select_one('div.wt_viewer').select('img')

        for img in wt_viewer:
            new_ep_image = EpisodeImage(
                episode=self.no,
                url=img.get('src')
            )
            self.image_list.append(new_ep_image)
        return self.image_list

    def download_all_images(self):
        for url in self.get_image_url_list():
            self.download(url)

    def download(self, url_img):
        """
        :param url_img: 실제 이미지의 URL
        :return:
        """
        # 서버에서 거부하지 않도록 HTTP헤더 중 'Referer'항목을 채워서 요청
        url_referer = f'http://comic.naver.com/webtoon/list.nhn?titleId={self.webtoon}'
        headers = {
            'Referer': url_referer,
        }
        response = requests.get(url_img.url, headers=headers)

        # 이미지 URL에서 이미지명을 가져옴
        file_name = url_img.url.rsplit('/', 1)[-1]

        # 이미지가 저장될 폴더 경로, 폴더가 없으면 생성해준다.
        dir_path = f'data/{self.webtoon.webtoon_id}/{self.no}'
        os.makedirs(dir_path, exist_ok=True)

        # 이미지가 저장될 파일경로, 'wb' 모드로 열어 이진데이터를 기록한다.
        file_path = f'{dir_path}/{file_name}'
        open(file_path, 'wb').write(response.content)

        # 저장된 이미지를 인터넷에서 볼 수 있도록 html 파일로 생성
        with open(f'data/{self.webtoon.webtoon_id}/{self.no}.html', 'a') as f:
            f.write(f'<img src = {self.no}/{file_name}')
        