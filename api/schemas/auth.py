# -*- coding: utf-8 -*-
"""
认证相关数据模型

定义用户认证所需的请求和响应模型，包括登录请求、Token响应等。
"""

from typing import Optional
from pydantic import BaseModel


class UserLogin(BaseModel):
    """用户登录请求模型"""
    username: str  # 用户名
    password: str  # 密码


class Token(BaseModel):
    """Token响应模型"""
    access_token: str  # 访问令牌
    token_type: str = "bearer"  # 令牌类型


class UserInfo(BaseModel):
    """用户信息模型"""
    id: int  # 用户ID
    username: str  # 用户名
    is_active: bool = True  # 是否激活


class UserCreate(BaseModel):
    """创建用户请求模型"""
    username: str  # 用户名
    password: str  # 密码
