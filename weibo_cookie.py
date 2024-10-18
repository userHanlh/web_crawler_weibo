from selenium import webdriver
import json
import time
from driverUtils import driver
from selenium.webdriver.common.by import By

def get_cookie(url = 'https://passport.weibo.com/sso/signin?entry=miniblog&source=miniblog&disp=popup&url=https%3A%2F%2Fweibo.com%2Fnewlogin%3Ftabtype%3Dweibo%26gid%3D102803%26openLoginLayer%3D0%26url%3Dhttps%253A%252F%252Fweibo.com%252F'):
    url = url
    driver.get(url)
    print('使用微博APP扫码登录你的账号')
    time.sleep(25)
    # 定位账号输入框，输入账号
    # driver.find_element(By.XPATH, '//*[@placeholder="手机号"]').send_keys('17513160826')
    # driver.find_element(By.XPATH, '//*[@class="text-sm text-alink dark:text-alinkdark cursor-pointer"]').click()
    # yzm = input("请输入获得的验证码")
    # driver.find_element(By.XPATH, '//*[@placeholder="验证码"]').send_keys(yzm)
    # driver.find_element(By.XPATH, '//*[@type="button"]').click()

    # driver.find_element(By.XPATH, '//*[@class="md:hidden"]').click()
    # time.sleep(10)
    # driver.find_element(By.XPATH, '//*[@placeholder="手机号或邮箱"]').send_keys('17838609589')
    # time.sleep(10)
    # #定位密码输入框，输入密码
    # driver.find_element(By.XPATH, '//*[@placeholder="密码"]').send_keys('H689689')
    # # 点击登录
    # driver.find_element(By.XPATH, '//*[@type="button"]').click()

    with open('cookies.json', 'w') as f:
        f.write(json.dumps(driver.get_cookies()))
    print("已使用Cookie登录微博")
    print('已成功保存cookie信息。')
    driver.quit()
if __name__ == '__main__':
    get_cookie()
