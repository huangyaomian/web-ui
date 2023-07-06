# -*- coding: utf-8 -*-
# @File: login.py
# @Author: Mika
# @E-mail: yaomian@qoo-app.com
# @Time: 2020/10/22  16:21

import os
import sys

from utils.yaml_util import get_element_by

sys.path.append(os.pardir)

from public import Web

'''

page  对应 locatorYAML 操作页面
'''


class QooNewLogin(Web):

    def email_login(self, email: str, pwd: str):
        """
        郵箱登錄，正常流程
        :return:
        """
        self.input_email(email)
        self.my_send_keys("input_pwd", pwd)
        self.my_click("protocol_checkbox")
        self.my_click("login_btn")

    def input_email(self, email: str):
        """
        郵箱登錄，正常流程
        :return:
        """
        self.my_send_keys("input_text", email)

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

    def forget_pwd(self, email: str):
        """
        忘記密碼，正常流程
        :return:
        """
        self.my_click("forget_pwd_btn")
        self.sleep(1)
        el_list = self.my_find_elements('input_text')
        self.my_send_keys(el_list[0], email)
        self.my_click("get_code_btn")
        self.my_send_keys(el_list[1], '900677')
        self.my_click("next_step_btn")

    def goto_register_page(self):
        """
        跳转注册的弹窗
        """
        self.my_click("fb_register_icon")

    def fb_register(self, email: str):
        """
        fb註冊，正常走完流程
        :return:
        """
        self.goto_register_page()
        self.my_click("fb_register_icon")

    def google_register(self, email: str):
        """
        google 註冊，正常走完流程
        :return:
        """
        self.goto_register_page()
        self.my_click("google_register_icon")

    def fb_login_for_not_register(self, email: str):
        """
        fb 登錄，未註冊的賬號進行登錄
        :return:
        """
        pass

    def google_login_for_not_register(self, email: str):
        """
        google 登錄，未註冊的賬號進行登錄
        :return:
        """
        pass

    def click_login_button(self, ):
        """
        點擊登入按鈕
        :return:
        """
        pass

    def get_user_login_stats(self) -> bool:
        """
        通過右上角判斷用戶是否已登錄
        :return:
        """
        pass
