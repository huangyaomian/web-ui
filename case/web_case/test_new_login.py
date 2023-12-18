# -*- coding: utf-8 -*-
# @File: test_demo.py
# @Author: Mika
# @E-mail: yaomian@qoo-app.com
# @Time: 2020/10/26  11:08

import allure
import pytest

from page.new_login_page import QooNewLogin
from public.reda_data import reda_pytest_data, RandomData
from utils.ip_util import get_public_ip_address
from utils.mysql import db_get_email
from utils.redis_util import RedisPool
from utils.str_util import my_find
from utils.time_util import get_remaining_seconds_until_midnight


@allure.story("新登录方式的登录验证")
class TestNewLogin:
    login_redis_key = 'ID-CACHE:SDK:LIMIT-Key-login:'
    forget_pwd_redis_key = 'ID-CACHE:SDK:LIMIT-Key-email-forget-password:'
    forget_pwd_redis_keys = 'ID-CACHE:SDK:LIMIT-Key-email-forget-password:*'

    @pytest.fixture(autouse=True)
    def setup(self, get_driver):
        self.qoo_login_page = QooNewLogin(get_driver)
        self.qoo_login_page.click_login_test_btn()

    @allure.title("驗證三次登錄失敗，會彈出滑動驗證碼")  # 用例标题
    @allure.description('驗證滑動驗證碼的彈出和需不需要彈出滑動驗證碼的緩存時效')
    @pytest.mark.test_new_login_web  # 用列标记
    @pytest.mark.parametrize('email,pwd', reda_pytest_data(__file__, 'test_email_login_fail_slide_code'))  # 测试数据
    @pytest.mark.run(order=1)
    def test_email_login_fail_slide_code(self, email, pwd):
        redis_pool = RedisPool(7)
        redis_pool.delete(self.login_redis_key + email)
        self.qoo_login_page.email_login(email, pwd)
        self.qoo_login_page.sleep(4)
        self.qoo_login_page.click_login_btn()
        self.qoo_login_page.sleep(4)
        self.qoo_login_page.click_login_btn()
        time = abs(get_remaining_seconds_until_midnight() - redis_pool.get_ttl(self.login_redis_key + email))
        self.qoo_login_page.sleep(4)
        self.qoo_login_page.click_login_btn()
        assert self.qoo_login_page.is_captcha_slider() and time < 20

    @allure.title("正確郵箱登錄")  # 用例标题
    @allure.description('輸入用戶名和密碼')  # 用例描述
    @pytest.mark.test_new_login_web  # 用列标记
    @pytest.mark.parametrize('email,pwd', reda_pytest_data(__file__, 'test_qoo_email_login'))  # 测试数据
    @pytest.mark.run(order=2)
    def test_qoo_email_login(self, email, pwd):
        RedisPool(7).delete(self.login_redis_key + email)
        self.qoo_login_page.email_login(email, pwd)
        assert self.qoo_login_page.get_user_login_stats()

    @allure.title("錯誤郵箱登錄")  # 用例标题
    @allure.description('錯誤郵箱登錄')  # 用例描述
    @pytest.mark.test_new_login_web  # 用列标记
    @pytest.mark.parametrize('email,pwd,tip', reda_pytest_data(__file__, 'test_qoo_email_login_error'))  # 测试数据
    @pytest.mark.run(order=3)
    def test_qoo_email_login_error(self, email, pwd, tip):
        RedisPool(7).delete(self.login_redis_key + email)
        self.qoo_login_page.email_login(email, pwd)
        assert self.qoo_login_page.get_user_login_stats()

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
        assert not qoo_login_page.is_email_format_error_tip()

    @allure.title("勾選條款提示")  # 用例标题
    @allure.description('驗證勾選條款提示')  # 用例描述
    @pytest.mark.test_new_login_web  # 用列标记
    @pytest.mark.parametrize('tip', reda_pytest_data(__file__, 'test_login_need_allow_protocol'))  # 测试数据
    @pytest.mark.run(order=31)
    def test_login_need_allow_protocol(self, get_driver, tip):
        qoo_login_page = QooNewLogin(get_driver)
        assert qoo_login_page.login_need_allow_protocol(tip=tip)

    @allure.title("未綁定uid和通行證郵箱的fb登錄")
    @allure.description('未綁定uid和通行證郵箱的fb登錄')
    @pytest.mark.test_new_login_web
    @pytest.mark.parametrize('email,tip', reda_pytest_data(__file__, 'test_check_email_format_error_case'))  # 测试数据
    @pytest.mark.run(order=3)
    def test_fb_login(self, email, tip):
        self.qoo_login_page.fb_login_for_not_register(email=email)
        assert True

    @allure.title("未綁定uid和通行證郵箱的gp登錄")
    @allure.description('未綁定uid和通行證郵箱的gp登錄')
    @pytest.mark.test_new_login_web
    @pytest.mark.parametrize('email,tip', reda_pytest_data(__file__, 'test_check_email_format_error_case'))  # 测试数据
    @pytest.mark.run(order=3)
    def test_google_login(self, get_driver, email, tip):
        get_driver.get('https://accounts.google.com/o/oauth2/v2/auth/oauthchooseaccount?redirect_uri=https%3A%2F%2Fdevelopers.google.com%2Foauthplayground&prompt=consent&response_type=code&client_id=407408718192.apps.googleusercontent.com&scope=email&access_type=offline&flowName=GeneralOAuthFlow')
        self.qoo_login_page.google_login_for_not_register(email=email)
        assert True

    # region 忘記密碼相關的
    @allure.title("忘記密碼")  # 用例标题
    @allure.description('忘記密碼')  # 用例描述
    @pytest.mark.test_new_login_web  # 用列标记
    @pytest.mark.parametrize('email', reda_pytest_data(__file__, 'test_forget_pwd'))  # 测试数据
    @pytest.mark.run(order=61)
    def test_forget_pwd(self, email):
        RedisPool(7).delete_redis_keys(self.forget_pwd_redis_keys)
        pwd = RandomData().generate_random_alphanumeric(10)
        self.qoo_login_page.forget_pwd(email=email, pwd=pwd)
        self.qoo_login_page.email_login(email, pwd)
        assert self.qoo_login_page.get_user_login_stats()

    @allure.title("未綁定uid的郵箱獲取忘記密碼的驗證碼")  # 用例标题
    @pytest.mark.test_new_login_web  # 用列标记
    @pytest.mark.run(order=62)
    def test_forget_pwd_unavailable_email(self, get_driver):
        self.qoo_login_page.forget_pwd_get_code(RandomData().random_email())
        assert True

    @allure.title("忘記密碼，自然天內同一郵箱只能獲取10次")  # 用例标题
    @pytest.mark.test_new_login_web  # 用列标记
    @pytest.mark.parametrize('email', reda_pytest_data(__file__, 'test_forget_pwd'))  # 测试数据
    @pytest.mark.run(order=63)
    def test_forget_pwd_code_for_email(self, email):
        redis_pool = RedisPool(7)
        redis_pool.delete_redis_keys(self.forget_pwd_redis_keys)
        for i in range(10):
            self.qoo_login_page.forget_pwd_get_code(email)
            self.qoo_login_page.sleep(2)
            self.qoo_login_page.click_back_btn()
        redis_pool.delete_redis_keys(self.forget_pwd_redis_keys, self.forget_pwd_redis_key + email)
        self.qoo_login_page.forget_pwd_get_code(email)
        time = abs(
            abs(get_remaining_seconds_until_midnight()) - abs(redis_pool.get_ttl(self.forget_pwd_redis_key + email)))
        assert self.qoo_login_page.is_visibility_many_code_tip() and time < 20

    @allure.title("忘記密碼，自然天內同ip，獲取驗證碼只能10次")  # 用例标题
    @pytest.mark.test_new_login_web  # 用列标记
    @pytest.mark.run(order=63)
    def test_forget_pwd_code_for_ip(self):
        redis_pool = RedisPool(7)
        redis_pool.delete_redis_keys(self.forget_pwd_redis_keys)
        emails = db_get_email()
        for item in emails:
            self.qoo_login_page.forget_pwd_get_code(item['email'])
            self.qoo_login_page.sleep(2)
            self.qoo_login_page.click_back_btn()
        self.qoo_login_page.forget_pwd_get_code(emails[0]['email'])
        time = abs(abs(get_remaining_seconds_until_midnight())
                   - abs(redis_pool.get_ttl(self.forget_pwd_redis_key + get_public_ip_address())))
        assert self.qoo_login_page.is_visibility_many_code_tip() and time < 20

    @allure.title("忘記密碼，自然天內同ip，獲取驗證碼只能10次")  # 用例标题
    @pytest.mark.test_new_login_web  # 用列标记
    @pytest.mark.run(order=63)
    def test_forget_pwd_code_for_ipi(self):
        db_get_email()

    @allure.title("驗證忘記密碼正確郵箱格式")  # 用例标题
    @allure.description('驗證忘記密碼正確郵箱格式')  # 用例描述
    @pytest.mark.test_new_login_web  # 用列标记
    @pytest.mark.parametrize('email', reda_pytest_data(__file__, 'test_check_email_format_correct'))  # 测试数据
    @pytest.mark.run(order=67)
    def test_check_forget_pwd_email_format_correct(self, email):
        self.qoo_login_page.click_forget_pwd_btn()
        self.qoo_login_page.input_forget_pwd_email(email=email)
        assert not self.qoo_login_page.is_email_format_error_tip()

    @allure.title("驗證忘記密碼錯誤郵箱格式")  # 用例标题
    @allure.description('驗證忘記密碼錯誤郵箱格式')  # 用例描述
    @pytest.mark.test_new_login_web  # 用列标记
    @pytest.mark.parametrize('email,tip', reda_pytest_data(__file__, 'test_check_email_format_error_case'))  # 测试数据
    @pytest.mark.run(order=63)
    def test_check_forget_pwd_email_format_error(self, email, tip):
        self.qoo_login_page.click_forget_pwd_btn()
        self.qoo_login_page.input_forget_pwd_email(email=email)
        assert my_find(self.qoo_login_page.get_email_format_error_tip(), tip)

    # endregion

    @allure.title("協議跳轉")  # 用例标题
    @allure.description('協議跳轉')  # 用例描述
    @pytest.mark.test_new_login_web  # 用列标记
    @pytest.mark.run(order=101)
    def test_check_protocol_jump(self, get_driver):
        driver = get_driver
        current_window = driver.current_window_handle
        self.qoo_login_page.click_terms_btn()
        self.qoo_login_page.sleep(3)
        driver.switch_to.window(driver.window_handles[-1])
        url = driver.current_url
        if not my_find(driver.current_url, 'terms'):
            assert False
        driver.switch_to.window(current_window)
        self.qoo_login_page.click_privacy_btn()
        self.qoo_login_page.sleep(3)
        driver.switch_to.window(driver.window_handles[-1])
        assert my_find(driver.current_url, 'privacy')
