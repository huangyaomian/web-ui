# -*- coding: utf-8 -*-
# @File: test_demo.py
# @Author: Mika
# @E-mail: yaomian@qoo-app.com
# @Time: 2020/10/26  11:08

import allure
import pytest

from page.qoo_search import QooSearch
from public.reda_data import reda_pytestdata


# 修改 setting  URL
class TestQooSearch:

    @allure.feature("qoo搜索")  # 测试用例特性（主要功能模块）
    @allure.story("搜索验证")  # 模块说明
    @allure.title("输入内容并搜索")  # 用例标题
    @allure.description('输入多参数搜索')  # 用例描述
    @pytest.mark.test_qoo_search_web  # 用列标记
    @pytest.mark.parametrize('content', reda_pytestdata(__file__, 'test_qoo_search'))  # 测试数据
    def test_qoo_search(self, get_driver, content):
        text = QooSearch(get_driver).search_game(content)
        assert content.__eq__(text)

    # search_result = qoo_search_page.screen_shot('search')
    # df = ImgDiff.ahaDiff('python.png', search_result)
    # assert df < 50
