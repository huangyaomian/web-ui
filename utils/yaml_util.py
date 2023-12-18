# -*- coding: utf-8 -*-
import yaml
from selenium.webdriver.common.by import By

from config import ELEMENT_FILE_PATH


def get_element_by(element_key: str) -> tuple[By, str]:
    """
    點擊登入按鈕
    :return:
    """
    with open(ELEMENT_FILE_PATH, 'r', encoding='utf-8') as file:
        data = yaml.safe_load(file)
    my_type = data[element_key]['type'].lower()
    my_locate = data[element_key]['locate']

    if my_type == By.ID:
        return By.ID, my_locate
    elif my_type == By.XPATH:
        return By.XPATH, my_locate
    elif my_type == "link_text" or my_type == "link":
        return By.LINK_TEXT, my_locate
    elif my_type == "partial_link_text" or my_type == "partial":
        return By.PARTIAL_LINK_TEXT, my_locate
    elif my_type == By.NAME:
        return By.NAME, my_locate
    elif my_type == "tag_name" or my_type == "tag":
        return By.TAG_NAME, my_locate
    elif my_type == "class_name" or my_type == "class":
        return By.CLASS_NAME, my_locate
    elif my_type == "css" or my_type == "css_selector":
        return By.CSS_SELECTOR, my_locate
    elif my_type == "function":
        return my_type, my_locate

    else:
        raise Exception(f'定位类型错误！！！！{my_type}')
