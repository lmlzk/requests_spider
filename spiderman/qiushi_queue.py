import requests
from lxml import etree
import json
from queue import Queue
import threading


class QiuBai(object):
    def __init__(self):
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_5) AppleWeb\
            Kit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36"}
        self.url_queue = Queue()
        self.html_queue = Queue()
        self.content_queue = Queue()

    def get_total_url(self):
        url_temp = 'https://www.qiushibaike.com/8hr/page/{}/'
        for i in range(1, 36):
            self.url_queue.put(url_temp.format(i))

    def parse_url(self):
        while True:
            url = self.url_queue.get()
            print("parsing url: ", url)
            response = requests.get(url, headers=self.headers, timeout=10)
            html = response.content.decode()
            html = etree.HTML(html)
            self.html_queue.put(html)
            self.url_queue.task_done()

    def get_content(self):
        while True:
            html = self.html_queue.get()
            total_div = html.xpath('//div[@class="article block untagged mb15"]')
            items = []
            for i in total_div:
                author_img = i.xpath('./div[@class="author clearfix"]/a[1]/img/@src')
                author_img = "https:" + author_img[0] if len(author_img) > 0 else None
                author_name = i.xpath('./div[@class="author clearfix"]/a[2]/h2/text()')
                author_name = author_name[0] if len(author_name) > 0 else None
                author_href = i.xpath('./div[@class="author clearfix"]/a[1]/@href')
                author_href = "https://www.qiushibaike.com" + author_href[0] if len(author_href) > 0 else None
                author_gender = i.xpath('./div[@class="author clearfix"]//div/@class')
                author_gender = author_gender[0].split(" ")[-1].replace("Icon", "") if len(author_gender) > 0 else None
                author_age = i.xpath('./div[@class="author clearfix"]//div/text()')
                author_age = author_age[0] if len(author_age) > 0 else None
                content = i.xpath('./a[@class="contentHerf"]/div/span/text()')
                content_vote = i.xpath('./div[@class="stats"]/span[1]/i/text()')
                content_vote = content_vote[0] if len(content_vote) > 0 else None
                content_comment_numbers = i.xpath('./div[@class="stats"]/span[2]/a/i/text()')
                content_comment_numbers = content_comment_numbers[0] if len(content_comment_numbers) > 0 else None
                hot_comment_author = i.xpath('./a[@class="indexGodCmt"]/div/span[last()]/text()')
                hot_comment_author = hot_comment_author[0] if len(hot_comment_author) > 0 else None
                hot_comment = i.xpath('./a[@class="indexGodCmt"]/div/div/text()')
                hot_comment = hot_comment[0].replace("\n：", "").replace("\n", "") if len(hot_comment) > 0 else None
                hot_comment_like_num = i.xpath('./a[@class="indexGodCmt"]/div/div/div/text()')
                hot_comment_like_num = hot_comment_like_num[-1].replace("\n", "") if len(hot_comment_like_num) > 0 else None
                item = dict(
                    author_name=author_name,
                    author_img=author_img,
                    author_href=author_href,
                    author_gender=author_gender,
                    author_age=author_age,
                    content=content,
                    content_vote=content_vote,
                    content_comment_numbers=content_comment_numbers,
                    hot_comment=hot_comment,
                    hot_comment_author=hot_comment_author,
                    hot_comment_like_num=hot_comment_like_num
                )
                items.append(item)
            self.content_queue.put(items)
            self.html_queue.task_done()

    def save_items(self):
        while True:
            items = self.content_queue.get()
            with open("qiu_bai.json", "a")as f:
                for i in items:
                    res = json.dumps(i, f, ensure_ascii=False, indent=2)
                    f.write(res)
            self.content_queue.task_done()

    def run(self):
        thread_list = []
        thread_url = threading.Thread(target=self.get_total_url)
        thread_list.append(thread_url)

        for i in range(10):
            thread_parse = threading.Thread(target=self.parse_url)
            thread_list.append(thread_parse)

        thread_get_content = threading.Thread(target=self.get_content)
        thread_list.append(thread_get_content)

        thread_save = threading.Thread(target=self.save_items)
        thread_list.append(thread_save)

        for t in thread_list:
            t.setDaemon(True)
            t.start()

        self.url_queue.join()
        self.html_queue.join()
        self.content_queue.join()

if __name__ == "__main__":
    qiu_bai = QiuBai()
    qiu_bai.run()
