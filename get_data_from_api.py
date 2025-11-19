import requests
import json
import os

SCRIPT_PATH = os.path.abspath(__file__)
BASE_DIR = os.path.dirname(SCRIPT_PATH)
all_news_data_path = os.path.join(BASE_DIR, "all_news_data")
cate_news_dir = os.path.join(BASE_DIR, "cate_news")


def curl_api():
    print("Fetching data from API...")
    all_news_data = requests.get(
        "http://aryhsgsnewsapi.onrender.com/api/scrape-all-news/"
    ).json()
    # 將獲取的數據寫入本地文件(json格式)
    try:
        with open(all_news_data_path, "w", encoding="utf-8") as f:
            json.dump(all_news_data, f, ensure_ascii=False, indent=4)
        print("Data successfully written to all_news_data")
    except Exception as e:
        print(f"Error writing to file: {e}")


def split_news_data(all_news_data_path):
    os.makedirs(cate_news_dir, exist_ok=True)
    with open(all_news_data_path, "r", encoding="utf-8") as f:
        all_news_data = json.load(f)

        for i in range(12):
            cate_news_path = os.path.join(cate_news_dir, f"cate{i}_news.json")
            json.dump(
                all_news_data["data"][i],
                open(cate_news_path, "w", encoding="utf-8"),
                ensure_ascii=False,
            )
        print("News data successfully split into categories.")


if __name__ == "__main__":
    curl_api()
    split_news_data(all_news_data_path)
