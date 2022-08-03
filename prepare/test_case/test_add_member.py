"""
Name : test_add_member.py
Author  : Tiffany
Time : 2022/7/31 19:38
DESC: 
"""
import time

import yaml
from faker import Faker
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait

from prepare.utils.log_utils import logger


class TestAddMemberFromHome:
    def setup_class(self):
        fake = Faker("zh_CN")
        self.username = fake.name()
        self.acctid = fake.ssn()
        self.mobile = fake.phone_number()
        # 实例化
        self.driver = webdriver.Chrome()
        self.driver.implicitly_wait(5)
        self.driver.maximize_window()
        # 一.登录
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

    def teardown_class(self):
        # self.driver.quit()
        pass

    def test_add_member(self):

        # 2.点击添加成员按钮
        self.driver.find_element(By.XPATH, '//*[text()="添加成员"]').click()
        # 3.填写成员信息
        # 3.1 输入用户名、输入acctid、输入手机号、点击保存按钮
        self.driver.find_element(By.ID, "username").send_keys(self.username)
        logger.info(self.username)
        self.driver.find_element(By.ID, "memberAdd_acctid").send_keys(self.acctid)
        self.driver.find_element(By.ID, "memberAdd_phone").send_keys(self.mobile)
        self.driver.find_elements(By.CLASS_NAME, "js_btn_save")[0].click()
        # 4.断言结果
        loc_tips = (By.ID, "js_tips")
        WebDriverWait(self.driver, 10, 2).until(expected_conditions.visibility_of_element_located(loc_tips))
        tips_value = self.driver.find_element(*loc_tips).text
        assert tips_value == "保存成功"

        pass
