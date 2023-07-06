# -*- coding: utf-8 -*-
# @File: conftest.py.py
# @Author: Mika
# @E-mail: yaomian@qoo-app.com
# @Time: 2020/10/26  20:16
import pytest

from public import WebInit, AppInit
from public import reda_conf

from selenium import webdriver

from public.web_base import WEB_UI

driver: webdriver.Chrome = None


@pytest.fixture(scope="session", autouse=True)
def open_browser():
    CASE_TYPE = reda_conf('CURRENCY').get('CASE_TYPE')
    APP_UI = reda_conf('APP_UI')
    IS_EXIT_APPLICATION = APP_UI.get('APP_IS_EXIT_APPLICATION')
    PLATFORM = APP_UI.get('APP_PLATFORM')
    ANDROID_CAPA = APP_UI.get('ANDROID_CAPA')
    IOS_CAPA = APP_UI.get('IOS_CAPA')
    global driver
    if CASE_TYPE.lower() == 'app':
        driver = AppInit().enable
        yield driver
        if IS_EXIT_APPLICATION:  # 是否退出应用操作
            if PLATFORM.lower() == 'android':
                appname = ANDROID_CAPA["appPackage"]
            else:
                appname = IOS_CAPA["udid"]
            driver.terminate_app(appname)  # 退出应用
        driver.quit()
    else:
        if driver is None:
            driver = WebInit().enable
        yield driver
        driver.quit()


@pytest.fixture(scope='function', autouse=True)
def get_driver():
    yield driver
    driver.get(WEB_UI.get('WEB_URL'))


def pytest_collection_modifyitems(items):
    """
    测试用例收集完成时，将收集到的name和nodeid的中文显示在控制台上
    """
    for i in items:
        i.name = i.name.encode("utf-8").decode("unicode_escape")
        print(i.nodeid)
        i._nodeid = i.nodeid.encode("utf-8").decode("unicode_escape")
