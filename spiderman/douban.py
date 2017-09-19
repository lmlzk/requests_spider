import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys


class DouBan():
    def __init__(self):
        self.url = "https://www.douban.com/"
        self.driver = webdriver.PhantomJS()

    def log_in(self):
        print("start: ", self.url)
        self.driver.get(self.url)
        print("get")
        time.sleep(3)
        self.driver.save_screenshot("0.jpg")
        print("0.jpg")

        self.driver.find_element_by_xpath('//*[@id="form_email"]').send_keys("user")
        print("user")

        self.driver.find_element_by_xpath('//*[@id="form_password"]').send_keys("pswd")
        print("passwd")

        self.driver.find_element_by_class_name("bn-submit").click()
        print("click")
        time.sleep(5)
        self.driver.save_screenshot("douban.jpg")

        print(self.driver.get_cookies())

    def __del__(self):
        self.driver.quit()

if __name__ == "__main__":
    dou_ban = DouBan()
    dou_ban.log_in()