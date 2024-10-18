import random
from selenium import webdriver
from selenium.webdriver.common.by import By
import json
import time
from driverUtils import driver
from weibo_data_functions import scrape_multiple_pages
from database_connection_utils import conn
# 打开微博首页
driver.get("https://s.weibo.com/")
time.sleep(random.randint(1, 2))  # 等待页面加载
# 加载保存的cookie
with open("cookies.json", "r") as file:
    cookies = json.load(file)
# 添加cookie到浏览器
for cookie in cookies:
    driver.add_cookie(cookie)
# 刷新页面，模拟已登录状态
driver.refresh()
time.sleep(random.randint(1, 2))  # 等待页面刷新和微博数据加载
#  获取微博输入框区域
search_input = driver.find_element(By.XPATH, '//div[@class="search-input"]/input[@type="text"]')
topic = input("请输入你想查询的微博话题\n")
search_input.send_keys(topic)
search_input.send_keys(u'\ue007')  # 模拟按下Enter键
num_pages = int(input("输入待查询的页数\n"))
data_list=scrape_multiple_pages(num_pages, driver)
# 执行非查询性质SQL
cursor = conn.cursor()      # 获取到游标对象
# 选择数据库
conn.select_db("weibo_data")
for data in data_list:
    print(f"({data["author"]}, {data["time"]},{data["content"]},{data["like_count"]})")
    # 执行sql
    # 插入数据时使用参数化查询
    sql = "INSERT INTO weibo (topic,author, time, content, like_count) VALUES (%s, %s, %s, %s, %s)"
    cursor.execute(sql, (topic, data["author"], data["time"], data["content"], data["like_count"]))
print("数据库更新完成")
# 关闭链接
conn.close()
driver.quit()






