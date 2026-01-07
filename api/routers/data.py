# -*- coding: utf-8 -*-
"""
数据管理路由模块

提供爬取数据文件管理的API端点：
- GET /data/files - 获取数据文件列表
- GET /data/files/{path} - 预览文件内容
- GET /data/download/{path} - 下载文件
- GET /data/stats - 获取数据统计

所有接口需要Bearer Token认证
"""

import os
import json
from pathlib import Path
from typing import Optional

from fastapi import APIRouter, HTTPException, Depends
from fastapi.responses import FileResponse

from .auth import get_current_user

router = APIRouter(prefix="/data", tags=["数据管理"])

# 数据存储目录
DATA_DIR = Path(__file__).parent.parent.parent / "data"


def get_file_info(file_path: Path) -> dict:
    """
    获取文件信息
    
    解析文件元数据，包括大小、修改时间、记录数等
    """
    stat = file_path.stat()
    record_count = None

    # 尝试获取记录数
    try:
        if file_path.suffix == ".json":
            with open(file_path, "r", encoding="utf-8") as f:
                data = json.load(f)
                if isinstance(data, list):
                    record_count = len(data)
        elif file_path.suffix == ".csv":
            with open(file_path, "r", encoding="utf-8") as f:
                record_count = sum(1 for _ in f) - 1  # 减去表头行
    except Exception:
        pass

    return {
        "name": file_path.name,
        "path": str(file_path.relative_to(DATA_DIR)),
        "size": stat.st_size,
        "modified_at": stat.st_mtime,
        "record_count": record_count,
        "type": file_path.suffix[1:] if file_path.suffix else "unknown"
    }


@router.get("/files", summary="获取文件列表")
async def list_data_files(
    platform: Optional[str] = None,
    file_type: Optional[str] = None,
    current_user: dict = Depends(get_current_user)
):
    """
    获取数据文件列表
    
    - **platform**: 平台过滤 (xhs/zhihu/xhy)
    - **file_type**: 文件类型过滤 (json/csv/xlsx)
    """
    if not DATA_DIR.exists():
        return {"files": []}

    files = []
    supported_extensions = {".json", ".csv", ".xlsx", ".xls"}

    for root, dirs, filenames in os.walk(DATA_DIR):
        root_path = Path(root)
        for filename in filenames:
            file_path = root_path / filename
            if file_path.suffix.lower() not in supported_extensions:
                continue

            # 平台过滤
            if platform:
                rel_path = str(file_path.relative_to(DATA_DIR))
                if platform.lower() not in rel_path.lower():
                    continue

            # 类型过滤
            if file_type and file_path.suffix[1:].lower() != file_type.lower():
                continue

            try:
                files.append(get_file_info(file_path))
            except Exception:
                continue

    # 按修改时间排序（最新在前）
    files.sort(key=lambda x: x["modified_at"], reverse=True)

    return {"files": files}


@router.get("/files/{file_path:path}", summary="预览文件内容")
async def get_file_content(
    file_path: str,
    preview: bool = True,
    limit: int = 100,
    current_user: dict = Depends(get_current_user)
):
    """
    获取文件内容或预览
    
    - **file_path**: 文件相对路径
    - **preview**: 是否预览模式，默认True
    - **limit**: 预览记录数，默认100
    """
    full_path = DATA_DIR / file_path

    if not full_path.exists():
        raise HTTPException(status_code=404, detail="文件不存在")

    if not full_path.is_file():
        raise HTTPException(status_code=400, detail="不是有效文件")

    # 安全检查：确保在DATA_DIR内
    try:
        full_path.resolve().relative_to(DATA_DIR.resolve())
    except ValueError:
        raise HTTPException(status_code=403, detail="访问被拒绝")

    if preview:
        # 返回预览数据
        try:
            if full_path.suffix == ".json":
                with open(full_path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    if isinstance(data, list):
                        # 取最后 limit 条并倒序返回（最新的在前）
                        latest_data = data[-limit:] if len(data) > limit else data
                        latest_data = list(reversed(latest_data))
                        return {"data": latest_data, "total": len(data)}
                    return {"data": data, "total": 1}
            elif full_path.suffix == ".csv":
                import csv
                with open(full_path, "r", encoding="utf-8") as f:
                    reader = csv.DictReader(f)
                    rows = []
                    for i, row in enumerate(reader):
                        if i >= limit:
                            break
                        rows.append(row)
                    # 重新读取获取总数
                    f.seek(0)
                    total = sum(1 for _ in f) - 1
                    return {"data": rows, "total": total}
            elif full_path.suffix.lower() in (".xlsx", ".xls"):
                import pandas as pd
                # 读取前limit行
                df = pd.read_excel(full_path, nrows=limit)
                # 获取总行数（只读第一列节省内存）
                df_count = pd.read_excel(full_path, usecols=[0])
                total = len(df_count)
                # 转换为字典列表，处理NaN值
                rows = df.where(pd.notnull(df), None).to_dict(orient='records')
                return {
                    "data": rows,
                    "total": total,
                    "columns": list(df.columns)
                }
            else:
                raise HTTPException(status_code=400, detail="不支持预览该文件类型")
        except json.JSONDecodeError:
            raise HTTPException(status_code=400, detail="无效的JSON文件")
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
    else:
        # 返回文件下载
        return FileResponse(
            path=full_path,
            filename=full_path.name,
            media_type="application/octet-stream"
        )


@router.get("/download/{file_path:path}", summary="下载文件")
async def download_file(
    file_path: str,
    current_user: dict = Depends(get_current_user)
):
    """
    下载数据文件
    
    - **file_path**: 文件相对路径
    """
    full_path = DATA_DIR / file_path

    if not full_path.exists():
        raise HTTPException(status_code=404, detail="文件不存在")

    if not full_path.is_file():
        raise HTTPException(status_code=400, detail="不是有效文件")

    # 安全检查
    try:
        full_path.resolve().relative_to(DATA_DIR.resolve())
    except ValueError:
        raise HTTPException(status_code=403, detail="访问被拒绝")

    return FileResponse(
        path=full_path,
        filename=full_path.name,
        media_type="application/octet-stream"
    )


@router.get("/stats", summary="数据统计")
async def get_data_stats(current_user: dict = Depends(get_current_user)):
    """
    获取数据文件统计信息
    
    返回文件总数、总大小、按平台和类型的分布
    """
    if not DATA_DIR.exists():
        return {"total_files": 0, "total_size": 0, "by_platform": {}, "by_type": {}}

    stats = {
        "total_files": 0,
        "total_size": 0,
        "by_platform": {},
        "by_type": {}
    }

    supported_extensions = {".json", ".csv", ".xlsx", ".xls"}

    for root, dirs, filenames in os.walk(DATA_DIR):
        root_path = Path(root)
        for filename in filenames:
            file_path = root_path / filename
            if file_path.suffix.lower() not in supported_extensions:
                continue

            try:
                stat = file_path.stat()
                stats["total_files"] += 1
                stats["total_size"] += stat.st_size

                # 按类型统计
                file_type = file_path.suffix[1:].lower()
                stats["by_type"][file_type] = stats["by_type"].get(file_type, 0) + 1

                # 按平台统计（从路径推断）
                rel_path = str(file_path.relative_to(DATA_DIR))
                for platform in ["xhs", "zhihu", "xhy"]:
                    if platform in rel_path.lower():
                        stats["by_platform"][platform] = stats["by_platform"].get(platform, 0) + 1
                        break
            except Exception:
                continue

    return stats
