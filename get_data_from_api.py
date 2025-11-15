import requests
import json
import os

def split_news_data(
    input_file_name: str = "all_news_data"):
        source_dict = {
         "要聞": 0, "產業": 1, "證券": 2, "國際": 3, "金融": 4, "期貨": 5, "理財": 6, "房市": 7,
         "專欄": 8, "專題": 9, "商情": 10, "兩岸":11
}

        with open("all_news_data", "r", encoding="utf-8") as f:
                all_news_data = json.load(f)

                for i in range(12):
                  json.dump(all_news_data["data"][i] , open(f"cate{i}_news.json", "w"), ensure_ascii=False)

if __name__ == "__main__":
        split_news_data("all_news_data")

