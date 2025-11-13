from news_crawler import NewsCrawler
from groq import Groq
from news_class import News
import groq_summary
import os
import json
import dotenv
dotenv.load_dotenv()

headers={
      'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36',
      'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
      'Accept-Language': 'zh-TW,zh;q=0.8,en-US;q=0.5,en;q=0.3',
      'Referer': 'https://money.udn.com/'
    }

if __name__ == "__main__":
    news  = News(source_type="專欄")
    crawler = NewsCrawler(headers=headers)
    crawler.generate_URLs(news.source_url)
    crawler.news_crawler()
    crawler.store_news()

    client = Groq(api_key=os.environ.get("GROQ_API_KEY"),)
    news_data = json.load(open("news_data.json", "r", encoding="utf-8"))
    groq_summary = groq_summary.generate_summary(news_data[0]["content"])

    picked_news = {
        "title": news_data[0]["title"],
        "url": news_data[0]["url"],
        "summary": groq_summary
    }

    json.dump(picked_news, open("picked_news.json", "w", encoding="utf-8"), ensure_ascii=False, indent=4)
    print("Picked news saved to picked_news.json")