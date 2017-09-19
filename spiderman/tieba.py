#coding:utf-8

import requests
import sys


class TieBa(object):
    def __init__(self, tieba_name, pn):
        self.tieba_name = tieba_name
        self.base_url = 'https://tieba.baidu.com/f?kw={}&ie=utf-8&pn='.format(tieba_name)
        self.url_list = [self.base_url + str(i*50) for i in range(pn)]
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.101 Safari/537.36",
        }

    def get_page(self, url):
        response = requests.get(url, headers=self.headers)
        return response.content.decode()

    def save_data(self, data, number):
        filename = self.tieba_name + "_" + str(number+1) + '.html'
        with open(filename, 'w')as f:
            f.write(data)

    def run(self):
        print(self.url_list)
        for url in self.url_list:
            data = self.get_page(url)
            number = self.url_list.index(url)
            self.save_data(data, number)

if __name__ == '__main__':
    name = sys.argv[1]
    pn = sys.argv[2]

    tie_ba = TieBa(name, int(pn))
    tie_ba.run()
