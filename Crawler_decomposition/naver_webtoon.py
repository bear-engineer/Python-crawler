from bs4 import BeautifulSoup
import os
import requests
from urllib import parse



def get_url():
    url = 'https://comic.naver.com/webtoon/weekday.nhn'
    file_path = 'data/webtoon_list.html'
    if os.path.exists(file_path):
        html = open(file_path, 'rt').read()
        print('webtoon_list 파일을 불러왔습니다.')
    else:
        response = requests.get(url)
        html = response.text
        open(file_path, 'wt').write(html)
        print('file_path 경로에 html 파일이 없어 생성했습니다.')
    return html

get_url()

def crawler():
    soup = BeautifulSoup(get_url(),'lxml')
    title = soup.select('div.col_inner > ul > li > a')

    title_list = []
    for item in title:
        href = item.get('href')
        query_dict = parse.parse_qs(parse.urlsplit(href).query)
        webtoon_id = query_dict.get('titleId')[0]
        webtoon_title = item.string
        title_list.append({
            'webtoon_id': webtoon_id,
            'title':webtoon_title,
        })
    result_list = []
    for title_dict in title_list:
        # result_list.append({title_dict['title']:title_dict['webtoon_id']})
        print(title_dict['title'], title_dict['webtoon_id'])
    keyword = input()




crawler()