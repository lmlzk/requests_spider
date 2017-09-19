from selenium import webdriver
import json
import time


class DouYu(object):
    def __init__(self):
        self.driver = webdriver.Chrome()
        self.url = 'https://www.douyu.com/directory/all'
        self.driver.get(self.url)

    def parse_data(self):
        node_list = self.driver.find_elements_by_xpath('//*[@id="live-list-contentbox"]/li/a')
        print(len(node_list))

        data_list = []
        for node in node_list:
            temp = {}
            temp['title'] = node.find_element_by_xpath('./div/div/h3').text
            temp['category'] = node.find_element_by_xpath('./div/div/span').text
            temp['owner'] = node.find_element_by_xpath('./div/p/span[1]').text
            temp['num'] = node.find_element_by_xpath('./div/p/span[2]').text
            temp['cover'] = node.find_element_by_xpath('./span/img').get_attribute('data-original')
            data_list.append(temp)
        return data_list

    def save_data(self, data_list):
        with open('douyu.json', 'a')as f:
            for data in data_list:
                result = json.dumps(data, ensure_ascii=False) + ',\n'
                f.write(result)
            print('save')

    def __del__(self):
        self.driver.close()

    def run(self):
        while True:
            time.sleep(3)
            data_list = self.parse_data()
            self.save_data(data_list)
            try:
                el_next = self.driver.find_element_by_xpath('//a[@class="shark-pager-next"]')
                el_next.click()
            except:
                break

if __name__ == '__main__':
    dou_yu = DouYu()
    dou_yu.run()