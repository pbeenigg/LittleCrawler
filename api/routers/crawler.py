# -*- coding: utf-8 -*-
"""
爬虫控制路由模块

提供爬虫任务管理的API端点：
- POST /crawler/start - 启动爬虫任务
- POST /crawler/stop - 停止爬虫任务  
- GET /crawler/status - 获取爬虫状态
- GET /crawler/logs - 获取运行日志

所有接口需要Bearer Token认证
"""

from fastapi import APIRouter, HTTPException, Depends

from ..schemas import CrawlerStartRequest, CrawlerStatusResponse
from ..services import crawler_manager
from .auth import get_current_user

router = APIRouter(prefix="/crawler", tags=["爬虫控制"])


@router.post("/start", summary="启动爬虫")
async def start_crawler(
    request: CrawlerStartRequest,
    current_user: dict = Depends(get_current_user)
):
    """
    启动爬虫任务
    
    - **platform**: 目标平台 (xhs/zhihu)
    - **crawler_type**: 爬取类型 (search/detail/creator)
    - **keywords**: 搜索关键词（search模式）
    """
    success = await crawler_manager.start(request)
    if not success:
        # 处理并发/重复请求：如果进程已在运行，返回400而非500
        if crawler_manager.process and crawler_manager.process.poll() is None:
            raise HTTPException(status_code=400, detail="爬虫已在运行中")
        raise HTTPException(status_code=500, detail="启动爬虫失败")

    return {"status": "ok", "message": "爬虫启动成功"}


@router.post("/stop", summary="停止爬虫")
async def stop_crawler(current_user: dict = Depends(get_current_user)):
    """
    停止当前运行的爬虫任务
    
    发送SIGTERM信号，等待15秒后强制终止
    """
    success = await crawler_manager.stop()
    if not success:
        # 处理并发/重复请求：如果进程已退出/不存在，返回400而非500
        if not crawler_manager.process or crawler_manager.process.poll() is not None:
            raise HTTPException(status_code=400, detail="没有正在运行的爬虫")
        raise HTTPException(status_code=500, detail="停止爬虫失败")

    return {"status": "ok", "message": "爬虫已停止"}


@router.get("/status", response_model=CrawlerStatusResponse, summary="获取状态")
async def get_crawler_status(current_user: dict = Depends(get_current_user)):
    """
    获取爬虫当前运行状态
    
    返回状态、平台、类型、启动时间等信息
    """
    return crawler_manager.get_status()


@router.get("/logs", summary="获取日志")
async def get_logs(limit: int = 100, current_user: dict = Depends(get_current_user)):
    """
    获取最近的运行日志
    
    - **limit**: 返回日志条数，默认100条
    """
    logs = crawler_manager.logs[-limit:] if limit > 0 else crawler_manager.logs
    return {"logs": [log.model_dump() for log in logs]}
