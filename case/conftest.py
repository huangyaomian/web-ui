# -*- coding: utf-8 -*-
# @File: conftest.py.py
# @Author: Mika
# @E-mail: yaomian@qoo-app.com
# @Time: 2020/10/26  20:16
import pytest
from loguru import logger

from public import WebInit, AppInit
from public import reda_conf


@pytest.fixture(scope='function')
def get_driver():
    CASE_TYPE = reda_conf('CURRENCY').get('CASE_TYPE')
    APP_UI = reda_conf('APP_UI')
    IS_EXIT_APPLICATION = APP_UI.get('APP_IS_EXIT_APPLICATION')
    PLATFORM = APP_UI.get('APP_PLATFORM')
    ANDROID_CAPA = APP_UI.get('ANDROID_CAPA')
    IOS_CAPA = APP_UI.get('IOS_CAPA')
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
        driver = WebInit().enable
        logger.debug(f'driver.__hash__():{driver.__hash__()}')
        yield driver
        driver.quit()


def pytest_collection_modifyitems(items):
    """
    测试用例收集完成时，将收集到的name和nodeid的中文显示在控制台上
    """
    for i in items:
        i.name = i.name.encode("utf-8").decode("unicode_escape")
        print(i.nodeid)
        i._nodeid = i.nodeid.encode("utf-8").decode("unicode_escape")
