"""
Name : test_addmember.py
Author  : Tiffany
Time : 2022/8/1 19:02
DESC: 
"""
import time

import yaml
from faker import Faker
from selenium import webdriver
from selenium.common import StaleElementReferenceException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait


class TestAddMemberFromeContact:
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
        pass

    def test_addmember(self):
        """通讯录页面：添加成员"""
        # 点击通讯录按钮
        self.driver.find_element(By.ID, "menu_contacts").click()
        # 点击添加成员按钮
        time.sleep(5)
        attempts = 0
        while attempts < 3:
            try:
                self.driver.find_element\
                    (By.XPATH, '//*[@id="js_contacts82"]/div/div[2]/div/div[2]/div[3]/div[1]/a[1]').click()
                time.sleep(5)
                self.driver.find_element(By.ID, "username").send_keys(self.username)
                self.driver.find_element(By.ID, "memberAdd_acctid").send_keys(self.acctid)
                self.driver.find_element(By.ID, "memberAdd_phone").send_keys(self.mobile)
                self.driver.find_elements(By.CLASS_NAME, "js_btn_save")[0].click()
                break
            except StaleElementReferenceException:
                attempts += 1
        # 输入姓名、账号、手机

        # 点击保存按钮
        # 4.断言结果
        loc_tips = (By.ID, "js_tips")
        WebDriverWait(self.driver, 10, 2).until(expected_conditions.visibility_of_element_located(loc_tips))
        tips_value = self.driver.find_element(*loc_tips).text
        assert tips_value == "保存成功"

    def test_dept_contact(self):
        """通讯录页面：添加部门"""
        # 点击通讯录菜单
        self.driver.find_element(By.ID, "menu_contacts").click()
        # 点击加号
        self.driver.find_element(By.XPATH, "//i[@class='member_colLeft_top_addBtn']").click()
        # 点击添加部门
        self.driver.find_element(By.XPATH, "//a[text()='添加部门']").click()
        # 填写部门名称
        self.driver.find_element(By.XPATH, "//input[@name='name']").send_keys(self.username)
        # 选择所属部门
        self.driver.find_element(By.XPATH, "//span[@class='js_parent_party_name']").click()
        self.driver.find_element(By.XPATH, "//div[@class='inputDlg_item']//a[text()='加加加']").click()
        # 点击确定按钮
        self.driver.find_element(By.XPATH, "//a[text()='确定']").click()
        # 断言结果
        loc_tips = (By.ID, "js_tips")
        WebDriverWait(self.driver, 10, 2).until(expected_conditions.visibility_of_element_located(loc_tips))
        tips_value = self.driver.find_element(*loc_tips).text
        assert tips_value == "新建部门成功"
        pass

