"""
Name : test_wework_login.py
Author  : Tiffany
Time : 2022/7/31 15:55
DESC: 
"""
import time

import yaml
from selenium import webdriver


class TestWeworkLogin:
    def setup_class(self):
        self.driver = webdriver.Chrome()

    def teardown_class(self):
        # self.driver.quit()
        pass

    def test_save_cookies(self):
        # 1.访问登录页面
        self.driver.get("https://work.weixin.qq.com/wework_admin/loginpage_wx?from=myhome")
        # 2.人工扫码（直接等待）
        time.sleep(15)
        # 3.获取浏览器cookies记录
        cookies = self.driver.get_cookies()
        print(cookies)
        # 4.保存cookies到文件中
        with open("../data/cookies.yaml", "w") as f:
            yaml.safe_dump(cookies, f)

    def test_get_cookie(self):
        # 1.访问企业微信登录页面
        self.driver.get("https://work.weixin.qq.com/wework_admin/loginpage_wx?from=myhome")
        # 2.获取本地的cookie记录
        cookie = yaml.safe_load(open("../data/cookies.yaml"))
        # 3.植入cookie
        for c in cookie:
            self.driver.add_cookie(c)
        time.sleep(3)
        # 4.重新访问企业微信首页
        self.driver.get("https://work.weixin.qq.com/wework_admin/loginpage_wx?from=myhome")



