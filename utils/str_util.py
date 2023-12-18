# -*- coding: utf-8 -*-
import allure


def my_find(main_str: str, sub_str: str) -> bool:
    """
    判断main str中是否包含sub str，是返回True，否返回False
    @param main_str:
    @param sub_str:
    @return: 是返回True，否返回False
    """
    is_find = main_str.find(sub_str) != -1
    with allure.step(f'执行操作：判断【{main_str}】是否包含【{sub_str}】,结果为：{is_find}'):
        return is_find


