import requests
from bs4 import BeautifulSoup
from feedgenerator import Rss201rev2Feed
from datetime import datetime

url = "https://finance.naver.com/news/news_list.naver?mode=LSS2D&section_id=101&section_id2=258"
res = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
soup = BeautifulSoup(res.text, 'html.parser')

rss = Rss201rev2Feed(
    title="네이버 증권 뉴스 RSS",
    link=url,
    description="비공식 네이버 증권 뉴스 피드",
    language="ko",
)

for li in soup.select("ul.newsList li"):
    a = li.find("a")
    if not a:
        continue
    title = a.get("title", "").strip()
    link = "https://finance.naver.com" + a.get("href", "")
    rss.add_item(title=title, link=link, description=title, pubdate=datetime.now())

with open("docs/naver_finance_news.xml", "w", encoding="utf-8") as f:
    rss.write(f, 'utf-8')
