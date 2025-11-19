from get_data_from_api import curl_api, split_news_data
import myTelegram

if __name__ == "__main__":
    curl_api()
    split_news_data()
    myTelegram.main()
