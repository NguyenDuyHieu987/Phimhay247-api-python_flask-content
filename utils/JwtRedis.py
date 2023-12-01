import redis
import os
from datetime import datetime, timezone, timedelta
from configs.RedisCache import RedisCache


class JwtRedis(RedisCache):
    __redisPrefix = ""

    def __init__(self, prefix=""):
        self.__rd = self.ConnectRedis()
        self.__redisPrefix = prefix

    def __init_key(self, key):
        my_key = f"{self.__redisPrefix}_{key}"

        return my_key

    def set_prefix(self, prefix):
        self.__redisPrefix = prefix

        return self

    def sign(self, jwt, option={"exp": None}):
        key = self.__init_key(jwt)

        self.__rd.set(key, "True", ex=option["exp"])

    def verify(self, jwt):
        key = self.__init_key(jwt)

        if self.__rd.exists(key):
            return False
        else:
            return True
