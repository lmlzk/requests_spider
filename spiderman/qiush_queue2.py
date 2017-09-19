import requests
from lxml import etree
import json
import threading
from queue import Queue


class Qiushi(object):
    def __init__(self):
        self.base_url = 'https://www.qiushibaike.com/8hr/page/{}/'
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) \
            AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36"
        }
        self.host = 'https://www.qiushibaike.com'
        self.url_queue = Queue()
        self.str_data_queue = Queue()
        self.data_queue = Queue()

    def generate_list(self):
        print('生成url列表')
        for i in range(1, 14):
            url = self.base_url.format(i)
            self.url_queue.put(url)

    def get_page(self):
        while True:
            url = self.url_queue.get()
            print('开始获取%s的响应' % url)
            try:
                response = requests.get(url, headers=self.headers)
                str_data = response.content.decode()
            except:
                str_data = None
            self.str_data_queue.put(str_data)
            self.url_queue.task_done()

    def parse_data(self):
        while True:
            str_data = self.str_data_queue.get()
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

            self.data_queue.put(data_list)
            self.str_data_queue.task_done()

    def save_data(self):
        while True:
            data_list = self.data_queue.get()
            print('开始存储文件')
            with open('qiushi_t2.json', 'a')as f:
                for data in data_list:
                    result = json.dumps(data, ensure_ascii=False) + ',\n'
                    f.write(result)
            self.data_queue.task_done()

    def run(self):
        thread_list = []
        t_url = threading.Thread(target=self.generate_list)
        thread_list.append(t_url)

        for i in range(4):
            t = threading.Thread(target=self.get_page)
            thread_list.append(t)

        for i in range(4):
            t = threading.Thread(target=self.parse_data)
            thread_list.append(t)

        t_save = threading.Thread(target=self.save_data)
        thread_list.append(t_save)

        for t in thread_list:
            t.setDaemon(True)
            t.start()

        for q in [self.data_queue,self.str_data_queue,self.url_queue]:
            q.join()

if __name__ == '__main__':
    qiushi = Qiushi()
    qiushi.run()
