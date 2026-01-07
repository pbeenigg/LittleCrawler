# -*- coding: utf-8 -*-



from typing import TYPE_CHECKING, Optional

from src.utils import utils

if TYPE_CHECKING:
    from src.services.proxy.proxy_ip_pool import ProxyIpPool


class ProxyRefreshMixin:
    """
    Auto-refresh proxy Mixin class

    Usage:
    1. Let client class inherit this Mixin
    2. Call init_proxy_pool(proxy_ip_pool) in client's __init__
    3. Call await _refresh_proxy_if_expired() before each request method call

    Requirements:
    - client class must have self.proxy attribute to store current proxy URL
    """

    _proxy_ip_pool: Optional["ProxyIpPool"] = None

    def init_proxy_pool(self, proxy_ip_pool: Optional["ProxyIpPool"]) -> None:
        """
        Initialize proxy pool reference
        Args:
            proxy_ip_pool: Proxy IP pool instance
        """
        self._proxy_ip_pool = proxy_ip_pool

    async def _refresh_proxy_if_expired(self) -> None:
        """
        Check if proxy has expired, automatically refresh if so
        Call this method before each request to ensure proxy is valid
        """
        if self._proxy_ip_pool is None:
            return

        if self._proxy_ip_pool.is_current_proxy_expired():
            utils.logger.info(
                f"[{self.__class__.__name__}._refresh_proxy_if_expired] Proxy expired, refreshing..."
            )
            new_proxy = await self._proxy_ip_pool.get_or_refresh_proxy()
            # Update httpx proxy URL
            if new_proxy.user and new_proxy.password:
                self.proxy = f"http://{new_proxy.user}:{new_proxy.password}@{new_proxy.ip}:{new_proxy.port}"
            else:
                self.proxy = f"http://{new_proxy.ip}:{new_proxy.port}"
            utils.logger.info(
                f"[{self.__class__.__name__}._refresh_proxy_if_expired] New proxy: {new_proxy.ip}:{new_proxy.port}"
            )
