# -*- coding: utf-8 -*-
# @File: db.py
# @Author: Mika
# @E-mail: yaomian@qoo-app.com
# @Time: 2021/3/18  19:23

from typing import TypeVar, Tuple, List

import cx_Oracle
import redis
from rediscluster import RedisCluster

from public.common import logger, reda_conf

T = TypeVar('T')  # 可以是任何类型。

# 读取配置参数
DB = reda_conf('DB')
SSH = DB.get('SSH')
MYSQL = DB.get('MYSQL')
ORACLE = DB.get('ORACLE')
REDIS = DB.get('REDIS')
REDIS_CLUSTER = DB.get('REDIS_CLUSTER')
REDIS_CLUSTER_PASSWORD = DB.get('REDIS_CLUSTER_PASSWORD')



class Oracle:
    """
    Oracle 操作类  demo  Oracle.select('SELECT * FROM `case`')
    """

    @classmethod
    def connOracle(cls) -> T:
        """
        Oracle 连接客户端
        :return:
        """
        try:
            info = list(ORACLE.values())
            db = cx_Oracle.connect(f'{info[0]}/{info[1]}@{info[2]}')
            logger.debug('1111')
            return db
        except Exception as e:
            logger.error(f'连接Oracle客户端错误!{e}')

    @classmethod
    def ex_select(cls, sql: str) -> Tuple or List:
        """ 查询
        Oracle sql 执行
        :param sql:  sql str
        :return: tupe
        """
        try:
            conn = cls.connOracle()
            cursor = conn.cursor()
            cursor.execute(sql)
            select_data = cursor.fetchall()
            cursor.close()
            conn.close()
            logger.debug('查询sql成功！！')
            return select_data
        except Exception as e:
            logger.error(f'执行Oracle 查询异常{e}')

    @classmethod
    def ex_insert(cls, sql: str) -> Tuple or List:
        """ 插入
        Oracle sql 执行
        :param sql:  sql str
        :return: tupe
        """
        try:
            conn = cls.connOracle()
            cursor = conn.cursor()

            cursor.execute(sql)
            conn.commit()

            cursor.close()
            conn.close()
            logger.debug('提交sql成功！！')
        except Exception as e:
            logger.error(f'执行Oracle 插入异常{e}')





class RedisPoolCluster:
    """
    redsi 集群操作类
    """

    def __init__(self):

        self.session = self.connect()

    def connect(self):
        """
        连接redis集群
        :return: object
        """
        try:
            redisconn = RedisCluster(startup_nodes=REDIS_CLUSTER, password=REDIS_CLUSTER_PASSWORD)
            return redisconn
        except Exception as e:
            logger.error(f"错误,连接redis 集群失败 {e}")
            return None

    def set(self, key: T, value: T) -> T:
        """
        redis  set 操作
        :param key: 键
        :param value: 值
        :return:
        """
        set_key = self.session.set(key, value)
        self.session.close()
        return set_key

    def get(self, key: T) -> T:
        """
         获取指定键
        :param key:  key
        :return:
        """
        get_key = self.session.get(key)
        self.session.close()
        return get_key

    def keys(self) -> T:
        """
        获取所有键
        :return:
        """
        keys_all = self.session.keys()
        self.session.close()
        return keys_all

    @property
    def opt(self) -> T:
        """
        reis 操作   RedisPoolCluster.opt.xxxx
        :return:
        """
        return self.session
