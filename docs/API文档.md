# LittleCrawler API 文档

> 启动服务: `uvicorn api.main:app --port 8080 --reload`
>
> **默认账号**: admin / admin123

## 概览

| 类别      | 基础路径       | 说明                 | 认证                |
| --------- | -------------- | -------------------- | ------------------- |
| 认证      | `/api/auth`    | 登录、登出、用户信息 | ❌ 登录接口无需认证 |
| 爬虫控制  | `/api/crawler` | 启动、停止、状态查询 | ✅ 需要 Token       |
| 数据管理  | `/api/data`    | 文件列表、预览、下载 | ✅ 需要 Token       |
| WebSocket | `/api/ws`      | 实时日志、状态推送   | ❌ 无需认证         |

---

## 认证 `/api/auth`

### 用户登录

```
POST /api/auth/login
```

**请求体**

```json
{
  "username": "admin",
  "password": "admin123"
}
```

**响应**

```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIs...",
  "token_type": "bearer"
}
```

**错误码**

- `401` - 用户名或密码错误

---

### 获取当前用户

```
GET /api/auth/me
Authorization: Bearer <token>
```

**响应**

```json
{
  "id": 1,
  "username": "admin",
  "is_active": true
}
```

---

### 用户登出

```
POST /api/auth/logout
Authorization: Bearer <token>
```

**响应**

```json
{ "message": "登出成功" }
```

---

## 爬虫控制 `/api/crawler`

> ⚠️ 所有接口需要 `Authorization: Bearer <token>` 请求头

### 启动爬虫

```
POST /api/crawler/start
Authorization: Bearer <token>
```

**请求体**

```json
{
  "platform": "xhs", // 必填: xhs | zhihu
  "crawler_type": "search", // search | detail | creator
  "login_type": "qrcode", // qrcode | phone | cookie
  "keywords": "咖啡", // search 模式使用
  "specified_ids": "", // detail 模式使用，逗号分隔
  "creator_ids": "", // creator 模式使用，逗号分隔
  "start_page": 1,
  "enable_comments": true,
  "enable_sub_comments": false,
  "save_option": "json", // csv | json | db | sqlite | mongodb | excel
  "cookies": "", // cookie 登录时使用
  "headless": false
}
```

**响应**

```json
{ "status": "ok", "message": "爬虫启动成功" }
```

**错误码**

- `401` - 未认证
- `400` - 爬虫已在运行
- `500` - 启动失败

---

### 停止爬虫

```
POST /api/crawler/stop
```

**响应**

```json
{ "status": "ok", "message": "Crawler stopped successfully" }
```

**错误码**

- `400` - 没有正在运行的爬虫
- `500` - 停止失败

---

### 获取状态

```
GET /api/crawler/status
```

**响应**

```json
{
  "status": "running", // idle | running | stopping | error
  "platform": "xhs",
  "crawler_type": "search",
  "started_at": "2026-01-07T11:30:00",
  "error_message": null
}
```

---

### 获取日志

```
GET /api/crawler/logs?limit=100
```

**参数**

- `limit` (可选): 返回日志条数，默认 100

**响应**

```json
{
  "logs": [
    {
      "id": 1,
      "timestamp": "11:30:00",
      "level": "info", // info | warning | error | success | debug
      "message": "Starting crawler..."
    }
  ]
}
```

---

## 数据管理 `/api/data`

### 获取文件列表

```
GET /api/data/files?platform=xhs&file_type=json
```

**参数**

- `platform` (可选): 平台过滤 (xhs, zhihu)
- `file_type` (可选): 类型过滤 (json, csv, xlsx)

**响应**

```json
{
  "files": [
    {
      "name": "search_contents_2026-01-07.json",
      "path": "xhs/json/search_contents_2026-01-07.json",
      "size": 102400,
      "modified_at": 1736234400.0,
      "record_count": 50,
      "type": "json"
    }
  ]
}
```

---

### 预览文件内容

```
GET /api/data/files/{file_path}?preview=true&limit=100
```

**参数**

- `preview` (可选): 是否预览模式，默认 true
- `limit` (可选): 预览记录数，默认 100

**响应 (JSON/CSV)**

```json
{
  "data": [{ "title": "...", "content": "..." }],
  "total": 500
}
```

**响应 (Excel)**

```json
{
  "data": [{ "title": "...", "content": "..." }],
  "total": 500,
  "columns": ["title", "content", "author"]
}
```

---

### 下载文件

```
GET /api/data/download/{file_path}
```

**响应**: 文件下载流 (`application/octet-stream`)

---

### 数据统计

```
GET /api/data/stats
```

**响应**

```json
{
  "total_files": 25,
  "total_size": 5242880,
  "by_platform": { "xhs": 15, "zhihu": 10 },
  "by_type": { "json": 20, "csv": 5 }
}
```

---

## WebSocket `/api/ws`

### 实时日志流

```
WS /api/ws/logs
```

**心跳**: 客户端发送 `ping`，服务端响应 `pong`

**推送消息**

```json
{
  "id": 1,
  "timestamp": "11:30:00",
  "level": "info",
  "message": "..."
}
```

---

### 实时状态流

```
WS /api/ws/status
```

**推送频率**: 每秒一次

**推送消息**

```json
{
  "status": "running",
  "platform": "xhs",
  "crawler_type": "search",
  "started_at": "2026-01-07T11:30:00"
}
```

---

## 系统接口

### 健康检查

```
GET /api/health
```

**响应**

```json
{ "status": "ok" }
```

---

### 环境检查

```
GET /api/env/check
```

**响应**

```json
{
  "success": true,
  "message": "LittleCrawler environment configured correctly",
  "output": "..."
}
```

---

## 枚举值参考

| 字段           | 可选值                                            |
| -------------- | ------------------------------------------------- |
| `platform`     | `xhs`, `zhihu`                                    |
| `crawler_type` | `search`, `detail`, `creator`                     |
| `login_type`   | `qrcode`, `phone`, `cookie`                       |
| `save_option`  | `csv`, `json`, `db`, `sqlite`, `mongodb`, `excel` |
| `status`       | `idle`, `running`, `stopping`, `error`            |
| `log.level`    | `info`, `warning`, `error`, `success`, `debug`    |
