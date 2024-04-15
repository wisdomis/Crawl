# 매일경제 메인 화면에서 메인 기사를 크롤링


import requests
from bs4 import BeautifulSoup

def get_main_article(url):
    # URL에서 웹 페이지 내용 가져오기
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # 메인 기사의 HTML 구조에 따라 적절한 선택자 사용
    # 아래 선택자는 사이트 구조에 따라 변경될 수 있습니다.
    main_article = soup.select_one('.main_topnews ul li:first-child a')
    
    if main_article:
        article_link = main_article.get('href')
        article_response = requests.get(article_link)
        article_soup = BeautifulSoup(article_response.text, 'html.parser')

        # 기사 제목, 날짜, 기자, 내용 추출
        title = article_soup.select_one('.top_title').get_text().strip() if article_soup.select_one('.top_title') else 'No title'
        date = article_soup.select_one('.news_title_author .lasttime').get_text().strip() if article_soup.select_one('.news_title_author .lasttime') else 'No date'
        author = article_soup.select_one('.news_title_author .author').get_text().strip() if article_soup.select_one('.news_title_author .author') else 'No author'
        content = article_soup.select_one('.art_txt').get_text().strip() if article_soup.select_one('.art_txt') else 'No content'

        return {
            'title': title,
            'date': date,
            'author': author,
            'content': content
        }

    else:
        return "Error: 기사를 찾을 수 없습니다."

# 메인 함수 실행
if __name__ == "__main__":
    url = "https://www.mk.co.kr/"
    main_article_data = get_main_article(url)
    print(main_article_data)







response = requests.get(url)
print(response.status_code)
print(response.text[:500])  # 응답의 처음 500자만 출력

