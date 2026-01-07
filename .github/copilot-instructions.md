# LittleCrawler Copilot Instructions

## 项目概述

基于 Python 异步编程的多平台社交媒体爬虫框架（Python >=3.11），支持 xhs | zhihu。

## 核心架构

### 双工厂模式

```
main.py::CrawlerFactory.CRAWLERS      → 平台爬虫注册 {"xhs": XiaoHongShuCrawler, ...}
store/{platform}/__init__.py::*StoreFactory → 存储实现注册 {"csv": ..., "db": ..., "json": ...}
```

### 抽象基类体系 ([base/base_crawler.py](base/base_crawler.py))

| 基类                | 必须实现                                                                  |
| ------------------- | ------------------------------------------------------------------------- |
| `AbstractCrawler`   | `start()`, `search()`, `launch_browser()`                                 |
| `AbstractLogin`     | `begin()`, `login_by_qrcode()`, `login_by_mobile()`, `login_by_cookies()` |
| `AbstractStore`     | `store_content()`, `store_comment()`, `store_creator()`                   |
| `AbstractApiClient` | `request()`, `update_cookies()`                                           |

### 平台模块结构 (`infra/{platform}/`)

```
core.py      # 继承 AbstractCrawler，入口 start() 方法
client.py    # 继承 AbstractApiClient + ProxyRefreshMixin，处理 API 请求
login.py     # 继承 AbstractLogin，实现多种登录方式
field.py     # 平台枚举定义（SearchSortType 等）
help.py      # 辅助函数（URL 解析、签名等）
```

## 关键模式

### 代理自动刷新

API 客户端继承 `ProxyRefreshMixin`，**每次请求前**调用：

```python
await self._refresh_proxy_if_expired()  # 自动检测并刷新过期代理
```

### 上下文变量传递 ([var.py](var.py))

```python
crawler_type_var.set(config.CRAWLER_TYPE)  # 设置爬虫类型
source_keyword_var.set(keyword)            # 设置搜索关键词
# AsyncFileWriter 会读取这些变量决定输出文件路径
```

### CDP 浏览器模式

启用 `config.ENABLE_CDP_MODE=True` 时，使用真实浏览器环境降低检测风险：

```python
# core.py 中根据配置选择模式
if config.ENABLE_CDP_MODE:
    self.browser_context = await self.launch_browser_with_cdp(...)
else:
    await self.browser_context.add_init_script(path="libs/stealth.min.js")
```

## 配置系统 ([config/base_config.py](config/base_config.py))

关键配置项：`PLATFORM`, `CRAWLER_TYPE` (search|detail|creator), `LOGIN_TYPE` (qrcode|phone|cookie), `SAVE_DATA_OPTION` (csv|db|json|sqlite|mongodb|excel), `ENABLE_CDP_MODE`, `ENABLE_IP_PROXY`

## 数据流

```
爬虫 → store/{platform}/__init__.py::update_*_data() → StoreFactory.create_store() → 具体存储实现
```

存储实现位于 `store/{platform}/_store_impl.py`，每种存储类型（CSV/DB/JSON/SQLite/MongoDB/Excel）独立实现。

## 开发命令

```bash
uv sync                                    # 安装依赖
python main.py                             # 运行（使用 config 默认值）
python main.py --platform xhs --type search  # 指定平台和类型
python main.py --init-db sqlite            # 初始化数据库
pytest test/                               # 运行测试
```

## 添加新平台清单

1. `infra/{platform}/` — core.py, client.py, login.py, field.py
2. `store/{platform}/` — `__init__.py` (StoreFactory) + `_store_impl.py` (6 种存储实现)
3. `database/models.py` — SQLAlchemy ORM 模型
4. `model/m_{platform}.py` — Pydantic 数据模型
5. `main.py::CrawlerFactory.CRAWLERS` — 注册爬虫类

## 注意事项

- **全异步**：所有 I/O 操作使用 `async/await`
- **日志**：使用 `tools.utils.logger`
- **请求重试**：使用 `tenacity` 装饰器 `@retry(stop=stop_after_attempt(3), wait=wait_fixed(1))`
- **数据去重**：DB 存储模式内置去重（基于 note_id）
