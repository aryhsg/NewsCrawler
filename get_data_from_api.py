import requests
import json
import os

SCRIPT_PATH = os.path.abspath(__file__)
BASE_DIR = os.path.dirname(SCRIPT_PATH)
all_news_data_path = os.path.join(BASE_DIR, "all_news_data")
cate_news_dir = os.path.join(BASE_DIR, "cate_news")
filepath = "./cate_news"
filenames = os.listdir(filepath)
cate_dict = {}
source_dict = {
    "要聞": "A",
    "產業": "B",
    "證券": "C",
    "國際": "D",
    "金融": "E",
    "期貨": "F",
    "理財": "G",
    "房市": "H",
    "專欄": "I",
    "專題": "J",
    "商情": "K",
    "兩岸": "L"
}

def curl_api():
    print("Fetching data from API...")
    all_news_data = requests.get(
        os.environ.get("RENDER_API")
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

            cate_news_path = os.path.join(cate_news_dir, f"cate{source_dict[i]}_news.json")
            json.dump(
                all_news_data["data"][i],
                open(cate_news_path, "w", encoding="utf-8"),
                ensure_ascii=False,
            )
        print("News data successfully split into categories.")

def change_datastra_to_meet_vb(cate_news: str):
    with open(f"./cate_news/{cate_news}", "r", encoding="utf-8") as f:
        news = json.load(f)


        
        for i in range(len(news["url"])):
            category = news["category"]
            cate_dict[f"{source_dict[category]}_{i}"] = {
                "category": news["category"],
                "url": news["url"][i],
                "title": news["title"][i],
                "content": news["content"][i]
            }
    json.dump(cate_dict, open("vb_news_dict", "w", encoding="utf-8"), ensure_ascii=False)

if __name__ == "__main__":
    curl_api()
    split_news_data(all_news_data_path)
    for filename in filenames:
        change_datastra_to_meet_vb(cate_news= filename)