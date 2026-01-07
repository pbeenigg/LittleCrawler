# -*- coding: utf-8 -*-
"""
WebSocket路由模块

提供实时通信的WebSocket端点：
- WS /ws/logs - 实时日志推送
- WS /ws/status - 实时状态推送

WebSocket连接不需要Token认证（考虑到浏览器兼容性）
但仅在用户已登录后才会建立连接
"""

import asyncio
from typing import Set, Optional

from fastapi import APIRouter, WebSocket, WebSocketDisconnect

from ..services import crawler_manager

router = APIRouter(tags=["WebSocket"])


class ConnectionManager:
    """
    WebSocket连接管理器
    
    管理所有活跃的WebSocket连接，提供广播功能
    """

    def __init__(self):
        self.active_connections: Set[WebSocket] = set()

    async def connect(self, websocket: WebSocket):
        """接受新的WebSocket连接"""
        await websocket.accept()
        self.active_connections.add(websocket)

    def disconnect(self, websocket: WebSocket):
        """断开WebSocket连接"""
        self.active_connections.discard(websocket)

    async def broadcast(self, message: dict):
        """
        广播消息到所有连接
        
        自动清理断开的连接
        """
        if not self.active_connections:
            return

        disconnected = []
        for connection in list(self.active_connections):
            try:
                await connection.send_json(message)
            except Exception:
                disconnected.append(connection)

        # 清理断开的连接
        for conn in disconnected:
            self.disconnect(conn)


# 全局连接管理器实例
manager = ConnectionManager()


async def log_broadcaster():
    """
    后台任务：从队列读取日志并广播
    
    持续监听日志队列，将新日志推送给所有WebSocket客户端
    """
    queue = crawler_manager.get_log_queue()
    while True:
        try:
            # 从队列获取日志条目
            entry = await queue.get()
            # 广播到所有WebSocket连接
            await manager.broadcast(entry.model_dump())
        except asyncio.CancelledError:
            break
        except Exception as e:
            print(f"[日志广播] 错误: {e}")
            await asyncio.sleep(0.1)


# 全局广播任务
_broadcaster_task: Optional[asyncio.Task] = None


def start_broadcaster():
    """启动广播任务"""
    global _broadcaster_task
    if _broadcaster_task is None or _broadcaster_task.done():
        _broadcaster_task = asyncio.create_task(log_broadcaster())


@router.websocket("/ws/logs")
async def websocket_logs(websocket: WebSocket):
    """
    WebSocket日志流
    
    实时推送爬虫运行日志，支持心跳保活
    客户端发送'ping'，服务端响应'pong'
    """
    print("[WS] 新连接请求")

    try:
        # 确保广播任务运行中
        start_broadcaster()

        await manager.connect(websocket)
        print(f"[WS] 已连接，活跃连接数: {len(manager.active_connections)}")

        # 发送历史日志
        for log in crawler_manager.logs:
            try:
                await websocket.send_json(log.model_dump())
            except Exception as e:
                print(f"[WS] 发送历史日志错误: {e}")
                break

        print(f"[WS] 已发送 {len(crawler_manager.logs)} 条历史日志，进入主循环")

        while True:
            # 保持连接，接收心跳或其他消息
            try:
                data = await asyncio.wait_for(
                    websocket.receive_text(),
                    timeout=30.0
                )
                if data == "ping":
                    await websocket.send_text("pong")
            except asyncio.TimeoutError:
                # 发送ping保持连接
                try:
                    await websocket.send_text("ping")
                except Exception as e:
                    print(f"[WS] 发送ping错误: {e}")
                    break

    except WebSocketDisconnect:
        print("[WS] 客户端断开连接")
    except Exception as e:
        print(f"[WS] 错误: {type(e).__name__}: {e}")
    finally:
        manager.disconnect(websocket)
        print(f"[WS] Cleanup done, active connections: {len(manager.active_connections)}")


@router.websocket("/ws/status")
async def websocket_status(websocket: WebSocket):
    """WebSocket status stream"""
    await websocket.accept()

    try:
        while True:
            # Send status every second
            status = crawler_manager.get_status()
            await websocket.send_json(status)
            await asyncio.sleep(1)
    except WebSocketDisconnect:
        pass
    except Exception:
        pass
