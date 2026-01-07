
# -*- coding: utf-8 -*-


class CacheFactory:
    """
    Cache factory class
    """

    @staticmethod
    def create_cache(cache_type: str, *args, **kwargs):
        """
        Create cache object
        :param cache_type: Cache type
        :param args: Arguments
        :param kwargs: Keyword arguments
        :return:
        """
        if cache_type == 'memory':
            from .local_cache import ExpiringLocalCache
            return ExpiringLocalCache(*args, **kwargs)
        elif cache_type == 'redis':
            from .redis_cache import RedisCache
            return RedisCache()
        else:
            raise ValueError(f'Unknown cache type: {cache_type}')
