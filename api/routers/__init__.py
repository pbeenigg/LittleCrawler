# -*- coding: utf-8 -*-
"""
路由模块初始化

导出所有API路由：
- auth_router: 认证相关（登录、登出、用户信息）
- crawler_router: 爬虫控制（启动、停止、状态）
- data_router: 数据管理（文件列表、预览、下载）
- websocket_router: WebSocket实时通信
"""

from .auth import router as auth_router
from .crawler import router as crawler_router
from .data import router as data_router
from .websocket import router as websocket_router

__all__ = ["auth_router", "crawler_router", "data_router", "websocket_router"]
