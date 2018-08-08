import time
from selenium import webdriver
from selenium.common.exceptions import WebDriverException

def GetCookie():
    url = "http://www.cnvd.org.cn/flaw/list.htm"
    cookies = []
    try:
        print('open Chrome browser')
        chrome = webdriver.Chrome()
        print('visit cnvd website')
        chrome.get(url)
        timesleep = 8 #需要延时，来获取完整的cookies
        print('sleep {} seconds'.format(timesleep))
        time.sleep(timesleep) # important to get full cookies
    except WebDriverException as wde:
        print(wde)
        if chrome != None:
            chrome.quit()
    else:
        print('get cookies...')
        cookies = chrome.get_cookies()
        chrome.quit()

    if cookies == '' or type(cookies) != list  or cookies.__len__() == 0:
        print('cookie is not found')
    else:
        print('cookies: {}, size: {}'.format(cookies, cookies.__len__()))

GetCookie()