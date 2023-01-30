# -*- coding: utf-8 -*-
# @File: android.py.py
# @Author: Mika
# @E-mail: yaomian@qoo-app.com
# @Time: 2021/6/22  12:57

import os
import sys

sys.path.append(os.pardir)

from public import App




class OpenWeChatPage(App):

    def click_login_button(self, ):
        self.appexe(__file__, sys._getframe().f_code.co_name )
