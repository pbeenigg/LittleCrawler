# -*- coding: utf-8 -*-
"""
爬虫相关数据模型

定义爬虫API所需的请求和响应模型，包括：
- 平台枚举、登录类型、爬虫类型
- 爬虫启动请求、状态响应
- 日志条目、文件信息
"""

from enum import Enum
from typing import Optional, Literal
from pydantic import BaseModel


class PlatformEnum(str, Enum):
    """支持的平台枚举"""
    XHS = "xhs"      # 小红书
    ZHIHU = "zhihu"  # 知乎


class LoginTypeEnum(str, Enum):
    """登录方式枚举"""
    QRCODE = "qrcode"  # 二维码登录
    PHONE = "phone"    # 手机号登录
    COOKIE = "cookie"  # Cookie登录


class CrawlerTypeEnum(str, Enum):
    """爬虫类型枚举"""
    SEARCH = "search"    # 搜索模式
    DETAIL = "detail"    # 详情模式
    CREATOR = "creator"  # 创作者模式


class SaveDataOptionEnum(str, Enum):
    """数据存储方式枚举"""
    CSV = "csv"
    DB = "db"
    JSON = "json"
    SQLITE = "sqlite"
    MONGODB = "mongodb"
    EXCEL = "excel"


class CrawlerStartRequest(BaseModel):
    """爬虫启动请求模型"""
    platform: PlatformEnum  # 目标平台
    login_type: LoginTypeEnum = LoginTypeEnum.QRCODE  # 登录方式
    crawler_type: CrawlerTypeEnum = CrawlerTypeEnum.SEARCH  # 爬虫类型
    keywords: str = ""  # 搜索关键词（search模式）
    specified_ids: str = ""  # 指定ID列表（detail模式），逗号分隔
    creator_ids: str = ""  # 创作者ID列表（creator模式），逗号分隔
    start_page: int = 1  # 起始页码
    max_pages: Optional[int] = None  # 最大页数，None表示无限制
    enable_comments: bool = True  # 是否爬取评论
    enable_sub_comments: bool = False  # 是否爬取子评论
    save_option: SaveDataOptionEnum = SaveDataOptionEnum.JSON  # 存储方式
    cookies: str = ""  # Cookie字符串（cookie登录时使用）
    headless: bool = False  # 是否无头模式


class CrawlerStatusResponse(BaseModel):
    """爬虫状态响应模型"""
    status: Literal["idle", "running", "stopping", "error"]  # 状态
    platform: Optional[str] = None  # 当前平台
    crawler_type: Optional[str] = None  # 当前爬虫类型
    started_at: Optional[str] = None  # 启动时间
    error_message: Optional[str] = None  # 错误信息


class LogEntry(BaseModel):
    """日志条目模型"""
    id: int  # 日志ID
    timestamp: str  # 时间戳
    level: Literal["info", "warning", "error", "success", "debug"]  # 日志级别
    message: str  # 日志内容


class DataFileInfo(BaseModel):
    """数据文件信息模型"""
    name: str  # 文件名
    path: str  # 相对路径
    size: int  # 文件大小（字节）
    modified_at: str  # 修改时间
    record_count: Optional[int] = None  # 记录数
