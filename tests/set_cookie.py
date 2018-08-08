#-*-coding:utf-8-*-
import sys
from selenium import webdriver
import time
import pickle
sys.path.append('..')
import myconfig
driver=webdriver.PhantomJS(executable_path='E:\\phantomjs\\phantomjs.exe')
baiduconfig = myconfig.baiduconfig

driver.get('http://index.baidu.com/?tpl=trend&word=%D0%DB%B0%B2%D0%C2%C7%F8')
e1 = driver.find_element_by_id("TANGRAM__PSP_4__userName")
e1.send_keys(baiduconfig['username'])
e2 = driver.find_element_by_id("TANGRAM__PSP_4__password")
e2.send_keys(baiduconfig['password'])
e3 = driver.find_element_by_id("TANGRAM__PSP_4__submit")
e3.click()
cookies = driver.get_cookies()
print(cookies);
time.sleep(6)

pickle.dump(cookies, open("cookies.pkl","wb"))