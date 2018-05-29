# 우리가 웹 브라우저를 통해 보는 HTML 문서는 GET 요청의 결과
# requests 를 사용해 https://comic.naver.com/webtoon/weekday.nhn 주소
# 요청 결과를 response 변수에 할당해서 status_code 속성을 출력

import requests

response = requests.get('https://comic.naver.com/webtoon/weekday.nhn')
print(response.status_code)
# HTTP GET요청으로 받아온 Content를 text 데이터로 리턴
print(response.text)
# response.text에 해당하는 데이터를
# weekday,html 이라는 파일에 기록
# 다 기록했으면 close() 호출

write_test = open('weekday.html', 'wt')
write_test.write(response.text)
write_test.close()
