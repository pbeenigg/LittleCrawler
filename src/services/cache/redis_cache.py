
# -*- coding: utf-8 -*-
import pickle
import time
from typing import Any, List

from redis import Redis

from src.services.cache.abs_cache import AbstractCache
from config import db_config


class RedisCache(AbstractCache):

    def __init__(self) -> None:
        # Connect to redis, return redis client
        self._redis_client = self._connet_redis()

    @staticmethod
    def _connet_redis() -> Redis:
        """
        Connect to redis, return redis client, configure redis connection information as needed
        :return:
        """
        return Redis(
            host=db_config.REDIS_DB_HOST,
            port=db_config.REDIS_DB_PORT,
            db=db_config.REDIS_DB_NUM,
            password=db_config.REDIS_DB_PWD,
        )

    def get(self, key: str) -> Any:
        """
        Get the value of a key from the cache and deserialize it
        :param key:
        :return:
        """
        value = self._redis_client.get(key)
        if value is None:
            return None
        return pickle.loads(value)

    def set(self, key: str, value: Any, expire_time: int) -> None:
        """
        Set the value of a key in the cache and serialize it
        :param key:
        :param value:
        :param expire_time:
        :return:
        """
        self._redis_client.set(key, pickle.dumps(value), ex=expire_time)

    def keys(self, pattern: str) -> List[str]:
        """
        Get all keys matching the pattern
        """
        return [key.decode() for key in self._redis_client.keys(pattern)]


if __name__ == '__main__':
    redis_cache = RedisCache()
    # basic usage
    redis_cache.set("name", "pbeenig", 1)
    print(redis_cache.get("name"))  # pbeenig
    print(redis_cache.keys("*"))  # ['name']
    time.sleep(2)
    print(redis_cache.get("name"))  # None

    # special python type usage
    # list
    redis_cache.set("list", [1, 2, 3], 10)
    _value = redis_cache.get("list")
    print(_value, f"value type:{type(_value)}")  # [1, 2, 3]
