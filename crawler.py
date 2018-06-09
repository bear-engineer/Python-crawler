# http://comic.naver.com/webtoon/list.nhn?titleId=703845&weekday=wed
# 죽음에관하여(재) 페이지를
# requests 를 사용해서
# data/episode_list.html에 저장
# list.nhn뒤 ? 부터는 url 넣지말고 GET parameters로
# 저장 후에는 파일을 불러와 html 변수에 할당
#
# 1-2. dlal 'data/episode_list.html 이 있다면
# html 변수에 파일을 불러와 할당

import requests

import os

from bs4 import BeautifulSoup

file_path = 'data/episode_list.html'
url_episode = 'http://comic.naver.com/webtoon/list.nhn'
params = {'titleId': 703845}

if os.path.exists('data/episode_list.html') == True:
    html = open('data/episode_list.html', 'rt').read()
    print('True')
else:
    response = requests.get(url_episode, params)
    html = response.text
    html = open(file_path, 'wt').write(html)

soup = BeautifulSoup(html, 'lxml')

description = soup.select_one('div.detail > h2').get_text(strip=True)

print(description)



# 3. 에피소드 정보목록을 가져오기
# url_thumbnaol: 썸네일 URL
# title: 제목
# created_date: 등록일
# no: 에피소드 상세페이지 고유번호
# 각 에피소드들은 하나의 dict데이터
# 모든 에피소드들을 list에 넣는다.

# 에피소드 목록을 담고있는 테이블
table = soup.select_one('table.viewList')

# 테이블 내의 모든 tr 요소 목록
tr_list = table.select('tr')

from urllib import parse

url = "http://comic.naver.com/webtoon/list.nhn?titleId=703845&weekday=wed"
print(parse.urlsplit(url))

print(parse.parse_qs(parse.urlsplit(url).query))
print(dict(parse.parse_qs(parse.urlsplit(url).query)))


# for index, tr in enumerate(tr_list[1:]):
#     if tr.get('class'):
#         continue
#     # print('==={}===\n{}\n'.format(index, tr))
#     url_thumbnail = tr.select_one('td:nth-of-type(1) img').get('src')
#     url_detail = tr.select_one('tr > td:nth-of-type(1) > a').get('href')
#     title = tr.select_one('td:nth-of-type(2) > a').get_text(strip=True)
#     rating = tr.select_one('td:nth-of-type(3) strong').get_text(strip=True)
#     created_date = tr.select_one('td:nth-of-type(4)').get_text(strip=True)
#     print(url_detail)

# title_data = soup.find('td.title')
#
# url_thumbnaol = soup.select('td.title > a[href]')
# # title = soup.select('td.title > a').get_text("|", strip=True)
# for i in url_thumbnaol:
#     print(i)
#
# # for s in title:
# #     print(s)
# print(title_data.get_text())

class Episode:
    def __init__(self, webtoon_id, no, url_thumbnail, title, rating, created_date):
        self.webtoon = webtoon_id
        self.no = no
        self.url_thumbnail = url_thumbnail
        self.title = title
        self.rating = rating
        self.created_date = created_date

    @property
    def url_info(self):
            pass

