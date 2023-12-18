from typing import TypeVar

import redis
from loguru import logger
from sshtunnel import SSHTunnelForwarder

from public.common import reda_conf

DB = reda_conf('DB')
REDIS = DB.get('REDIS')
SSH = DB.get('SSH')

T = TypeVar('T')  # 可以是任何类型。


class RedisPool:
    """
    redis 操作类    demo  re = RedisPool(0)  re.set('han','2019')  re.get('han')

    """
    __Pool = None

    def __init__(self, db: int):
        """

        @rtype: object
        """
        self.session = self.redis_conn(db)

    def redis_conn(self, db: int) -> T:
        """
        连接redis 操作
        :return:
        """
        try:
            if not RedisPool.__Pool:
                server = SSHTunnelForwarder(
                    ssh_address_or_host=(SSH['host'], SSH['port']),  # ssh 目标服务器 ip 和 port
                    ssh_username=SSH['user'],  # ssh 目标服务器用户名
                    ssh_pkey=SSH['pkey'],  # ssh 目标服务器用户密码
                    remote_bind_address=(REDIS.get('host'), REDIS.get('port')),  # mysql 服务ip 和 part
                    local_bind_address=('127.0.0.1', 3308),  # ssh 目标服务器的用于连接 mysql 或 redis 的端口，该 ip 必须为 127.0.0.1
                )
                server.start()

                # 连接到 Redis
                session = redis.Redis(server.local_bind_host, port=server.local_bind_port, db=db)
                return session

        except Exception as e:
            logger.error(f'连接错误！{e}')

    def set(self, key: str, value: str) -> T:
        """
        redis  set 操作
        :param key: 键
        :param value: 值
        :return:
        """
        ret = self.session.set(key, value)
        self.session.close()
        return ret

    def delete(self, key: str) -> int:
        """
        删除 Redis key
        :param key: 键
        :return: 删除的键的数量
        """
        value = self.session.delete(key)
        self.session.close()
        return value

    def get_scan_with_pagination(self, pattern, count=100, limit=1000):
        """
        使用 SCAN 命令进行分页获取匹配给定模式的键
        :param pattern: 匹配模式
        :param count: 每次 SCAN 命令的返回数量
        :param limit: 结果列表的最大长度限制
        :return: 匹配的键列表
        """
        keys = []
        cursor = 0
        while len(keys) < limit:
            cursor, elements = self.session.scan(cursor, match=pattern, count=count)
            if elements:
                keys.extend(elements)
            if cursor == 0:
                break
        return keys

    def delete_redis_keys(self, pattern, exclude_key: str = None):
        """
            删除匹配给定模式的所有键
            :param pattern: 匹配模式
            :param exclude_key: 需要排除不刪除的key
            :return: 删除的键的数量
            """
        keys = self.get_scan_with_pagination(pattern=pattern)
        for key in keys:
            if str(key, 'utf-8') != exclude_key:
                self.delete(key)

    def get(self, key: str) -> T:
        """
        redis get 操作
        :param key: 键
        :return:
        """
        value = self.session.get(key)

        self.session.close()
        if value is not None:
            return value
        else:
            logger.error('无此key')
            return None

    def get_ttl(self, key: str) -> int:
        """
        获取 Redis 键的 TTL
        :param key: 键名
        :return: TTL，单位为秒
        """
        ttl = self.session.ttl(key)
        self.session.close()
        logger.debug(f'ttl:{ttl}')
        return ttl


if __name__ == '__main__':
    RedisPool(7).delete_redis_keys('ID-CACHE:SDK:LIMIT-Key-email-forget-password:*')
