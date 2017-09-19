import requests
from lxml import etree
import json


class TieBa(object):
    def __init__(self, tie_ba_name, pn):
        self.tie_ba_name = tie_ba_name
        self.base_url = 'https://tieba.baidu.com/f?kw={}&ie=utf-8&pn='.format(self.tie_ba_name)
        self.url_list = [self.base_url + str(i*50) for i in range(pn)]
        self.headers = {
            "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 9_1 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) Version/9.0 Mobile/13B143 Safari/601.1",
        }

    def parse_url(self, url):
        print("parsing url: "+url)
        response = requests.get(url, headers=self.headers, timeout=10)
        html = response.content.decode()
        html = etree.HTML(html)
        return html

    def get_title_href(self, url):
        html = self.parse_url(url)
        li_temp_list = html.xpath("//li[@class='tl_shadow']")
        total_items = []
        for i in li_temp_list:
            href = "https:"+i.xpath("./a/@href")[0] if len(i.xpath("./a/@href")) > 0 else None
            text = i.xpath("./a/div[1]/span[1]/text()")
            text = text[0] if len(text) > 0 else None
            item = dict(
                href=href,
                text=text,
            )
            total_items.append(item)
        return total_items

    def get_img(self, url):
        html = self.parse_url(url)
        img_list = html.xpath('//div[@data-class="BDE_Image"]/@data-url')
        img_list = [i.split("src=")[-1] for i in img_list]
        img_list = [requests.utils.unquote(i) for i in img_list]
        return img_list

    def save_item(self, item):
        with open("teibatupian.txt", "a") as f:
            f.write(json.dumps(item, ensure_ascii=False, indent=2))
            f.write("\n")

    def run(self):
        for url in self.url_list:
            total_item = self.get_title_href(url)
            for item in total_item:
                href = item["href"]
                img_list = self.get_img(href)
                item["img"] = img_list
                print(item)
                self.save_item(item)

if __name__ == "__main__":
    tie_ba = TieBa("猫", 1)
    tie_ba.run()
