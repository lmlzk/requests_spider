import json
import requests
import sys


class YouDaoTrans(object):
    def __init__(self, word):
        self.url = 'http://fanyi.youdao.com/translate?smartresult=dict&smartresult=rule&smartresult=ugc&sessionFrom=null'
        self.headers = {
           'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:55.0) Gecko/20100101 Firefox/55.0'
        }

        self.formdata = {
            "i": word,
        "from": "AUTO",
        "to": "AUTO",
        "smartresult": "dict",
        "client": "fanyideskweb",
        "salt": "1504860511472",
        "sign": "0da6ae98dd8d9abd23129a01663dbfca",
        "doctype": "json",
        "version": "2.1",
        "keyfrom": "fanyi.web",
        "action": "FY_BY_CLICKBUTTION",
        "typoResult": "true",
        }

    def get_data(self):
        response = requests.post(url=self.url, headers=self.headers, data=self.formdata)
        return response.content.decode()

    def pase_data(self, data):
        res = json.loads(data)
        trans_data = res['translateResult'][0][0]['tgt']
        print(trans_data)

    def run(self):
        data = self.get_data()
        self.pase_data(data)

if __name__ == '__main__':
    word = sys.argv[1] if len(sys.argv) > 1 else 'Python'
    youdao = YouDaoTrans(word)
    youdao.run()
