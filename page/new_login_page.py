# -*- coding: utf-8 -*-
# @File: login.py
# @Author: Mika
# @E-mail: yaomian@qoo-app.com
# @Time: 2020/10/22  16:21

import os
import sys

from public.reda_data import RandomData
from utils.str_util import my_find
from utils.yaml_util import get_element_by

sys.path.append(os.pardir)

from public import Web

'''

page  对应 locatorYAML 操作页面
'''


class QooNewLogin(Web):

    def click_back_btn(self):
        """
        點擊返回按鈕
        :return:
        """
        self.my_click("back_btn")

    def click_login_test_btn(self):
        """
        打開登錄彈窗
        :return:
        """
        self.my_click("login_test_btn")

    def email_login(self, email: str, pwd: str):
        """
        郵箱登錄，正常流程
        :return:
        """
        self.input_email(email)
        self.my_send_keys("input_pwd", pwd)
        self.click_protocol_checkbox()
        self.click_login_btn()

    def click_login_btn(self):
        """
        點擊登錄按鈕
        :return:
        """
        self.my_click("login_btn")

    def input_email(self, email: str):
        """
        郵箱登錄，正常流程
        :return:
        """
        self.my_send_keys("input_text", email)

    def click_protocol_checkbox(self):
        """
        勾選同意協議
        :return:
        """
        self.my_click("protocol_checkbox")

    def click_terms_btn(self):
        """
        點擊使用條款
        :return:
        """
        self.my_click("terms_btn")

    def click_privacy_btn(self):
        """
        點擊隱私協議
        :return:
        """
        self.my_click("privacy_btn")

    def is_email_format_error_tip(self) -> None or str:
        """
        判斷錯誤提示是否存在
        :return:
        """
        return self.is_visibility_of_element_located("email_error_tip", 3)

    def get_email_format_error_tip(self) -> None or str:
        """
        獲取提示信息
        :return:
        """
        return self.my_get_text("email_error_tip")

    def forget_pwd(self, email: str, pwd: str):
        """
        忘記密碼，正常流程
        :return:
        """
        self.forget_pwd_get_code(email)
        self.my_send_keys('forget_pwd_code_input', '900677')
        self.my_click("next_step_btn")
        el_list = self.my_find_elements('reset_pwd_input')
        self.my_send_keys(el_list[0], pwd)
        self.my_send_keys(el_list[1], pwd)
        self.my_click("reset_pwd_confirm")

    def forget_pwd_get_code(self, email: str):
        """
        忘記密碼，正常流程
        :return:
        """
        self.click_forget_pwd_btn()
        self.input_forget_pwd_email(email)
        self.click_forget_pwd_get_code()

    def click_forget_pwd_btn(self):
        """
        跳轉忘記密碼頁面
        :return:
        """
        self.my_click("forget_pwd_btn")

    def input_forget_pwd_email(self, email: str):
        """
        忘記密碼輸入郵箱
        :return:
        """
        self.my_send_keys("forget_pwd_email_input", email)

    def is_visibility_many_code_tip(self) -> bool:
        """
        忘記密碼輸入郵箱
        :return:
        """
        return self.is_visibility_of_element_located("many_code_tip") and self.my_is_enabled('get_code_btn')

    def click_forget_pwd_get_code(self):
        """
        忘記密碼。點擊發送驗證碼
        :return:
        """
        self.my_click("get_code_btn")

    def goto_register_page(self):
        """
        跳转注册的弹窗
        """
        self.my_click("fb_register_icon")

    def fb_register(self):
        """
        fb註冊，正常走完流程
        :return:
        """
        self.goto_register_page()
        self.my_click("fb_register_icon")

    def google_register(self):
        """
        google 註冊，正常走完流程
        :return:
        """
        self.goto_register_page()
        self.my_click("google_register_icon")

    def login_need_allow_protocol(self, tip: str) -> bool:
        """
        google 註冊，正常走完流程
        :return:
        """
        self.click_fb_login_btn()
        return my_find(main_str=self.my_get_text('allow_protocol_tip'), sub_str=tip)

    def fb_login_for_not_register(self, email: str):
        """
        fb 登錄，未註冊的賬號進行登錄
        :return:
        """
        self.click_protocol_checkbox()
        self.click_fb_login_btn()
        self.my_send_keys('fb_email_input', 'xiaoxiu0710@aliyun.com')
        self.my_send_keys('fb_pwd_input', 'xiaoxiu123')
        self.my_click('fb_login_btn')

    def click_fb_login_btn(self):
        """
        fb 登錄，未註冊的賬號進行登錄
        :return:
        """
        self.my_click('fb_login_icon')

    def google_login_for_not_register(self, email: str):
        """
        google 登錄，未註冊的賬號進行登錄
        :return:
        """
        # self.click_protocol_checkbox()
        # self.click_google_login_btn()
        self.my_send_keys('gp_email_input', 'mika930728@gmail.com')
        self.my_click('gp_next')
        self.my_click('fb_login_btn')


    def click_google_login_btn(self):
        """
        點擊gp登入按鈕
        :return:
        """
        self.my_click('google_login_icon')

    def get_user_login_stats(self) -> bool:
        """
        通過右上角判斷用戶是否已登錄
        :return:
        """
        return self.is_visibility_of_element_located("login_test_name")

    def is_captcha_slider(self) -> bool:
        """
        滑動驗證碼是否已彈出
        :return:
        """
        return self.is_visibility_of_element_located("captcha_slider")
