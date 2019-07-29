# -*- coding: utf-8 -*-
# created by: 吴佳霖 376030480@qq.com
# created time: 2019-7-29

# 新疆 内蒙古 辽宁 黑龙江数据不全
# 需安装selenium 和 Chrome driver.exe 百度查询安装方法
from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver import ActionChains
import numpy as np
import pandas as pd
from multiprocessing.dummy import Pool as ThreadPool


def get_table(province_name):
    # 定义常量和存放数据的矩阵
    price_table = []
    var_name = ['调整时间(单位:元/升)', '调整类别', '89#汽油价格', '89#汽油涨幅', '92#汽油价格', '92#汽油涨幅', '95#汽油价格',
                '95#汽油涨幅', '0#柴油价格', '0#柴油涨幅']
    url = "http://data.eastmoney.com/cjsj/oil_city.aspx?city=%s" % province_name

    # 解析所有页面信息
    driver = webdriver.Chrome(options=chrome_options)
    driver.get(url)
    control = "上一页"
    while control != "下一页":
        # 解析页面并爬取表格信息
        html = driver.page_source
        soup = BeautifulSoup(html, 'html.parser')
        for x in soup.find("div", {'class': "content"}).find_all('td'):
            price_table.append(x.get_text().replace("↑", "").replace("↓", "-"))
        # 判断当前是否仍然需要翻页
        try:
            control = soup.find("a", {'class': "nolink"}).get_text()
        except AttributeError:
            control = "上一页"
        # 浏览器模拟 翻页操作
        if control == "下一页":
            print("已经爬取完毕%s的油价调整信息" % province_name)
        else:
            try:
                continue_link = driver.find_element_by_link_text('下一页')
                ActionChains(driver).move_to_element(continue_link).click(continue_link).perform()
            except:
                break

    # part4 整理数据为DataFrame格式
    price_table = np.array(price_table).reshape(-1, 10)
    price_table = pd.DataFrame(price_table, columns=var_name)
    price_table.to_csv("./data/%s.csv" % province_name, index=False, encoding="gbk")
    # 关闭浏览器
    driver.close()
    return None


def get_province_urls(base_url="http://data.eastmoney.com/cjsj/oil_city.aspx?city=%E5%8C%97%E4%BA%AC"):
    
    # part1 获取省份列表
    driver = webdriver.Chrome(options=chrome_options)
    driver.get(base_url)
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')
    options = soup.find_all('option')
    province_all = [x.get_text() for x in options]
    driver.close()
    
    # part2 多线程进行网页爬虫
    pool = ThreadPool(4)
    pool.map(get_table, province_all)
    pool.close()
    pool.join()
    return None


if __name__ == "__main__":
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--headless')
    get_province_urls()
