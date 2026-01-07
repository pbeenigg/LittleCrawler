
# -*- coding: utf-8 -*-

import time
import unittest

from src.services.cache.local_cache import ExpiringLocalCache


class TestExpiringLocalCache(unittest.TestCase):

    def setUp(self):
        self.cache = ExpiringLocalCache(cron_interval=10)

    def test_set_and_get(self):
        self.cache.set('key', 'value', 10)
        self.assertEqual(self.cache.get('key'), 'value')

    def test_expired_key(self):
        self.cache.set('key', 'value', 1)
        time.sleep(2)  # wait for the key to expire
        self.assertIsNone(self.cache.get('key'))

    def test_clear(self):
        # Set two key-value pairs with expiration time of 11 seconds
        self.cache.set('key', 'value', 11)
        # Sleep for 12 seconds to let the cache class's scheduled task execute once
        time.sleep(12)
        self.assertIsNone(self.cache.get('key'))

    def tearDown(self):
        del self.cache


if __name__ == '__main__':
    unittest.main()
