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

    def email_login(self, email):
        """
        郵箱登錄
        :return:
        """

        self.web_exe(__file__, sys._getframe().f_code.co_name, text=email)

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
