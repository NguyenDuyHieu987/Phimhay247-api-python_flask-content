import pymongo
import os
import redis


class RedisCache:
    def __init__(self):
        self.cache = None

    def ConnectRedis(self):
        try:
            rediscache = redis.Redis(
                host=os.getenv("REDIS_HOST"),
                port=os.getenv("REDIS_PORT"),
                username="default",
                password=os.getenv("REDIS_PASSWORD"),
            )

            self.cache = rediscache

            return self.cache
        except:
            pass
