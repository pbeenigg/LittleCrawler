# -*- coding: utf-8 -*-
"""
LittleCrawler WebUI API 服务

提供爬虫控制、数据管理、用户认证等功能的RESTful API

启动命令:
  # 完整服务（API + 前端页面）
  uv run uvicorn api.main:app --port 8080 --reload

  # 仅 API 服务（不含前端页面）
  API_ONLY=1 uv run uvicorn api.main:app --port 8080 --reload

默认账号: admin / admin123
"""
import asyncio
import os
import subprocess
import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

from .routers import auth_router, crawler_router, data_router, websocket_router
from .services.auth_service import init_user_db

# 检查是否仅启动 API（不含前端）
API_ONLY = os.environ.get("API_ONLY", "").lower() in ("1", "true", "yes")

app = FastAPI(
    title="LittleCrawler API",
    description="多平台社交媒体爬虫控制API - 支持小红书、知乎",
    version="1.0.0"
)

# Get webui static files directory
WEBUI_DIR = os.path.join(os.path.dirname(__file__), "ui")

# CORS configuration - allow frontend dev server access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 允许所有来源（生产环境应限制）
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 注册路由
app.include_router(auth_router, prefix="/api")
app.include_router(crawler_router, prefix="/api")
app.include_router(data_router, prefix="/api")
app.include_router(websocket_router, prefix="/api")

# 初始化用户数据库（创建默认admin账号）
init_user_db()


@app.get("/")
async def serve_frontend():
    """Return frontend page or API info"""
    if API_ONLY:
        return {
            "message": "LittleCrawler API",
            "version": "1.0.0",
            "docs": "/docs",
            "mode": "API only (no frontend)"
        }
    index_path = os.path.join(WEBUI_DIR, "index.html")
    if os.path.exists(index_path):
        return FileResponse(index_path)
    return {
        "message": "LittleCrawler WebUI API",
        "version": "1.0.0",
        "docs": "/docs",
        "note": "WebUI not found, please build it first: cd web && npm run build"
    }


@app.get("/api/health")
async def health_check():
    """
    健康检查接口
    返回API状态、时间戳和版本号
    """
    from datetime import datetime
    return {
        "status": "ok",
        "timestamp": datetime.now().isoformat(),
        "version": "v1.0.0"
    }


@app.get("/api/env/check")
async def check_environment():
    """Check if LittleCrawler environment is configured correctly"""
    try:
        # Run uv run main.py --help command to check environment
        process = await asyncio.create_subprocess_exec(
            "uv", "run", "main.py", "--help",
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            cwd="."  # Project root directory
        )
        stdout, stderr = await asyncio.wait_for(
            process.communicate(),
            timeout=30.0  # 30 seconds timeout
        )

        if process.returncode == 0:
            return {
                "success": True,
                "message": "LittleCrawler environment configured correctly",
                "output": stdout.decode("utf-8", errors="ignore")[:500]  # Truncate to first 500 characters
            }
        else:
            error_msg = stderr.decode("utf-8", errors="ignore") or stdout.decode("utf-8", errors="ignore")
            return {
                "success": False,
                "message": "Environment check failed",
                "error": error_msg[:500]
            }
    except asyncio.TimeoutError:
        return {
            "success": False,
            "message": "Environment check timeout",
            "error": "Command execution exceeded 30 seconds"
        }
    except FileNotFoundError:
        return {
            "success": False,
            "message": "uv command not found",
            "error": "Please ensure uv is installed and configured in system PATH"
        }
    except Exception as e:
        return {
            "success": False,
            "message": "Environment check error",
            "error": str(e)
        }


@app.get("/api/config/platforms")
async def get_platforms():
    """Get list of supported platforms"""
    return {
        "platforms": [
            {"value": "xhs", "label": "小红书", "icon": "book-open"},
            {"value": "xhy", "label": "小黄鱼", "icon": "messages-square"},
            {"value": "zhihu", "label": "知乎", "icon": "help-circle"},
        ]
    }


@app.get("/api/config/options")
async def get_config_options():
    """Get all configuration options"""
    return {
        "login_types": [
            {"value": "qrcode", "label": "QR Code Login"},
            {"value": "cookie", "label": "Cookie Login"},
        ],
        "crawler_types": [
            {"value": "search", "label": "Search Mode"},
            {"value": "detail", "label": "Detail Mode"},
            {"value": "creator", "label": "Creator Mode"},
        ],
        "save_options": [
            {"value": "json", "label": "JSON File"},
            {"value": "csv", "label": "CSV File"},
            {"value": "excel", "label": "Excel File"},
            {"value": "sqlite", "label": "SQLite Database"},
            {"value": "db", "label": "MySQL Database"},
            {"value": "mongodb", "label": "MongoDB Database"},
        ],
    }


# Mount static resources - must be placed after all routes
# 仅在非 API_ONLY 模式下挂载静态资源
if not API_ONLY and os.path.exists(WEBUI_DIR):
    # Mount _next directory for Next.js static assets
    next_dir = os.path.join(WEBUI_DIR, "_next")
    if os.path.exists(next_dir):
        app.mount("/_next", StaticFiles(directory=next_dir), name="next-static")
    
    # Mount assets directory
    assets_dir = os.path.join(WEBUI_DIR, "assets")
    if os.path.exists(assets_dir):
        app.mount("/assets", StaticFiles(directory=assets_dir), name="assets")
    
    # Mount logos directory
    logos_dir = os.path.join(WEBUI_DIR, "logos")
    if os.path.exists(logos_dir):
        app.mount("/logos", StaticFiles(directory=logos_dir), name="logos")


# Catch-all route for SPA - must be at the very end
@app.get("/{full_path:path}")
async def serve_spa(full_path: str):
    """
    SPA 路由处理
    对于非API请求，返回对应的HTML页面或index.html
    API_ONLY 模式下直接返回 404
    """
    # Skip API routes
    if full_path.startswith("api/"):
        return {"error": "Not found"}
    
    # API_ONLY 模式下不提供前端页面
    if API_ONLY:
        return {"error": "Not found", "mode": "API only"}
    
    # Try to serve the specific page
    page_path = os.path.join(WEBUI_DIR, full_path, "index.html")
    if os.path.exists(page_path):
        return FileResponse(page_path)
    
    # Fallback to main index.html
    index_path = os.path.join(WEBUI_DIR, "index.html")
    if os.path.exists(index_path):
        return FileResponse(index_path)
    
    return {
        "message": "LittleCrawler API",
        "version": "v1.0.0",
        "docs": "/docs",
        "note": "前端页面未构建，请先运行: cd web && npm install && npm run build"
    }


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8080)
