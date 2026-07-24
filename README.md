# LittleCrawler

<p align="center">
  <b>基于 Python 异步编程的多平台社交媒体爬虫框架</b>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.11+-3776AB?style=flat-square&logo=python&logoColor=white" alt="Python">
  <img src="https://img.shields.io/badge/Playwright-1.45+-2EAD33?style=flat-square&logo=playwright&logoColor=white" alt="Playwright">
  <img src="https://img.shields.io/badge/FastAPI-0.115+-009688?style=flat-square&logo=fastapi&logoColor=white" alt="FastAPI">
  <img src="https://img.shields.io/badge/Next.js-14+-000000?style=flat-square&logo=next.js&logoColor=white" alt="Next.js">
  <img src="https://img.shields.io/badge/NextUI-2.0+-000000?style=flat-square&logo=nextui&logoColor=white" alt="NextUI">
  <img src="https://img.shields.io/badge/License-MIT-blue?style=flat-square" alt="License">
</p>

<p align="center">
  <img src="https://img.shields.io/badge/小红书-FF2442?style=flat-square&logo=xiaohongshu&logoColor=white" alt="小红书">
  <img src="https://img.shields.io/badge/知乎-0084FF?style=flat-square&logo=zhihu&logoColor=white" alt="知乎">
  <img src="https://img.shields.io/badge/小黄鱼-FFD700?style=flat-square&logo=firefish&logoColor=black" alt="小黄鱼,闲鱼">
</p>

---

## 🌐 支持平台

| 平台   | 代号    | 功能             |
| ------ | ------- | ---------------- |
| 小红书 | `xhs`   | 笔记、详情、作者 |
| 小黄鱼 | `xhy`   | 商品、笔记、作者 |
| 知乎   | `zhihu` | 文章、详情、作者 |

## 🚀 快速开始

### 📦 环境要求

- Python >= 3.11
- [uv](https://github.com/astral-sh/uv) (推荐) 或 pip

### 📥 安装

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

### ▶️ 运行

```bash
# 默认运行（使用 config/base_config.py 配置）
python main.py

# 指定平台和爬虫类型
python main.py --platform xhs --type search

# 初始化数据库
python main.py --init-db sqlite
```

### 🖥️ Web 后台

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

## 📸 界面预览

<table>
  <tr>
    <td align="center"><b>🔐 登录</b></td>
    <td align="center"><b>🚀 启动</b></td>
  </tr>
  <tr>
    <td><img src="docs/images/login.jpg" width="400" alt="登录"></td>
    <td><img src="docs/images/run.jpg" width="400" alt="状态"></td>
  </tr>
  <tr>
    <td align="center" colspan="2"><b>📊 首页</b></td>
  </tr>
  <tr>
    <td colspan="2" align="center"><img src="docs/images/start1.jpg" width="700" alt="运行状态"></td>
  </tr>
</table>

### 🛠️ 命令工具

```bash

## 清除 缓存数据  (node_modules|.venv|.git|.next|out|browser_data|data|.codacy )
find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null; tree -L 2 -d --noreport -I 'node_modules|.venv|.git|.next|out|browser_data|data|.codacy'

##
uv run python main.py --help


```

## ⚙️ 配置说明

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

## 📁 项目结构

```
├── main.py                  # 程序入口
├── config/                  # 配置文件
├── src/                     # 核心源码
│   ├── core/                # 核心模块（基类、命令行、上下文变量）
│   ├── platforms/           # 平台爬虫实现
│   │   ├── xhs/             # 小红书爬虫
│   │   ├── xhy/             # 小黄鱼爬虫
│   │   └── zhihu/           # 知乎爬虫
│   ├── storage/             # 数据存储层
│   │   ├── base/            # 通用存储（DB、Excel、MongoDB）
│   │   ├── xhs/             # 小红书存储实现
│   │   ├── xhy/             # 小黄鱼存储实现
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

## 💾 数据存储

| 方式    | 配置值    | 说明       |
| ------- | --------- | ---------- |
| CSV     | `csv`     | 简单通用   |
| JSON    | `json`    | 结构完整   |
| SQLite  | `sqlite`  | 轻量本地   |
| MySQL   | `db`      | 生产环境   |
| MongoDB | `mongodb` | 灵活扩展   |
| Excel   | `excel`   | 可视化分析 |

## 📄 License

MIT


## 🚀 赞助商

IPWO 提供全球住宅代理资源，为爬虫开发、数据采集和自动化任务提供更灵活的网络环境支持。
无论是项目测试、数据分析还是多地区访问需求，都可以根据业务场景选择合适的代理方案。

[访问IPWO](https://www.ipwo.net/?ref=githubpbeenigg)  




