import json

news = json.load(open("category_news.json", "r", encoding="utf-8"))
print(news["data"]["content"][0])