import random
import threading
from queue import Queue
from selenium import webdriver
import json
import time
from selenium.webdriver import ActionChains
from selenium.webdriver.support.ui import Select

from crawl_desc import JobDesc

WORK_EXP = {
    '不限': '1',
    '应届毕业生': '2',
    '3年及以下': '3',
    '3-5年': '4',
    '5-10年': '5',
    '10年以上': '6',
    '不要求': '7',
}

WORK = {
    '全职': '2',
}

SEARCH = {
    '数据分析', '爬虫', '后端', '数据'
}


class LaGou(object):
    sleeping = 10
    def __init__(self, search):
        self.search = search
        option = webdriver.ChromeOptions()
        option.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; \
                            x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.101 Safari/537.36')
        self.drive = webdriver.Chrome(chrome_options=option)
        # self.drive = webdriver.Chrome()
        # self.url = 'https://www.lagou.com/jobs/list_python?gj={}px=new&gx={}&city={}'.format('3年及以下', '全职', '北京')
        self.url = 'https://www.lagou.com/jobs/list_python{}'.format(search)
        self.drive.get(self.url)
        print("get_refer")
        # print(self.drive.get_cookies())
        # {cookie[‘name’]: cookie[‘value’] for cookie in driver.get_cookies()}

        self.fin_queue = Queue()
        self.data_queue = Queue()

    @classmethod
    def time_wait(cls):
        time.sleep(cls.sleeping)
        cls.sleeping *= 2
        cls.sleeping = int(cls.sleeping)
        if cls.sleeping >= 10420:
            cls.sleeping = 1

    def crawl_desc(self):
        while True:
            slp = random.randint(1, 10)
            time.sleep(slp*5)
            cur_data = self.data_queue.get()
            self.time_wait()
            url = cur_data.get('work_url')
            crawl_desc = JobDesc(url)
            detail = crawl_desc.run()
            data = dict(cur_data, **detail)

            self.fin_queue.put(data)
            self.data_queue.task_done()

    def parse_data(self):
        node_list = self.drive.find_elements_by_xpath('//*[@id="s_position_list"]/ul/li/div[@class="list_item_top"]')
        node_li_len = len(node_list)
        print("cur_page_len: "+str(node_li_len))

        for node in node_list:
            temp = {}

            company_node = node.find_element_by_xpath('.//div[@class="company_name"]/a')
            temp['company'] = company_node.text
            temp['com_url'] = company_node.get_attribute('href')
            # print(temp['company'])
            # print(temp['com_url'])

            work_node = node.find_element_by_xpath('.//a[@class="position_link"]')
            temp['work'] = work_node.find_element_by_xpath('./h3').text
            temp['work_place'] = work_node.find_element_by_xpath('./span').text
            temp['work_url'] = work_node.get_attribute('href')
            print("work: "+temp['work'])
            print("work_place: "+temp['work_place'])
            print("work_url: "+temp['work_url'])

            temp['salary'] = node.find_element_by_xpath('.//div[@class="li_b_l"]/span').text
            # print(temp['salary'])

            # self.crawl_desc(temp['work_url'])
            self.data_queue.put(temp)

        return node_li_len

    def __del__(self):
        self.drive.close()

    def go_to_url(self, ct, tm, wk):
        city = self.drive.find_element_by_link_text(ct)
        # ActionChains(self.drive).move_to_element(city).click(city).perform()
        city.click()

        exp = self.drive.find_element_by_xpath('//*[@id="filterCollapse"]/li[1]/a['+tm+']')
        exp.click()

        # work = self.drive.find_element_by_xpath('//*[@id="order"]/li/div[3]/div/ul/li[2]/a')
        # work.click()

        print("get: "+self.drive.current_url)

    def save_data(self):
        while True:
            data = self.fin_queue.get()
            print("save_file")
            with open('lagou_'+self.search+'.json', 'a')as f:
                res = json.dumps(data, ensure_ascii=False) + ',\n'
                f.write(res)
            self.fin_queue.task_done()

    def run(self):
        self.go_to_url('北京', WORK_EXP['3年及以下'], WORK['全职'])
        page_len = self.drive.find_element_by_xpath('//span[@page][last()]').text
        print(page_len)
        thread_list = []
        for i in range(int(page_len)):
            time.sleep(1)
            data_len = self.parse_data()
            for i in range(data_len):
                t = threading.Thread(target=self.crawl_desc)
                thread_list.append(t)

                t.setDaemon(True)
                t.start()

            self.data_queue.join()

            thread_save = threading.Thread(target=self.save_data)
            thread_save.setDaemon(True)
            thread_save.start()

            self.fin_queue.join()

            # self.save_data()
            cur_page = self.drive.find_element_by_class_name('pager_is_current').text
            print("cur_page: "+cur_page)
            next_node = self.drive.find_element_by_class_name('pager_next')
            # print(next_node.text)
            next_node.click()
            # time.sleep(2)
            # data_list = self.parse_data()

if __name__ == '__main__':
    lagou = LaGou('爬虫')
    lagou.run()

