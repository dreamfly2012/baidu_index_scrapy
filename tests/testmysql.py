# -*- coding=utf-8 -*-
import sys
import pymysql
sys.path.append('..')
import myconfig
config = myconfig.config

try:
    cnn = pymysql.connect(**config)
except pymysql.Error as e:
    print('connect fails!{}'.format(e))
cursor = cnn.cursor()
try:
    sql_query = 'select username,nickname from user ;'
    cursor.execute(sql_query)
    for username, nickname in cursor:
        print (username, nickname)
except pymysql.Error as e:
    print('query error!{}'.format(e))
finally:
    cursor.close()
    cnn.close()