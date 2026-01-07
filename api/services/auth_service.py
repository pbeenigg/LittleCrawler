# -*- coding: utf-8 -*-
"""
认证服务模块

提供用户认证相关功能，包括：
- SQLite用户数据库管理
- 密码哈希与验证
- JWT Token生成与验证
- 用户CRUD操作
"""

import os
import sqlite3
import hashlib
import secrets
from datetime import datetime, timedelta
from typing import Optional
from pathlib import Path

# JWT配置
SECRET_KEY = os.getenv("JWT_SECRET_KEY", secrets.token_hex(32))
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24  # 24小时

# 数据库路径
DB_PATH = Path(__file__).parent.parent.parent / "database" / "users.db"


def _get_db_connection() -> sqlite3.Connection:
    """获取数据库连接"""
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(str(DB_PATH))
    conn.row_factory = sqlite3.Row
    return conn


def init_user_db():
    """
    初始化用户数据库
    
    创建users表并插入默认管理员账号 admin/admin123
    """
    conn = _get_db_connection()
    cursor = conn.cursor()
    
    # 创建用户表
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            is_active INTEGER DEFAULT 1,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP,
            updated_at TEXT DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    # 检查是否存在admin用户，不存在则创建
    cursor.execute("SELECT id FROM users WHERE username = ?", ("admin",))
    if not cursor.fetchone():
        password_hash = hash_password("admin123")
        cursor.execute(
            "INSERT INTO users (username, password_hash) VALUES (?, ?)",
            ("admin", password_hash)
        )
        print("[Auth] 已创建默认管理员账号: admin / admin123")
    
    conn.commit()
    conn.close()


def hash_password(password: str) -> str:
    """
    密码哈希
    
    使用SHA256 + 盐值对密码进行哈希处理
    """
    salt = "littlecrawler_salt_2026"
    return hashlib.sha256(f"{password}{salt}".encode()).hexdigest()


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """验证密码"""
    return hash_password(plain_password) == hashed_password


def authenticate_user(username: str, password: str) -> Optional[dict]:
    """
    用户认证
    
    验证用户名和密码，返回用户信息或None
    """
    conn = _get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute(
        "SELECT id, username, password_hash, is_active FROM users WHERE username = ?",
        (username,)
    )
    row = cursor.fetchone()
    conn.close()
    
    if not row:
        print(f"[Auth] 用户不存在: {username}")
        return None
    
    input_hash = hash_password(password)
    stored_hash = row["password_hash"]
    print(f"[Auth] 密码验证: input_hash={input_hash[:20]}... stored_hash={stored_hash[:20]}...")
    
    if not verify_password(password, stored_hash):
        print(f"[Auth] 密码不匹配")
        return None
    
    if not row["is_active"]:
        print(f"[Auth] 用户已禁用")
        return None
    
    return {
        "id": row["id"],
        "username": row["username"],
        "is_active": bool(row["is_active"])
    }


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """
    创建访问Token
    
    使用简单的base64编码 + 签名方式生成Token
    """
    import base64
    import json
    import hmac
    
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire.isoformat()})
    
    # 编码payload
    payload = base64.urlsafe_b64encode(json.dumps(to_encode).encode()).decode()
    
    # 生成签名
    signature = hmac.new(
        SECRET_KEY.encode(),
        payload.encode(),
        hashlib.sha256
    ).hexdigest()[:32]
    
    return f"{payload}.{signature}"


def verify_token(token: str) -> Optional[dict]:
    """
    验证Token
    
    解析并验证Token，返回payload或None
    """
    import base64
    import json
    import hmac
    
    try:
        parts = token.split(".")
        if len(parts) != 2:
            return None
        
        payload_b64, signature = parts
        
        # 验证签名
        expected_signature = hmac.new(
            SECRET_KEY.encode(),
            payload_b64.encode(),
            hashlib.sha256
        ).hexdigest()[:32]
        
        if signature != expected_signature:
            return None
        
        # 解码payload
        payload = json.loads(base64.urlsafe_b64decode(payload_b64.encode()))
        
        # 验证过期时间
        exp = datetime.fromisoformat(payload["exp"])
        if datetime.utcnow() > exp:
            return None
        
        return payload
    except Exception:
        return None


def get_user_by_id(user_id: int) -> Optional[dict]:
    """根据ID获取用户信息"""
    conn = _get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute(
        "SELECT id, username, is_active FROM users WHERE id = ?",
        (user_id,)
    )
    row = cursor.fetchone()
    conn.close()
    
    if not row:
        return None
    
    return {
        "id": row["id"],
        "username": row["username"],
        "is_active": bool(row["is_active"])
    }


def create_user(username: str, password: str) -> Optional[dict]:
    """
    创建新用户
    
    返回创建的用户信息或None（用户名已存在）
    """
    conn = _get_db_connection()
    cursor = conn.cursor()
    
    try:
        password_hash = hash_password(password)
        cursor.execute(
            "INSERT INTO users (username, password_hash) VALUES (?, ?)",
            (username, password_hash)
        )
        conn.commit()
        user_id = cursor.lastrowid
        conn.close()
        
        return {
            "id": user_id,
            "username": username,
            "is_active": True
        }
    except sqlite3.IntegrityError:
        conn.close()
        return None


# 启动时初始化数据库
init_user_db()
