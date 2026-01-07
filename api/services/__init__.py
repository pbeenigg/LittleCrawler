# -*- coding: utf-8 -*-
"""
服务模块

导出所有业务服务：
- CrawlerManager: 爬虫进程管理器
- auth_service: 用户认证服务
"""

from .crawler_manager import CrawlerManager, crawler_manager

__all__ = ["CrawlerManager", "crawler_manager"]
