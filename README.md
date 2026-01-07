# LittleCrawler

基于 Python 异步编程的多平台社交媒体爬虫框架。

## 支持平台

| 平台   | 代号    | 功能                   |
| ------ | ------- | ---------------------- |
| 小红书 | `xhs`   | 笔记搜索、详情、创作者 |
| 知乎   | `zhihu` | 问答搜索、详情、答主   |

## 快速开始

### 环境要求

- Python >= 3.11
- [uv](https://github.com/astral-sh/uv) (推荐) 或 pip

### 安装

```bash
# 克隆项目
git clone https://github.com/pbeenig/LittleCrawler.git
cd LittleCrawler

# 安装依赖
uv sync
# 或
pip install -r requirements.txt

# 安装浏览器
playwright install chromium
```

### 运行

```bash
# 默认运行（使用 config/base_config.py 配置）
python main.py

# 指定平台和爬虫类型
python main.py --platform xhs --type search

# 初始化数据库
python main.py --init-db sqlite
```

### Web

```bash

## Step 1:  编译前端页面 到  `api/ui` 目录下
cd ./web &&  npm run build

## Step 2:  启动 完整服务（API + 前端页面）
uv run uvicorn api.main:app --port 8080 --reload

## Step 3： 访问 `http://127.0.0.1:8080`



## Step 1:  启动仅 API 服务（不含前端页面）
API_ONLY=1 uv run uvicorn api.main:app --port 8080 --reload


## Step 2:  开发模式启动 Web 后台
cd ./web &&  npm run dev

## Step 3： 访问 `http://127.0.0.1:8080`

```

### 命令工具

```bash

## 清除 缓存数据  (node_modules|.venv|.git|.next|out|browser_data|data|.codacy )
find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null; tree -L 2 -d --noreport -I 'node_modules|.venv|.git|.next|out|browser_data|data|.codacy'

##
uv run python main.py --help


```

## 配置说明

编辑 `config/base_config.py`：

```python
PLATFORM = "xhs"           # 目标平台
KEYWORDS = "关键词1,关键词2" # 搜索关键词
CRAWLER_TYPE = "search"    # search | detail | creator
LOGIN_TYPE = "qrcode"      # qrcode | phone | cookie
SAVE_DATA_OPTION = "json"  # csv | json | db | sqlite | mongodb | excel
ENABLE_CDP_MODE = True     # CDP模式（推荐，反检测更强）
ENABLE_IP_PROXY = False    # 是否启用代理
```

## 项目结构

```
├── main.py                  # 程序入口
├── config/                  # 配置文件
├── src/                     # 核心源码
│   ├── core/                # 核心模块（基类、命令行、上下文变量）
│   ├── platforms/           # 平台爬虫实现
│   │   ├── xhs/             # 小红书爬虫
│   │   └── zhihu/           # 知乎爬虫
│   ├── storage/             # 数据存储层
│   │   ├── base/            # 通用存储（DB、Excel、MongoDB）
│   │   ├── xhs/             # 小红书存储实现
│   │   └── zhihu/           # 知乎存储实现
│   ├── models/              # Pydantic 数据模型
│   ├── services/            # 服务层
│   │   ├── cache/           # 缓存（本地/Redis）
│   │   └── proxy/           # 代理IP管理
│   └── utils/               # 工具函数
├── api/                     # Web API 后台
├── web/                     # 前端界面
├── tests/                   # 测试用例
├── docs/                    # 文档
├── data/                    # 数据输出
└── libs/                    # 第三方依赖（JS）
```

## 数据存储

| 方式    | 配置值    | 说明       |
| ------- | --------- | ---------- |
| CSV     | `csv`     | 简单通用   |
| JSON    | `json`    | 结构完整   |
| SQLite  | `sqlite`  | 轻量本地   |
| MySQL   | `db`      | 生产环境   |
| MongoDB | `mongodb` | 灵活扩展   |
| Excel   | `excel`   | 可视化分析 |

## License

MIT
