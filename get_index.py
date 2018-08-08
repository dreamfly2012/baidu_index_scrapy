#-*-coding:utf-8-*-
import sys
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from urllib import parse
import time
import urllib.request
import pickle
#driver=webdriver.PhantomJS(executable_path='E:\\phantomjs\\phantomjs.exe')

from PIL import Image
from PIL import ImageEnhance
import pytesseract
import pymysql
import myconfig

config = myconfig.config
commonconfig = myconfig.commonconfig
baiduconfig = myconfig.baiduconfig

def update_movie_index(index, sid, datetime, config):
    try:
        cnn = pymysql.connect(**config)
    except pymysql.Error as e:
        print('connect fails!{}'.format(e))
        exit()
    cursor = cnn.cursor()
    try:
        sql_query = "select id, sid, datetime from movie_baidu_index where sid = '%s' and datetime = '%s'"
        effect_row = cursor.execute(sql_query % (sid, datetime))
        if effect_row :
            print('yes')
            update_sql = "update movie_baidu_index set index = '%s' where id = '%s'";
            for id in cursor:
                data = (index, id)
                cursor.execute(update_sql % data)
                cnn.commit()
                print('成功更新', cursor.rowcount, '条数据')
        else:
            print('no')
            insert_sql = "insert into movie_baidu_index (sid, index, datetime) values('%s', '%s', '%s')"
            data = (sid, index, datetime)
            cursor.execute(insert_sql % data)
            cnn.commit()
            print('成功插入', cursor.rowcount, '条数据')
    except pymysql.Error as e:
        print('query error!{}'.format(e))
    finally:
        cursor.close()
        cnn.close()

def select_movie(config,baiduconfig):
    try:
        cnn = pymysql.connect(**config)
    except pymysql.Error as e:
        print('connect fails!{}'.format(e))
        exit()
    cursor = cnn.cursor()
    try:
        datetime = '2016'
        sql_query = "select * from yien where releasetime <> '' and publishdate = '%s' limit 10"
        effect_row = cursor.execute(sql_query % datetime)
        if effect_row :
            rows = cursor.fetchall()
            for row in rows:
                scrapy_baidu_index(baiduconfig['username'], baiduconfig['password'], row[2])
        else:
            print('none')
    except pymysql.Error as e:
        print('query error!{}'.format(e))
    finally:
        cursor.close()
        cnn.close()

####################################第零步:设置浏览器宽度#####################################
#print (driver.get_window_size())  
#driver.set_window_size(1280,800)  # 分辨率 1280*800  

###########二值化算法
def binarizing(img,threshold):
    pixdata = img.load()
    w, h = img.size
    for y in range(h):
        for x in range(w):
            if pixdata[x, y] < threshold:
                pixdata[x, y] = 0
            else:
                pixdata[x, y] = 255
    return img


####################################第一步:获取cookie#####################################

