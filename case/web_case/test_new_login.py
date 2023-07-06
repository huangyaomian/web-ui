# -*- coding: utf-8 -*-
# @File: test_demo.py
# @Author: Mika
# @E-mail: yaomian@qoo-app.com
# @Time: 2020/10/26  11:08

import allure
import pytest
from loguru import logger

from page.new_login_page import QooNewLogin
from public.reda_data import reda_pytest_data
from utils.str_util import my_find


@allure.story("行登录方式的登录验证")
class TestNewLogin:

    # @allure.feature("qoo mobile login")  # 测试用例特性（主要功能模块）

    @allure.title("郵箱登錄")  # 用例标题
    @allure.description('輸入用戶名和密碼')  # 用例描述
    @pytest.mark.test_new_login_web  # 用列标记
    @pytest.mark.parametrize('email,pwd', reda_pytest_data(__file__, 'test_qoo_email_login'))  # 测试数据
    @pytest.mark.run(order=1)
    def test_qoo_email_login(self, get_driver, email, pwd):
        logger.debug(email)
        qoo_login_page = QooNewLogin(get_driver)
        qoo_login_page.email_login(email=email, pwd=pwd)
        assert True

    @allure.title("驗證正確郵箱格式")  # 用例标题
    @allure.description('驗證正確郵箱格式')  # 用例描述
    @pytest.mark.test_new_login_web  # 用列标记
    @pytest.mark.parametrize('email', reda_pytest_data(__file__, 'test_check_email_format_correct'))  # 测试数据
    @pytest.mark.run(order=2)
    def test_check_email_format_correct(self, get_driver, email):
        qoo_login_page = QooNewLogin(get_driver)
        qoo_login_page.input_email(email=email)
        assert not qoo_login_page.is_email_format_error_tip()

    @allure.title("驗證錯誤郵箱格式")  # 用例标题
    @allure.description('驗證錯誤郵箱格式')  # 用例描述
    @pytest.mark.test_new_login_web  # 用列标记
    @pytest.mark.parametrize('email,tip', reda_pytest_data(__file__, 'test_check_email_format_error_case'))  # 测试数据
    @pytest.mark.run(order=3)
    def test_check_email_format_error_case(self, get_driver, email, tip):
        qoo_login_page = QooNewLogin(get_driver)
        qoo_login_page.input_email(email=email)
        assert my_find(qoo_login_page.get_email_format_error_tip(), tip)

    @allure.title("忘記密碼")  # 用例标题
    @allure.description('忘記密碼')  # 用例描述
    @pytest.mark.test_new_login_web  # 用列标记
    @pytest.mark.parametrize('email', reda_pytest_data(__file__, 'test_forget_pwd'))  # 测试数据
    @pytest.mark.run(order=21)
    def test_forget_pwd(self, get_driver, email):
        qoo_login_page = QooNewLogin(get_driver)
        qoo_login_page.forget_pwd(email=email)
        assert True
