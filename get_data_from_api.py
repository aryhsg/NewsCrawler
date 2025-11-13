import requests
import json
import os

cate = {
        "要聞": "cate1_news.json",
        "產業": "cate2_news.json",
        "證券": "cate3_news.json",
        "國際": "cate4_news.json",
        "金融": "cate5_news.json",
        "期貨": "cate6_news.json",
        "理財": "cate7_news.json",
        "房市": "cate8_news.json",
        "專欄": "cate9_news.json",
        "專題": "cate10_news.json",
        "商情": "cate11_news.json",
        "兩岸": "cate12_news.json"}




def get_data(category:str) -> json:
    base_url = "http://127.0.0.1:8000"
    endpoint = "/api/scrape-news/"
    params = {"category": category}
    api_url = f"{base_url}{endpoint}"

    try:
        response = requests.get(api_url, params=params)
        if response.status_code == 200:
            print("---API呼叫成功!!!---")
            
            data = response.json()

            json.dump(data, open(full_path, "w", encoding="utf-8"), indent=4, ensure_ascii=False)
            return(data)
        else:
            print(f"---API呼叫失敗...HTTP 狀態碼: {response.status_code}---")
            error_data = response.json()
            return(error_data)

    except requests.RequestException as e:
        print(f"網路連線錯誤或服務為啟動: {e}")


if __name__ == "__main__":
    category_list = ["要聞", "產業", "證券", "國際", "金融", "期貨", "理財", "房市", "專欄", "專題", "商情", "兩岸"]

    output_path = "./category_news/"
    if not os.path.exists(output_path):
        os.makedirs(output_path)

    for category in category_list:
        filename = cate[category]
        full_path = os.path.join(output_path, filename)
        get_data(category)