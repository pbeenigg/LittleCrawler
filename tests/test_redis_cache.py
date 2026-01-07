
# -*- coding: utf-8 -*-

import time
import unittest

from src.services.cache.redis_cache import RedisCache


class TestRedisCache(unittest.TestCase):

    def setUp(self):
        self.redis_cache = RedisCache()

    def test_set_and_get(self):
        self.redis_cache.set('key', 'value', 10)
        self.assertEqual(self.redis_cache.get('key'), 'value')

    def test_expired_key(self):
        self.redis_cache.set('key', 'value', 1)
        time.sleep(2)  # wait for the key to expire
        self.assertIsNone(self.redis_cache.get('key'))

    def test_keys(self):
        self.redis_cache.set('key1', 'value1', 10)
        self.redis_cache.set('key2', 'value2', 10)
        keys = self.redis_cache.keys('*')
        self.assertIn('key1', keys)
        self.assertIn('key2', keys)

    def tearDown(self):
        # self.redis_cache._redis_client.flushdb()  # Clear redis database
        pass


if __name__ == '__main__':
    unittest.main()
