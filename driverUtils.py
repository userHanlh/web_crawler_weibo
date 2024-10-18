from selenium import webdriver
opt = webdriver.ChromeOptions()
# 添加防检测的参数
opt.add_argument('--disable-infobars')
opt.add_experimental_option("excludeSwitches", ["enable-automation"])
opt.add_experimental_option('useAutomationExtension', False)
driver = webdriver.Chrome(options = opt)
# 在每次打开页面之前，执行该脚本，去除selenium浏览器生成的相关属性
with open('hide.js') as f:
    driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {"source": f.read()})
