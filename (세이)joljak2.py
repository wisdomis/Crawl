from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup

# 크롬 드라이버 설정
chrome_options = Options()
chrome_options.add_argument("--headless")  # 브라우저 창을 표시하지 않고 실행
chrome_options.add_argument("--disable-gpu")  # GPU 가속을 사용하지 않도록 설정
service = Service(ChromeDriverManager().install())

# Chrome 드라이버 실행
driver = webdriver.Chrome(service=service, options=chrome_options)

# 웹 페이지에 접속하여 기사 정보 추출
url = "https://news.naver.com/main/list.naver?mode=LPOD&mid=sec&oid=005&listType=title&date=20240413"
driver.get(url)

# 페이지 소스를 BeautifulSoup로 파싱
soup = BeautifulSoup(driver.page_source, 'html.parser')

# 기사 제목과 작성 날짜/시간, 링크 주소 추출
articles = soup.find_all('a', class_='nclicks(cnt_flashart)')

for article in articles:
    title = article.text.strip()  # 기사 제목 추출
    link = article['href']  # 기사 링크 추출
    
    print("제목:", title)
    print("링크 주소:", link)

    # 기사 페이지로 이동하여 기사 내용 추출
    driver.get(link)
    WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'div#articleBodyContents')))
    article_html = driver.page_source
    article_soup = BeautifulSoup(article_html, 'html.parser')
    
    # 기사 내용 추출
    content_element = article_soup.find('div', id='articleBodyContents')
    content = content_element.text.strip() if content_element else "기사 내용 없음"
    print("내용:", content)
    print()

# 브라우저 종료
driver.quit()
