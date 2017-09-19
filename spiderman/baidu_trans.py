import json

import requests


class BaiDuTrans(object):
    def __init__(self, word):
        self.url = 'http://fanyi.baidu.com/v2transapi'
        self.headers = {
           "User-Agent":
               "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.101 Safari/537.36",

        }
        self.post_data = {
            "from": "en",
            "to": "zh",
            "query": word,
            "simple_means_flag": 3,
        }

    def parse_data(self, data):
        result = json.loads(data)
        en_data = result['trans_result']['data'][0]['dst']
        print(en_data)

    def get_data(self):
        response = requests.post(self.url, headers=self.headers, data=self.post_data)
        return response.content.decode()

    def run(self):
        data = self.get_data()
        self.parse_data(data)


if __name__ == '__main__':
    baidu = BaiDuTrans("study")
    baidu.run()



