#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by master on 2017/4/7
import os
import requests
from bs4 import BeautifulSoup
import sqlite3

from Kuaidaili.FreeDaili import Daili


class KuaiDaili(object):
    def get_html(self, page):
        header = {  # 添加header可以将程序伪装成浏览器
            "Host": "www.kuaidaili.com",
            'Connection': 'keep-alive',
            'Cache-Control': 'max-age=0',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.87 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate, sdch',
            'Accept-Language': 'zh-CN,zh;q=0.8',
        }
        TARGET_URL = ("http://www.kuaidaili.com/free/inha/%s" % page)  # 目标地址
        html = requests.get(url=TARGET_URL, headers=header, timeout=30).content  # 获取html文本
        return html.decode("utf-8")

    def create_table(self):
        conn = sqlite3.connect('ip.db')
        cursor = conn.cursor()
        cursor.execute(
            '''CREATE TABLE ip (id INTEGER PRIMARY KEY ,
                ip VARCHAR(20) ,
                port BOOLEAN ,
                anonymous VARCHAR(20) ,
                types VARCHAR(20) ,
                location VARCHAR(20) ,
                speed VARCHAR(20) ,
                verify_time VARCHAR(20))
            ''')
        conn.commit()

    def insert_ip(self, daili):
        if not os.path.exists('ip.db'):
            self.create_table()  # 创建数据库
        conn = sqlite3.connect('ip.db')
        cursor = conn.cursor()
        sql = "INSERT INTO ip(ip,port,anonymous,types,location,speed,verify_time) VALUES (" + str(
            '\'' + daili.ip + '\',\'' + daili.port + '\',\'' + daili.anonymous + '\',\'' + daili.types + '\',\'' + daili.location + '\',\'' + daili.speed + '\',\'' + daili.verify_time) + '\')'

        daili.__str__()
        cursor.execute(sql)
        conn.commit()

    def ip_list(self, html):
        soup = BeautifulSoup(html, 'lxml')  # 创建一个BeautifulSoup，使用更强的lxml解析器，
                                            # 需要提前安装
        list_tr = soup.find('div', id='list').find_all('tr')  # 提取id为list的div标签中的所有tr标签
        for i in range(len(list_tr)):  # 遍历tr标签的列表
            if i == 0: continue  # 因为从上图中我们可以看到第一个tr标签里面的内容是表头，
                                # 不是我们需要的数据，所以我们跳过第一个tr标签，从第二个tr标签开始遍历
            tr = list_tr[i]
            list_td = tr.find_all('td')# 获取每个tr标签中的所有td标签，分析html可知td标签从上到下
                                        # 依次是ip,端口，匿名度等信息...

            ip = list_td[0].get_text()
            port = list_td[1].get_text()
            anonymous = list_td[2].get_text()
            types = list_td[3].get_text()
            location = list_td[4].get_text()
            speed = list_td[5].get_text()
            verify_time = list_td[6].get_text()
            # 创建代理对象，把每个代理信息都保存到对象中，这一步也可以跳过
            daili = Daili(ip, port, anonymous, types, location, speed, verify_time)


            self.insert_ip(daili)# 插入数据

    def batch_insert(self, page=10):# 批量插入
        for i in range(1, page):
            resp = self.get_html(i)
            self.ip_list(resp)

    def query(self):# 查询数据
        conn = sqlite3.connect('ip.db')
        cursor = conn.cursor()
        # sql = 'select ip,port from ip where location like "中国 江苏省 镇江市%";'
        # sql = 'select * from ip where port="80";'
        sql = 'select * from ip;'
        rows = cursor.execute(sql)

        for row in rows:
            print(str(row[0]) + ":" + str(row[1]))
        print('rows length:%s', len(rows))
        conn.commit()
        conn.close()


if __name__ == '__main__':
    daili = KuaiDaili()
    daili.batch_insert()
