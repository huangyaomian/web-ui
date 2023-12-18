# -*- coding: utf-8 -*-
# @File: conftest.py
# @Author: Mika
# @E-mail: yaomian@qoo-app.com
# @Time: 2020/10/26  20:16
import os
import time

import allure
import pytest
from loguru import logger

from public import WebInit, AppInit
from public import reda_conf

from selenium import webdriver

from public.web_base import WEB_UI

from selenium_stealth import stealth

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
    time.sleep(1)



def pytest_collection_modifyitems(items):
    """
    测试用例收集完成时，将收集到的name和nodeid的中文显示在控制台上
    """
    for i in items:
        i.name = i.name.encode("UTF-8").decode("unicode_escape")
        print(i.nodeid)
        i._nodeid = i.nodeid.encode("UTF-8").decode("unicode_escape")


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """
    获取用例执行结果的钩子函数
    :param item:
    :param call:
    :return:
    """
    outcome = yield
    report = outcome.get_result()
    if report.when == "call" and report.failed:
        mode = "a" if os.path.exists("failures") else "w"
        with open("failures", mode, encoding='utf-8') as f:
            if "tmpir" in item.fixturenames:
                extra = " (%s)" % item.funcargs["tmpdir"]
            else:
                extra = ""
                f.write(report.nodeid + extra + "\n")
            with allure.step('添加失败截图...'):
                allure.attach(driver.get_screenshot_as_png(), "失败截图", allure.attachment_type.PNG)
