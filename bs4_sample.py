# weekday.html 파일의 내용을 불러와서 html이라는 변수에 할당
# f = open('weekday.html', 'rt')
# html = f.read()
# f.close()
# html = open('weekday.html', 'rt').read()
# import re
#
# with open('weekday.html', 'rt') as f:
#     html = f.read()
#
# result = re.findall(r'<a.*?>(.*?)</a>', html)
#
# print(result)

html_doc = """
<html><head><title>The Dormouse's story</title></head>
<body>
<p class="title"><b>The Dormouse's story</b></p>

<p class="story">Once upon a time there were three little sisters; and their names were
<a href="http://example.com/elsie" class="sister" id="link1">Elsie</a>,
<a href="http://example.com/lacie" class="sister" id="link2">Lacie</a> and
<a href="http://example.com/tillie" class="sister" id="link3">Tillie</a>;
and they lived at the bottom of a well.</p>

<p class="story">...</p>
"""

from bs4 import BeautifulSoup
soup = BeautifulSoup(html_doc, 'lxml')

# print(soup.title)
# print(soup.title.name)
# print(soup.title.string)
# print(soup.title.parent.name)
# print(soup.find_all('p'))

# print(html_doc)
# for anchor in soup.find_all('a'):
#     print(anchor.get('href'))

html = open('weekday.html', 'rt').read()

# div_content = soup.find('div', id='content')
# div_list_area = div_content.find('div', class_='list')

soup.select('a.title')
for a in a_list:
    print(a.get_text(strip=True))