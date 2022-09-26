# -*- coding: utf-8 -*-
# created by: 吴佳霖 376030480@qq.com
# created time: 2022-09-26

# 新疆 内蒙古 辽宁 黑龙江数据不全
# 需安装selenium 和 Chrome driver.exe 百度查询安装方法
from selenium.webdriver import ActionChains
import numpy as np
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import time
from multiprocessing.dummy import Pool as ThreadPool


def get_table(province_name):
    # 定义常量和存放数据的矩阵
    province_name='上海'
    price_table = []
    var_name = ['调整时间(单位:元/升)', '调整类别', '89#汽油价格', '89#汽油涨幅', '92#汽油价格', '92#汽油涨幅',
                '95#汽油价格',
                '95#汽油涨幅', '0#柴油价格', '0#柴油涨幅']
    url = "http://data.eastmoney.com/cjsj/oil_city.aspx?city=%s" % province_name
    # 解析所有页面信息
    driver = webdriver.Chrome(options=chrome_options)
    driver.get(url)
    control = "下一页"
    while control != "上一页":
        # 解析页面并爬取表格信息
        source = driver.find_element(By.XPATH, '//*[@id="cjsj_table"]/table/tbody').find_elements(By.XPATH, '//td')
        for x in source:
            price_table.append(x.get_attribute('innerText').replace("↑", "").replace("↓", "-"))
        # 判断当前是否仍然需要翻页
        try:
            page = driver.find_element(By.XPATH, '//*[@id="cjsj_table_pager"]/div[1]/a[@class="active"]').get_attribute('data-page')
            print(province_name, page)
            control = driver.find_element(By.LINK_TEXT, '下一页')
            ActionChains(driver).move_to_element(control).click(control).perform()
            control = "下一页"
        except:
            control = "上一页"
            print("已经爬取完毕%s的油价调整信息" % province_name)
    # part4 整理数据为DataFrame格式
    price_table = np.array(price_table).reshape(-1, 10)
    price_table = pd.DataFrame(price_table, columns=var_name)
    price_table.to_csv("./data/%s.csv" % province_name, index=False, encoding="gbk")
    # 关闭浏览器
    driver.close()
    return None


def get_province_urls(base_url="http://data.eastmoney.com/cjsj/oil_city.aspx?city=%E5%8C%97%E4%BA%AC"):
    # part1 获取省份列表
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    driver.get(base_url)
    options = driver.find_element(By.ID, 'city-select').find_elements(By.XPATH, '//option')
    province_all = [x.get_attribute('innerText') for x in options]
    driver.close()
    # part2 爬取各省份油价数据
    for province in province_all:
        print(province)
        get_table(province)
    # part2 多线程进行网页爬虫
    # pool = ThreadPool(4)
    # pool.map(get_table, province_all)
    # pool.close()
    # pool.join()
    return None


if __name__ == "__main__":
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--headless')
    get_province_urls()
