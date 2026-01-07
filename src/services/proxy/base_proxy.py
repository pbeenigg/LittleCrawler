
# @Url     : KuaiDaili HTTP implementation, official documentation: https://www.kuaidaili.com/?ref=ldwkjqipvz6c
import json
from abc import ABC, abstractmethod
from typing import List

import config
from src.services.cache.abs_cache import AbstractCache
from src.services.cache.cache_factory import CacheFactory
from src.utils.utils import utils

from .types import IpInfoModel


class IpGetError(Exception):
    """ ip get error"""


class ProxyProvider(ABC):
    @abstractmethod
    async def get_proxy(self, num: int) -> List[IpInfoModel]:
        """
        Abstract method to get IP, different HTTP proxy providers need to implement this method
        :param num: Number of IPs to extract
        :return:
        """
        raise NotImplementedError



class IpCache:
    def __init__(self):
        self.cache_client: AbstractCache = CacheFactory.create_cache(cache_type=config.CACHE_TYPE_REDIS)

    def set_ip(self, ip_key: str, ip_value_info: str, ex: int):
        """
        Set IP with expiration time, Redis is responsible for deletion after expiration
        :param ip_key:
        :param ip_value_info:
        :param ex:
        :return:
        """
        self.cache_client.set(key=ip_key, value=ip_value_info, expire_time=ex)

    def load_all_ip(self, proxy_brand_name: str) -> List[IpInfoModel]:
        """
        Load all unexpired IP information from Redis
        :param proxy_brand_name: Proxy provider name
        :return:
        """
        all_ip_list: List[IpInfoModel] = []
        all_ip_keys: List[str] = self.cache_client.keys(pattern=f"{proxy_brand_name}_*")
        try:
            for ip_key in all_ip_keys:
                ip_value = self.cache_client.get(ip_key)
                if not ip_value:
                    continue
                all_ip_list.append(IpInfoModel(**json.loads(ip_value)))
        except Exception as e:
            utils.logger.error("[IpCache.load_all_ip] get ip err from redis db", e)
        return all_ip_list
