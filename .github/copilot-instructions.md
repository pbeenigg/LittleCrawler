# LittleCrawler Copilot Instructions

## 项目概述

基于 Python 异步编程的多平台社交媒体爬虫框架（Python >=3.11），支持小红书 (xhs) 和知乎 (zhihu)。项目包含爬虫核心 + Web 管理后台。

## 项目结构

```
LittleCrawler/
├── main.py                 # 爬虫程序入口
├── config/                 # 配置文件
│   ├── base_config.py      # 基础配置（平台、登录方式、存储选项等）
│   ├── xhs_config.py       # 小红书特有配置
│   └── zhihu_config.py     # 知乎特有配置
├── src/                    # 核心源码
│   ├── core/               # 核心模块
│   │   ├── base_crawler.py # 抽象基类（AbstractCrawler, AbstractLogin, AbstractStore）
│   │   ├── arg.py          # 命令行参数解析
│   │   └── var.py          # 上下文变量（crawler_type_var, source_keyword_var）
│   ├── platforms/          # 平台实现
│   │   ├── xhs/            # 小红书爬虫
│   │   ├── xhy/            # 小黄鱼爬虫
│   │   └── zhihu/          # 知乎爬虫
│   ├── storage/            # 存储模块
│   │   ├── base/           # 数据库、Excel 基类、ORM 模型
│   │   ├── xhs/            # 小红书存储实现（6种：csv/db/json/sqlite/mongodb/excel）
│   │   ├── xhy/            # 小黄鱼存储实现（6种：csv/db/json/sqlite/mongodb/excel）
│   │   └── zhihu/          # 知乎存储实现
│   ├── models/             # Pydantic 数据模型
│   ├── services/           # 服务层
│   │   ├── cache/          # 缓存（本地/Redis）
│   │   └── proxy/          # 代理IP池
│   └── utils/              # 工具函数
├── api/                    # Web API 服务
│   ├── main.py             # FastAPI 入口
│   ├── routers/            # 路由（auth, crawler, data, websocket）
│   ├── services/           # API 业务逻辑
│   └── ui/                 # 前端静态文件（Next.js 构建产物）
├── web/                    # 前端源码（Next.js + NextUI）
├── libs/                   # 第三方库（stealth.min.js 等）
└── data/                   # 爬取数据输出目录
```

## 核心架构

### 双工厂模式

```python
# main.py - 平台爬虫注册
CrawlerFactory.CRAWLERS = {"xhs": XiaoHongShuCrawler, "zhihu": ZhihuCrawler}

# src/storage/{platform}/__init__.py - 存储实现注册
StoreFactory.STORES = {"csv": CsvStore, "db": DbStore, "json": JsonStore, ...}
```

### 抽象基类体系 ([src/core/base_crawler.py](src/core/base_crawler.py))

| 基类                | 必须实现的方法                                                            |
| ------------------- | ------------------------------------------------------------------------- |
| `AbstractCrawler`   | `start()`, `search()`, `launch_browser()`                                 |
| `AbstractLogin`     | `begin()`, `login_by_qrcode()`, `login_by_mobile()`, `login_by_cookies()` |
| `AbstractStore`     | `store_content()`, `store_comment()`, `store_creator()`                   |
| `AbstractApiClient` | `request()`, `update_cookies()`                                           |

### 平台模块结构 (`src/platforms/{platform}/`)

```
core.py      # 继承 AbstractCrawler，入口 start() 方法
client.py    # 继承 AbstractApiClient + ProxyRefreshMixin，处理 API 请求
login.py     # 继承 AbstractLogin，实现多种登录方式
field.py     # 平台枚举定义（SearchSortType 等）
help.py      # 辅助函数（URL 解析、签名等）
```

## 关键模式

### 代理自动刷新

API 客户端继承 `ProxyRefreshMixin`，每次请求前调用：

```python
await self._refresh_proxy_if_expired()  # 自动检测并刷新过期代理
```

### 上下文变量传递 ([src/core/var.py](src/core/var.py))

```python
crawler_type_var.set(config.CRAWLER_TYPE)  # 设置爬虫类型
source_keyword_var.set(keyword)            # 设置搜索关键词
# AsyncFileWriter 会读取这些变量决定输出文件路径
```

### CDP 浏览器模式

启用 `config.ENABLE_CDP_MODE=True` 时，使用真实浏览器环境降低检测风险：

```python
if config.ENABLE_CDP_MODE:
    self.browser_context = await self.launch_browser_with_cdp(...)
else:
    await self.browser_context.add_init_script(path="libs/stealth.min.js")
```

## 配置系统 ([config/base_config.py](config/base_config.py))

| 配置项             | 可选值                                            | 说明           |
| ------------------ | ------------------------------------------------- | -------------- |
| `PLATFORM`         | `xhs`, `zhihu`                                    | 目标平台       |
| `CRAWLER_TYPE`     | `search`, `detail`, `creator`                     | 爬取模式       |
| `LOGIN_TYPE`       | `qrcode`, `phone`, `cookie`                       | 登录方式       |
| `SAVE_DATA_OPTION` | `csv`, `db`, `json`, `sqlite`, `mongodb`, `excel` | 存储方式       |
| `ENABLE_CDP_MODE`  | `True`, `False`                                   | CDP 浏览器模式 |
| `ENABLE_IP_PROXY`  | `True`, `False`                                   | 是否启用代理   |

## 数据流

```
爬虫 → src/storage/{platform}/__init__.py::update_*_data() → StoreFactory.create_store() → 具体存储实现
```

## 开发命令

```bash
# 爬虫
uv sync                                      # 安装依赖
uv run python main.py                        # 运行（使用 config 默认值）
uv run python main.py --platform xhs --type search  # 指定平台和类型
uv run python main.py --init-db sqlite       # 初始化数据库

# Web 后台
uv run uvicorn api.main:app --port 8080 --reload        # 启动完整服务
API_ONLY=1 uv run uvicorn api.main:app --port 8080      # 仅启动 API

# 前端开发
cd web && npm run dev                        # 前端开发模式
cd web && npm run build                      # 构建前端到 api/ui/

# 测试
uv run pytest tests/
```

## Web API 接口

> 文档详见 [docs/API 文档.md](docs/API文档.md)

| 类别      | 路径           | 说明           | 认证 |
| --------- | -------------- | -------------- | ---- |
| 认证      | `/api/auth`    | 登录、登出     | ❌   |
| 爬虫控制  | `/api/crawler` | 启动、停止     | ✅   |
| 数据管理  | `/api/data`    | 文件列表、下载 | ✅   |
| WebSocket | `/api/ws`      | 实时日志推送   | ❌   |

默认账号: `admin` / `admin123`

## 添加新平台清单

1. `src/platforms/{platform}/` — core.py, client.py, login.py, field.py, help.py
2. `src/storage/{platform}/` — `__init__.py` (StoreFactory) + `_store_impl.py` (6 种存储)
3. `src/storage/base/models.py` — SQLAlchemy ORM 模型
4. `src/models/m_{platform}.py` — Pydantic 数据模型
5. `config/{platform}_config.py` — 平台特有配置
6. `main.py::CrawlerFactory.CRAWLERS` — 注册爬虫类

## 注意事项

- **全异步**：所有 I/O 操作使用 `async/await`
- **日志**：使用 `from src.utils.utils import logger`
- **请求重试**：使用 `tenacity` 装饰器 `@retry(stop=stop_after_attempt(3), wait=wait_fixed(1))`
- **数据去重**：DB 存储模式内置去重（基于 note_id）
- **导入路径**：核心代码统一使用 `from src.xxx import ...` 格式
