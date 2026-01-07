# -*- coding: utf-8 -*-
"""
LittleCrawler API 模块

提供基于FastAPI的RESTful API服务，包括：
- 用户认证（登录/登出）
- 爬虫控制（启动/停止/状态）
- 数据管理（文件列表/预览/下载）
- WebSocket实时通信

启动: uvicorn api.main:app --port 8080 --reload
默认账号: admin / admin123
"""
