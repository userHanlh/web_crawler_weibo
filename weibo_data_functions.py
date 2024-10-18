import random
from selenium.webdriver.common.by import By
import time
from datetime import datetime, timedelta
import re


# 时间处理函数
def process_time(time_str):
    # 获取当前时间
    now = datetime.now()

    try:
        # 处理“分钟前”
        if "分钟前" in time_str:
            minutes = int(re.search(r"\d+", time_str).group(0))  # 提取数字部分
            processed_time = now - timedelta(minutes = minutes)

        # 处理“秒前”
        elif "秒前" in time_str:
            seconds = int(re.search(r"\d+", time_str).group(0))  # 提取数字部分
            processed_time = now - timedelta(seconds = seconds)

        # 处理“今天08:40”
        elif "今天" in time_str:
            time_part = re.search(r"\d{2}:\d{2}", time_str).group(0)
            # 转换为datetime对象
            time_obj = datetime.strptime(time_part, "%H:%M")
            # 使用当前日期和提取的时间生成新的时间
            processed_time = now.replace(hour = time_obj.hour, minute = time_obj.minute, second = 0, microsecond = 0)

        # 处理形如“10月07日23:12”的时间
        elif re.match(r"\d+月\d+日\d{2}:\d{2}", time_str):
            processed_time = datetime.strptime(time_str, "%m月%d日%H:%M")
            processed_time = processed_time.replace(year = now.year)

        # 处理形如“2023年10月02日10:02”的时间
        elif re.match(r"\d+年\d+月\d+日\d{2}:\d{2}", time_str):
            processed_time = datetime.strptime(time_str, "%Y年%m月%d日%H:%M")

        # 如果没有匹配到预期的时间格式，则抛出异常
        else:
            raise ValueError("无法解析的时间格式")

        # 字符串格式化，最终转换为指定格式
        return processed_time.strftime("%Y年%m月%d日%H:%M")

    except Exception as e:
        return f"解析错误: {e}"


# 列表推导式去除空格换行符制表符
def string_strip(str):
    return ''.join([i for i in str if i not in [' ', '\n']])

# 微博内容处理
def strip_message(str):
    return ''.join(char for char in str if
                   char.isalnum() or char in ['#', '@', ' ', '！', '。', '，', '？'] or ('a' <= char <= 'z') or (
                               'A' <= char <= 'Z'))


def get_page_data(driver):
    weibo_data = []
    # 获取所有微博卡片
    weibo_posts = driver.find_elements(By.XPATH, '//*[@id="pl_feedlist_index"]/div/div[@action-type="feed_list_item"]')
    for post in weibo_posts:
        try:
            try:
                expand_button = post.find_element(By.XPATH, './/a[@action-type="fl_unfold"]')
                expand_button.click()  # 点击展开全文
                time.sleep(random.randint(1, 2))  # 等待内容展开
                # 需要展开和不需要展开的XPATH路径不一样
                content = post.find_element(By.XPATH, './/p[@class="txt"and @node-type="feed_list_content_full"]').text
                content = content.replace("收起d", "")
            except:
                # 获取微博内容
                content = post.find_element(By.XPATH, './/p[@class="txt"]').text
                pass  # 如果没有展开按钮，继续正常流程
            content = string_strip(content)
            content = strip_message(content)
            # 获取发布者昵称
            author = post.find_element(By.XPATH, './/a[@class="name"]').text
            #  获取发布时间
            time_posted = post.find_element(By.XPATH, './/div[@class="from"]/a[@target="_blank"]').text
            time_posted = string_strip(time_posted)
            time_posted = process_time(time_posted)
            # 获取点赞数量
            like_count = post.find_element(By.XPATH, './/span[@class="woo-like-count"]').text
            if "赞" in like_count:
                like_count = like_count.replace("赞", "0")
            like_count = int(like_count)

            weibo_data.append({
                "author": author,
                "content": content,
                "time": time_posted,
                "like_count": like_count
            })
        except Exception as e:
            print(f"遇到错误：{e}")
            continue
    return weibo_data


# 抓取多页微博内容的函数
def scrape_multiple_pages(num_pages, driver):
    all_weibo_data = []
    for i in range(num_pages):
        print(f"正在抓取第 {i + 1} 页微博内容...")
        page_data = get_page_data(driver)
        all_weibo_data.extend(page_data)
        # 查找并点击"下一页"按钮，跳转到下一页
        try:
            next_button = driver.find_element(By.XPATH, "//a[contains(text(), '下一页')]")
            next_button.click()
            time.sleep(random.randint(2, 3))  # 等待页面加载
        except:
            print("没有找到更多页面")
            break
    return all_weibo_data
