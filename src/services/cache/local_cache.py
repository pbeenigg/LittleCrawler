
# -*- coding: utf-8 -*-
# @Desc    : Local cache

import asyncio
import time
from typing import Any, Dict, List, Optional, Tuple

from src.services.cache.abs_cache import AbstractCache


class ExpiringLocalCache(AbstractCache):

    def __init__(self, cron_interval: int = 10):
        """
        Initialize local cache
        :param cron_interval: Time interval for scheduled cache cleanup
        :return:
        """
        self._cron_interval = cron_interval
        self._cache_container: Dict[str, Tuple[Any, float]] = {}
        self._cron_task: Optional[asyncio.Task] = None
        # Start scheduled cleanup task
        self._schedule_clear()

    def __del__(self):
        """
        Destructor function, cleanup scheduled task
        :return:
        """
        if self._cron_task is not None:
            self._cron_task.cancel()

    def get(self, key: str) -> Optional[Any]:
        """
        Get the value of a key from the cache
        :param key:
        :return:
        """
        value, expire_time = self._cache_container.get(key, (None, 0))
        if value is None:
            return None

        # If the key has expired, delete it and return None
        if expire_time < time.time():
            del self._cache_container[key]
            return None

        return value

    def set(self, key: str, value: Any, expire_time: int) -> None:
        """
        Set the value of a key in the cache
        :param key:
        :param value:
        :param expire_time:
        :return:
        """
        self._cache_container[key] = (value, time.time() + expire_time)

    def keys(self, pattern: str) -> List[str]:
        """
        Get all keys matching the pattern
        :param pattern: Matching pattern
        :return:
        """
        if pattern == '*':
            return list(self._cache_container.keys())

        # For local cache wildcard, temporarily replace * with empty string
        if '*' in pattern:
            pattern = pattern.replace('*', '')

        return [key for key in self._cache_container.keys() if pattern in key]

    def _schedule_clear(self):
        """
        Start scheduled cleanup task
        :return:
        """

        try:
            loop = asyncio.get_event_loop()
        except RuntimeError:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)

        self._cron_task = loop.create_task(self._start_clear_cron())

    def _clear(self):
        """
        Clean up cache based on expiration time
        :return:
        """
        for key, (value, expire_time) in self._cache_container.items():
            if expire_time < time.time():
                del self._cache_container[key]

    async def _start_clear_cron(self):
        """
        Start scheduled cleanup task
        :return:
        """
        while True:
            self._clear()
            await asyncio.sleep(self._cron_interval)


if __name__ == '__main__':
    cache = ExpiringLocalCache(cron_interval=2)
    cache.set('name', 'pbeenig', 3)
    print(cache.get('key'))
    print(cache.keys("*"))
    time.sleep(4)
    print(cache.get('key'))
    del cache
    time.sleep(1)
    print("done")
