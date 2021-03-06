import random
import time
from lxml import etree
import requests


class JobDesc(object):
    def __init__(self, url):
        self.url = url
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) \
            AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36"
        }
        # self.proxies = {
        #     "http": "http://125.67.74.93:9000",
        #     "https": "https://125.67.74.93:9000"
        # }

    def get_page(self):
        print("start: "+self.url)
        try:
            time.sleep(3)
            # response = requests.get(self.url, headers=self.headers, proxies=self.proxies)
            response = requests.get(self.url, headers=self.headers)
            print("get: "+self.url)
            return response.content.decode()
        except:
            print("unconnected")
            return None

    def parse_data(self, str_data):
        print("para_data_start-------------")
        html = etree.HTML(str_data)

        data_dic = {}

        adv_node = html.xpath('//*[@id="job_detail"]/dd[1]//text()')
        adv = adv_node[0].strip() if len(adv_node) > 0 else None
        print(adv)
        data_dic['adv'] = adv

        con_list = html.xpath('//*[@id="job_detail"]/dd[2]//div')
        # '//*[@id="job_detail"]/dd[2]/div/p'
        con_len = len(con_list)
        # print(con_len)
        con_str = ''
        if con_len == 1:
            conx = con_list[0].xpath('.//text()')
            # con_str = conx[0].strip()
            con_str = (''.join(conx)).strip()
        else:
            for con in con_list:
                conx = con.xpath('.//text()')
                # print(conx)
                con_str += conx[0].strip() if conx else ''
        print(con_str)
        print("para_data_end-------------")

        data_dic['job_info'] = con_str.strip()

        return data_dic

    def save_data(self, data_list):
        pass

    def run(self):
        str_data = self.get_page()
        data_dic = self.parse_data(str_data)
        self.save_data(list(data_dic))
        return data_dic

if __name__ == '__main__':
    url = 'https://www.lagou.com/jobs/3589378.html'
    crawl_desc = JobDesc(url)
    crawl_desc.run()
