# -*- coding: utf-8 -*-
# @File: test_demo.py
# @Author: Mika
# @E-mail: yaomian@qoo-app.com
# @Time: 2020/10/26  11:08

import allure
import pytest

from pageobj.qoo_search import QooSearch
from public.common import ImgDiff, logger
from public.reda_data import reda_pytestdata


# 修改 setting  URL
class TestQooSearch:

    @allure.feature("qoo搜索")  # 测试用例特性（主要功能模块）
    @allure.story("所搜验证")  # 模块说明
    @allure.title("输入内容并搜索")  # 用例标题
    @allure.description('输入多参数搜索')  # 用例描述
    @pytest.mark.test_qoo_search_web  # 用列标记
    @pytest.mark.parametrize('content', reda_pytestdata(__file__, 'test_qoo_search'))  # 测试数据
    def test_qoo_search(self, get_driver, content):
        qoo_search_page = QooSearch(get_driver)

        with allure.step('點擊游戲庫'):
            qoo_search_page.click_app_store_button()

        with allure.step('输入搜索内容'):
            qoo_search_page.input_search_content(content)

        with allure.step('点击搜索'):
            qoo_search_page.click_search_button()
            qoo_search_page.sleep(3)
            # 对比查询后图片结果
            search_result = qoo_search_page.screen_shot('search')
            df = ImgDiff.ahaDiff('python.png', search_result)
            assert df < 50
