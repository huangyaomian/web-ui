# -*- coding: utf-8 -*-
# @File: login.py
# @Author: Mika
# @E-mail: yaomian@qoo-app.com
# @Time: 2020/10/22  16:21

import os
import sys

sys.path.append(os.pardir)

from public import Web

'''

page  对应 locatorYAML 操作页面
'''


class QooLogin(Web):

    def email_login(self, email: str, pwd: str):
        """
        郵箱登錄，正常流程
        :return:
        """
        self.my_send_keys("input_text", email)
        self.my_send_keys("input_pwd", pwd)
        self.my_click("protocol_checkbox")
        self.my_click("login_btn")

    def check_email_format_correct(self, email: str):
        """
        郵箱登錄，正常流程
        :return:
        """
        self.my_send_keys("input_text", email)

    def check_email_format_error(self, email: str, pwd: str):
        """
        郵箱登錄，正常流程
        :return:
        """
        self.my_send_keys("input_text", email)
        self.my_send_keys("input_pwd", pwd)
        self.my_click("protocol_checkbox")
        self.my_click("login_btn")

    def get_email_format_error_tip(self) -> bool:
        """
        郵箱登錄，正常流程
        :return:
        """
        return self.my_get_text("")

    def forget_pwd(self, email: str):
        """
        忘記密碼，正常流程
        :return:
        """
        self.my_click("forget_pwd_btn")
        self.sleep(3)
        el_list = self.my_find_elements('input_text')
        self.my_send_keys(el_list[0], email)
        self.my_click("get_code_btn")
        self.my_send_keys(el_list[1], '900677')
        self.my_click("next_step_btn")

    def fb_register(self, email: str):
        """
        fb註冊，正常走完流程
        :return:
        """
        pass

    def google_register(self, email: str):
        """
        google 註冊，正常走完流程
        :return:
        """
        pass

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
        self.web_exe(__file__, sys._getframe().f_code.co_name, )

    def click_discord_icon(self, ):
        """
        click_discord_icon
        :return:
        """

        self.web_exe(__file__, sys._getframe().f_code.co_name, )

    def input_discord_email(self, discord_email: str):
        """
        click_discord_icon
        :return:
        """
        self.web_exe(__file__, sys._getframe().f_code.co_name, text=discord_email, )

    def input_discord_pwd_and_submit(self, discord_pwd: str):
        """
        input_discord_pwd_and_submit
        :return:
        """
        self.web_exe(__file__, sys._getframe().f_code.co_name, text=discord_pwd, )

    def get_user_login_stats(self) -> bool:
        """
        通過右上角判斷用戶是否已登錄
        :return:
        """
        return self.web_exe(__file__, sys._getframe().f_code.co_name, )
