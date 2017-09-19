import time
from selenium import webdriver

driver = webdriver.PhantomJS()

driver.get('https://qzone.qq.com/')

el_frame = driver.find_element_by_xpath('//*[@id="login_frame"]')
driver.switch_to_frame(el_frame)

el = driver.find_element_by_xpath('//*[@id="switcher_plogin"]')
print(el.text)

el.click()

el_user = driver.find_element_by_xpath('//*[@id="u"]')
el_pwd = driver.find_element_by_xpath('//*[@id="p"]')
el_user.send_keys('user')
el_pwd.send_keys('pswd')

el_su = driver.find_element_by_xpath('//*[@id="login_button"]')
el_su.click()

time.sleep(2)
driver.save_screenshot("qzone.jpg")

