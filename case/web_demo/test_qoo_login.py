# -*- coding: utf-8 -*-
# @File: test_demo.py
# @Author: Mika
# @E-mail: yaomian@qoo-app.com
# @Time: 2020/10/26  11:08
import logging
import sys

import allure
import pytest
from loguru import logger

from page.qoo_login import QooLogin
from public.common import ImgDiff
from public.reda_data import reda_pytest_data


# 修改 setting  URL
class TestQooLogin:

    @allure.feature("qoo mobile login")  # 测试用例特性（主要功能模块）
    @allure.story("登錄驗證")  # 模块说明
    @allure.title("郵箱登錄")  # 用例标题
    @allure.description('輸入用戶名和密碼')  # 用例描述
    @pytest.mark.test_qoo_login_web  # 用列标记
    @pytest.mark.parametrize('email,pwd', [reda_pytest_data(__file__, 'test_qoo_login', )])  # 测试数据
    def test_qoo_email_login(self, get_driver, email, pwd):
        logger.debug(email)
        qoo_login_page = QooLogin(get_driver)
        qoo_login_page.email_login(email=email, pwd=pwd)
        assert qoo_login_page.get_user_login_stats() is not None

    @allure.feature("qoo mobile login")  # 测试用例特性（主要功能模块）
    @allure.story("登錄驗證")  # 模块说明
    @allure.title("忘記密碼")  # 用例标题
    @allure.description('忘記密碼')  # 用例描述
    @pytest.mark.test_qoo_login_web  # 用列标记
    @pytest.mark.parametrize('email', [reda_pytest_data(__file__, 'test_qoo_login')])  # 测试数据
    def test_forget_pwd(self, get_driver, email):
        qoo_login_page = QooLogin(get_driver)
        qoo_login_page.forget_pwd(email=email)
        assert qoo_login_page.get_user_login_stats() is not None

    @allure.feature("qoo pc login")  # 测试用例特性（主要功能模块）
    @allure.story("登錄驗證")  # 模块说明
    @allure.title("第三方登錄-discord")  # 用例标题
    @allure.description('使用discord登錄')  # 用例描述
    @pytest.mark.test_qoo_login_web  # 用列标记
    @pytest.mark.parametrize('discord_email,discord_pwd', [reda_pytest_data(__file__, 'test_qoo_login')])
    @pytest.mark.skip
    def test_qoo_discord_login(self, get_driver, discord_email, discord_pwd):
        logging.debug(f'discord_email:{discord_email},discord_pwd:{discord_pwd}')
        login_page = QooLogin(get_driver)
        login_page.click_login_button()
        login_page.click_discord_icon()
        login_page.input_discord_email(discord_email=discord_email)
        login_page.input_discord_pwd_and_submit(discord_pwd=discord_pwd)
        assert login_page.get_user_login_stats() is not None
