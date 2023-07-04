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


class QooSearch(Web):

    def search_game(self, content) -> str:
        """
        搜索遊戲
        :return:
        """
        return self.web_exe(__file__, sys._getframe().f_code.co_name, text=content)

