import re

with open('weekday.html', 'rt') as f:
    urla = f.read()

p = re.compile(r'<.*?>(.*?)</.*?>', re.DOTALL)

result = re.findall(p, urla)

print(result)
# 전체 HTML 문서에서 '태그'를 찾고
# 해당 '태그' 의 내용을 그룹화
# 1.< 로 시작하고
# 2.사이에 임의의 문자열이 있으며(태그명과 속성, 값)
# 3.>로 끝난 후
# 4.임의이ㅡ 문자열이 있거나 없을 수도 있다(내용이 빈 태그)
# 5.다시< 를 만난 후
# 6.사이에 임의의 문자열이 있으며
# 7.>로 끝나는 경우



# def get_tag_content(tag_string):
