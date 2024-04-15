import requests
from bs4 import BeautifulSoup

# 크롤링할 페이지의 URL
url = "https://news.naver.com/main/list.naver?mode=LPOD&mid=sec&oid=028"

# 페이지 내용 가져오기
response = requests.get(url)
html_content = response.text

# BeautifulSoup을 사용하여 HTML 파싱
soup = BeautifulSoup(html_content, "html.parser")

# 헤드라인과 URL, 날짜/시간을 담을 빈 리스트 생성
articles = []

# 모든 <a> 태그 찾기
for link in soup.find_all('a'):
    # 클래스가 "nclicks(cnt_flashart)" 인 링크인지 확인
    if "nclicks(cnt_flashart)" in link.get('class', []):
        # 헤드라인 텍스트 가져오기
        headline = link.text.strip()
        # 게시글 URL 가져오기
        url = link.get('href')
        # 게시글 날짜와 시간 가져오기
        datetime_tag = link.parent.find_next('span', class_='date')
        datetime = datetime_tag.text.strip() if datetime_tag else None
        # 가져온 정보가 모두 있으면 리스트에 추가
        if headline and url and datetime:
            articles.append({'headline': headline, 'url': url, 'datetime': datetime})

# 결과 출력
for article in articles:
    print("헤드라인:", article['headline'])
    print("URL:", article['url'])
    print("날짜/시간:", article['datetime'])
    print()