import json
from datetime import datetime
from typing import Union

from public.common import logger, reda_conf
import pymysql
import pymysql.cursors
from sshtunnel import SSHTunnelForwarder


# 读取配置参数
DB = reda_conf('DB')
SSH = DB.get('SSH')
MYSQL = DB.get('MYSQL')
ORACLE = DB.get('ORACLE')
REDIS = DB.get('REDIS')
REDIS_CLUSTER = DB.get('REDIS_CLUSTER')
REDIS_CLUSTER_PASSWORD = DB.get('REDIS_CLUSTER_PASSWORD')


class MysqlServer:
    """
    初始化数据库连接(支持通过SSH隧道的方式连接)，并指定查询的结果集以字典形式返回
    """

    def __init__(self, db_host, db_port, db_user, db_pwd, db_database, ssh=False,
                 **kwargs):
        """
        初始化方法中， 连接mysql数据库， 根据ssh参数决定是否走SSH隧道方式连接mysql数据库
        """
        self.server = None
        if ssh:
            self.server = SSHTunnelForwarder(
                ssh_address_or_host=(kwargs.get("host"), kwargs.get("port")),  # ssh 目标服务器 ip 和 port
                ssh_username=kwargs.get("user"),  # ssh 目标服务器用户名
                ssh_pkey=kwargs.get("pkey"),  # ssh 目标服务器用户密码
                remote_bind_address=(db_host, db_port),  # mysql 服务ip 和 part
                local_bind_address=('127.0.0.1', 3307),  # ssh 目标服务器的用于连接 mysql 或 redis 的端口，该 ip 必须为 127.0.0.1
            )
            self.server.start()
            db_host = self.server.local_bind_host  # server.local_bind_host 是 参数 local_bind_address 的 ip
            db_port = self.server.local_bind_port  # server.local_bind_port 是 参数 local_bind_address 的 port
        # 建立连接
        self.conn = pymysql.connect(host=db_host,
                                    port=db_port,
                                    user=db_user,
                                    password=db_pwd,
                                    database=db_database,
                                    charset="utf8",
                                    cursorclass=pymysql.cursors.DictCursor  # 加上pymysql.cursors.DictCursor这个返回的就是字典
                                    )
        # 创建一个游标对象
        self.cursor = self.conn.cursor()

    def query_all(self, sql):
        """
        查询所有符合sql条件的数据
        :param sql: 执行的sql
        :return: 查询结果
        """
        try:
            self.conn.commit()
            self.cursor.execute(sql)
            data = self.cursor.fetchall()
            # 关闭数据库链接和隧道
            self.close()
            return self.verify(data)
        except Exception as e:
            logger.error(f"查询所有符合sql条件的数据报错: {e}")
            raise e

    def query_one(self, sql):
        """
        查询符合sql条件的数据的第一条数据
        :param sql: 执行的sql
        :return: 返回查询结果的第一条数据
        """
        try:
            self.conn.commit()
            self.cursor.execute(sql)
            data = self.cursor.fetchone()
            # 关闭数据库链接和隧道
            self.close()
            return self.verify(data)
        except Exception as e:
            logger.error(f"查询符合sql条件的数据的第一条数据报错: {e}")
            raise e

    def insert(self, sql):
        """
        插入数据
        :param sql: 执行的sql
        """
        try:
            self.cursor.execute(sql)
            # 提交  只要数据库更新就要commit
            self.conn.commit()
            # 关闭数据库链接和隧道
            self.close()
        except Exception as e:
            logger.error(f"插入数据报错: {e}")
            raise e

    def update(self, sql):
        """
        更新数据
        :param sql: 执行的sql
        """
        try:
            self.cursor.execute(sql)
            # 提交 只要数据库更新就要commit
            self.conn.commit()
            # 关闭数据库链接和隧道
            self.close()
        except Exception as e:
            logger.error(f"更新数据报错: {e}")
            raise e

    def query(self, sql, one=True):
        """
        根据传值决定查询一条数据还是所有
        :param sql: 查询的SQL语句
        :param one: 默认True. True查一条数据，否则查所有
        :return:
        """
        try:
            if one:
                return self.query_one(sql)
            else:
                return self.query_all(sql)
        except Exception as e:
            logger.error(f"查询数据报错: {e}")
            raise e

    def close(self):
        """
        断开游标，关闭数据库
        如果开启了SSH隧道，也关闭
        :return:
        """
        # 关闭游标
        self.cursor.close()
        # 关闭数据库链接
        self.conn.close()
        # 如果开启了SSH隧道，则关闭
        if self.server:
            self.server.close()

    def verify(self, result: dict) -> Union[dict, None]:
        """验证结果能否被json.dumps序列化"""
        # 尝试变成字符串，解决datetime 无法被json 序列化问题
        try:
            json.dumps(result)
        except TypeError:  # TypeError: Object of type datetime is not JSON serializable
            for k, v in result.items():
                if isinstance(v, datetime):
                    result[k] = str(v)
        return result


if __name__ == '__main__':
    ssh = True
    db = MysqlServer(MYSQL['host'], MYSQL['port'], MYSQL['user'], MYSQL['password'], MYSQL['db'], ssh,
                     **SSH)
    logger.debug(db.query_one(sql="select * from user limit 2;"))
