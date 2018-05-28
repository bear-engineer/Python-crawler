import re
# with open('re_weekday_iteml_title.html', 'rt') as f:
#     html = f.read()

with open('weekday.html', 'rt') as t:
    title = t.read()

# <a...(임의의 텍스트)class="title"...>[내용]</a>
# [내용] 에 해당하는 부분을 추출하는 정규표현식을 작성해서
# 실행한 결과 -> '유미의 세포들' 이라고 나올 수 있도록
# 1.<a 로 시작해서
# 2.임의의 문자가 최소 반복으로(>가 등장하기 전까지)
# 3.>문자
# 4.<가 등장하기 전까지의 임의의 문자 반복을 그룹화
# 5. </a>문자

# 정규표현식 패턴 (a태그이며, class="title" 이 여는 태그에 포함되어있을 경우, 해당 a태그의 내용부분을 그룹화)

p = re.compile(r'''<a                  # <a로 시작하며
                   .*class="title".*?> # 중간에 class="title" 문자열이 존재하며
                   .*?>                # >가 등장하기전까지 임의의 문자 최소 반복, >까지
                  (.*?)                # 임의의 문자 반복
                  </a>                 # </a>가 나오기 전까지''', re.VERBOSE)

p = re.compile(r'<a.*class="title".*?>(.*?)</a>')

result = re.findall(p, title)

print(result)
