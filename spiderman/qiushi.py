import json
import requests
from retrying import retry
from lxml import etree


class QiuBaiSpider(object):
    def __init__(self):
        self.url = "http://www.qiushibaike.com/8hr/page/{}/"
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36"
        }

    @retry(stop_max_attempt_number=5)  # 调用retry，当assert出错时候，重复请求5次
    def parse_url(self, url):
        response = requests.get(url, timeout=10, headers=self.headers) #请求url
        assert response.status_code == 200  # 当响应码不是200时候，做断言报错处理
        print(url)
        return etree.HTML(response.text)  # 返回etree之后的html

    def parse_content(self, html):
        item_temp = html.xpath('//div[@id="content-left"]/div')

        data_list = []

        for item in item_temp:
            avatar = item.xpath("./div[1]/a[1]/img/@src")[0] if len(item.xpath("./div[1]/a[1]/img/@src"))>0 else None
            if avatar is not None and not avatar.startswith("http:"):
                avatar = "http:"+avatar
            try:
                name = item.xpath("./div[1]/a[2]/h2/text()")[0].strip()
            except:
                name = '匿名用户'
            content = item.xpath("./a[@class='contentHerf']/div/span/text()")[0].strip()
            star_number = item.xpath("./div[@class='stats']/span[1]/i/text()")[0] .strip()
            comment_number = item.xpath("./div[@class='stats']/span[2]/a/i/text()")[0].strip()
            data = dict(
                avatar=avatar,
                name=name,
                content=content,
                star_number=star_number,
                comment_number=comment_number,
            )
            data_list.append(data)
        return data_list

    def generate_list(self):
        print('生成url列表')
        url_list = [self.url.format(i) for i in range(1, 14)]
        return url_list

    def save_data(self, data_list):
        with open('qiu__shi.json', 'a')as f:
            for data in data_list:
                result = json.dumps(data, ensure_ascii=False) + ',\n'
                f.write(result)

    def run(self):
        url_list = self.generate_list()
        for url in url_list:
            html = self.parse_url(url)
            data_list = self.parse_content(html)
            self.save_data(data_list)

if __name__ == "__main__":
    qiu_bai = QiuBaiSpider()
    qiu_bai.run()
