import requests
from lxml import etree
import json


class QiuShi(object):
    def __init__(self):
        self.base_url = 'https://www.qiushibaike.com/8hr/page/{}/'
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36"
        }
        self.host = 'https://www.qiushibaike.com'

    def generate_list(self):
        print('生成url列表')
        url_list = [self.base_url.format(i) for i in range(1, 14)]
        return url_list

    def get_page(self, url):
        print('开始获取%s的响应' % url)
        try:
            response = requests.get(url, headers=self.headers)
            return response.content.decode()
        except:
            return None

    def parse_data(self, str_data):
        print('开始解析数据')
        html = etree.HTML(str_data)

        node_list = html.xpath('//div[@id="content-left"]/div')

        data_list = []
        for node in node_list:
            temp = {}
            try:
                temp['user'] = node.xpath('./div[1]/a[2]/h2/text()')[0].strip()
                temp['zone_link'] = self.host + node.xpath('./div[1]/a[2]/@href')[0]
                temp['age'] = node.xpath('./div[1]/div/text()')[0]
                temp['gender'] = node.xpath('./div[1]/div/@class')[0]
            except:
                temp['user'] = '匿名用户'
                temp['zone_link'] = None
                temp['age'] = None
                temp['gender'] = None
            if not temp['gender']:
                pass
            elif 'women' in temp['gender']:
                temp['gender'] = 'women'
            else:
                temp['gender'] = 'man'
            temp['content'] = node.xpath('./a[1]/div/span/text()')[0].strip()
            temp['url'] = self.host + node.xpath('./a[1]/@href')[0]

            data_list.append(temp)

        return data_list

    def save_data(self, data_list):
        print('开始存储文件')
        with open('qiushi.json', 'a')as f:
            for data in data_list:
                result = json.dumps(data, ensure_ascii=False) + ',\n'
                f.write(result)

    def run(self):
        url_list = self.generate_list()
        for url in url_list:
            str_data = self.get_page(url)
            data_list = self.parse_data(str_data)
            self.save_data(data_list)

if __name__ == '__main__':
    qiu_shi = QiuShi()
    qiu_shi.run()
