import json
import os

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
filepath = "./cate_news"
file = os.listdir(filepath)
cate_dict = {}
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
    json.dump(cate_dict, open("testdict", "w", encoding="utf-8"), ensure_ascii=False)


if __name__ == "__main__":
    
    for filename in file: 
        print(filename)
        change_datastra_to_meet_vb(cate_news= filename)