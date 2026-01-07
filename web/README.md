# LittleCrawler Web UI

基于 Next.js + NextUI 构建的爬虫管理后台。

## 技术栈

- **框架**: Next.js 14 (App Router)
- **UI 库**: NextUI v2
- **样式**: Tailwind CSS
- **状态管理**: React Context
- **图标**: Lucide React
- **主题**: next-themes (黑白主题切换)
- **国际化**: 自定义 i18n (中英文)

## 功能特性

1. **用户认证** - 登录/退出，JWT Token 认证
2. **主题切换** - 浅色/深色主题
3. **国际化** - 中文/英文界面
4. **仪表盘** - API 状态、系统概览
5. **爬虫管理** - 平台选择、配置、启动/停止
6. **数据管理** - 查看、搜索、导出数据
7. **实时日志** - WebSocket 日志控制台

## 开发

```bash
# 安装依赖
npm install

# 启动开发服务器
npm run dev

# 构建生产版本（输出到 ../api/ui）
npm run build
```

## 目录结构

```
web/
├── src/
│   ├── app/                    # Next.js App Router
│   │   ├── layout.tsx          # 根布局
│   │   ├── page.tsx            # 首页（重定向）
│   │   ├── providers.tsx       # 全局Providers
│   │   ├── globals.css         # 全局样式
│   │   ├── login/              # 登录页
│   │   └── dashboard/          # 仪表盘
│   │       ├── layout.tsx      # 仪表盘布局
│   │       ├── page.tsx        # 概览页
│   │       ├── crawler/        # 爬虫管理
│   │       ├── data/           # 数据管理
│   │       └── logs/           # 日志控制台
│   ├── components/             # 公共组件
│   │   ├── Sidebar.tsx         # 侧边导航
│   │   └── Header.tsx          # 顶部导航
│   ├── contexts/               # React Context
│   │   ├── AuthContext.tsx     # 认证上下文
│   │   └── I18nContext.tsx     # 国际化上下文
│   ├── lib/                    # 工具库
│   │   └── api.ts              # API客户端
│   ├── locales/                # 语言包
│   │   ├── zh.json             # 中文
│   │   └── en.json             # 英文
│   └── types/                  # TypeScript类型
│       └── index.ts
├── next.config.js              # Next.js配置
├── tailwind.config.ts          # Tailwind配置
├── tsconfig.json               # TypeScript配置
└── package.json
```

## 环境变量

创建 `.env.local` 文件:

```env
NEXT_PUBLIC_API_URL=http://localhost:8080
```

## 构建输出

运行 `npm run build` 后，静态文件将输出到 `../api/ui` 目录，
FastAPI 会自动提供这些静态文件。