def scrapy_baidu_index(username, password, keyword):
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--disable-extensions')
    chrome_options.add_argument('--start-maximized')
    chrome_options.add_experimental_option('excludeSwitches', ['ignore-certificate-errors'])
    #chrome_options.binary_location = r'D:\chromedriver\chromedriver.exe'
    #chrome_options.binary_location = r'C:\Program Files (x86)\Google\Chrome\Application\chrome.exe'
    executable_path = r'D:\chromedriver\chromedriver.exe'
    base_url = "http://index.baidu.com/"
    driver = webdriver.Chrome(executable_path, chrome_options=chrome_options)

    info = parse.urlencode({'word':keyword})
    driver.get(base_url + '?tpl=trend&'+info)
    driver.get_screenshot_as_file(commonconfig['screen_shot'])
    print("截屏.................")
    e1 = driver.find_element_by_id("TANGRAM__PSP_4__userName")
    e1.send_keys(username)
    e2 = driver.find_element_by_id("TANGRAM__PSP_4__password")
    e2.send_keys(password)
    e3 = driver.find_element_by_id("TANGRAM__PSP_4__submit")
    e3.click()



    # 获取验证码URL地址
    imgsrc = driver.find_element_by_id("TANGRAM__PSP_4__verifyCodeImg").get_attribute('src')
    driver.get_screenshot_as_file(commonconfig['screen_shot'])
    # 定位验证码位置及大小
    # location = driver.find_element_by_id('TANGRAM__PSP_4__verifyCodeImg').location
    # size = driver.find_element_by_id('TANGRAM__PSP_4__verifyCodeImg').size
    # left = location['x']
    # top = location['y']
    # right = location['x'] + size['width']
    # bottom = location['y'] + size['height']
    urllib.request.urlretrieve(imgsrc, commonconfig['screen_code_shot'])


    # 从文件读取截图，截取验证码位置再次保存
    img = Image.open(commonconfig['screen_code_shot'])
    img = img.convert('L')  # 转换模式：L | RGB
    img = ImageEnhance.Contrast(img)  # 增强对比度
    img = img.enhance(2.0)  # 增加饱和度
    img.save(commonconfig['screen_code_shot'])

    #去除干扰线
    data = img.getdata()
    w, h = img.size
    # im.show()
    black_point = 0
    for x in range(1, w - 1):
        for y in range(1, h - 1):
            mid_pixel = data[w * y + x]  # 中央像素点像素值
            if mid_pixel == 0:  # 找出上下左右四个方向像素点像素值
                top_pixel = data[w * (y - 1) + x]
                left_pixel = data[w * y + (x - 1)]
                down_pixel = data[w * (y + 1) + x]
                right_pixel = data[w * y + (x + 1)]

                # 判断上下左右的黑色像素点总个数
                if top_pixel == 0:
                    black_point += 1
                if left_pixel == 0:
                    black_point += 1
                if down_pixel == 0:
                    black_point += 1
                if right_pixel == 0:
                    black_point += 1
                if black_point >= 3:
                    img.putpixel((x, y), 0)
                # print black_point
                black_point = 0
    img.show()
    img.save(commonconfig['screen_code_shot'])

    # 再次读取识别验证码
    img = Image.open(commonconfig['screen_code_shot'])
    code = pytesseract.image_to_string(img, lang='chi_sim')
    print(code)
    # code= pytesser.image_file_to_string(screenImg)
    driver.find_element_by_id("TANGRAM__PSP_3__verifyCode").send_keys(code.strip())
    print(code.strip())

    e3.click()
    cookies = driver.get_cookies()
    print(cookies);
    #cookies = pickle.load(open("cookies.pkl", "rb"))
    for cookie in cookies:
        driver.add_cookie(cookie)

    time.sleep(6)

    driver.get("http://index.baidu.com/?tpl=trend&"+info)
    time.sleep(3)

    driver.get_screenshot_as_file(commonconfig['screen_code_shot'])
    print("截屏结束.................")
    driver.quit()


    img1=Image.open(commonconfig['screen_shot'])
    w,h=img1.size
    # region = (220*3,320*3,420*3,380*3)//两个一起
    ##将图片放大3倍
    out=img1.resize((w*3,h*3),Image.ANTIALIAS)
    region1 = (220*3,320*3,320*3,380*3)
    region2 = (320*3,320*3,420*3,380*3)
    cropImg1 = out.crop(region1)
    cropImg2 = out.crop(region2)
    img1= cropImg1.convert('L')
    img2= cropImg2.convert('L')
    img1=binarizing(img1,200)
    img2=binarizing(img2,200)
    code1 = pytesseract.image_to_string(img1)
    code2 = pytesseract.image_to_string(img2)

    print ("整体搜索指数:" + str(code1).replace(".","").replace(" ",''))
    print ("移动搜索指数:" + str(code2).replace(".","").replace(" ",''))

select_movie(config, baiduconfig)