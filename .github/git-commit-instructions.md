# GitHub Copilot 全局 Git 提交说明配置（中文优先版）

## Git Flow 工作流规范

### 分支管理策略

#### 核心分支
```
# master - 生产环境稳定代码
git switch master
git pull origin master

# dev - 开发主分支
git switch dev
git pull origin dev

# test - 测试分支
git switch test
git pull origin test

# release - 预发布分支
git switch release
git pull origin release
```

#### 功能开发分支
```
# 创建新功能分支
git switch dev
git pull origin dev
git switch -c feature/模块名-功能描述

# 示例：
git switch -c feature/search-hotel-brand
git switch -c feature/user-auth-login
```

#### 紧急修复分支
```
# 创建紧急修复分支
git switch master
git pull origin master
git switch -c hf/bug描述-YYYYMMDD

# 示例：
git switch -c hf/login-session-fix-20240115
```

#### 分支合并操作
```
# 合并功能分支到dev
git switch dev
git merge feature/branch-name
git push origin dev
git branch -d feature/branch-name

# 合并紧急修复到master和dev
git switch master
git merge hf/fix-name
git push origin master
git switch dev
git merge hf/fix-name
git push origin dev
git branch -d hf/fix-name
```

## Conventional Commits 提交规范（中文优先）

### 提交格式模板
```
<type>(<scope>): <subject>

<body>

<footer>
```

### 提交类型说明（中文描述优先）

#### feat - 新功能开发
```
# GitHub Copilot 提示：
# feat: 添加新功能（使用中文描述）

feat(user): 添加用户管理模块
feat(auth): 实现JWT token认证
feat(search): 集成酒店品牌搜索功能
feat(api): 添加酒店搜索API接口
feat(geo): 实现地理位置搜索功能
```

#### fix - Bug修复
```
# GitHub Copilot 提示：
# fix: 修复bug问题（使用中文描述）

fix(login): 修复登录页面验证码不显示问题
fix(search): 解决酒店搜索结果排序异常
fix(api): 解决用户查询接口空指针异常
fix(cache): 修复Redis缓存失效问题
fix(geo): 修复地理位置坐标转换错误
```

#### docs - 文档更新
```
# GitHub Copilot 提示：
# docs: 更新文档（使用中文描述）

docs(readme): 更新项目部署说明
docs(api): 完善酒店搜索接口文档
docs(search): 更新搜索功能使用说明
docs(changelog): 更新版本变更记录
```

#### style - 代码格式调整
```
# GitHub Copilot 提示：
# style: 代码格式优化（使用中文描述）

style(search): 统一搜索模块代码缩进格式
style: 移除多余的空行和注释
style(user): 优化代码注释格式
style(config): 规范配置文件格式
```

#### refactor - 代码重构
```
# GitHub Copilot 提示：
# refactor: 代码重构优化（使用中文描述）

refactor(search): 优化酒店搜索服务层代码结构
refactor(util): 提取公共搜索工具类方法
refactor(controller): 重构搜索控制器逻辑
refactor(service): 重构用户服务架构
```

#### perf - 性能优化
```
# GitHub Copilot 提示：
# perf: 性能优化改进（使用中文描述）

perf(search): 优化酒店搜索查询性能
perf(cache): 添加Redis缓存提升搜索响应速度
perf(elasticsearch): 优化ES索引配置
perf(database): 优化数据库查询语句
```

#### test - 测试相关
```
# GitHub Copilot 提示：
# test: 测试用例添加（使用中文描述）

test(search): 添加酒店搜索服务单元测试
test(integration): 完善搜索功能集成测试用例
test(elasticsearch): 添加ES搜索测试
test(geo): 添加地理位置搜索测试用例
```

#### chore - 构建和辅助工具
```
# GitHub Copilot 提示：
# chore: 构建配置更新（使用中文描述）

chore(deps): 升级Spring Boot版本到3.1.5
chore(build): 优化Maven构建配置
chore(config): 更新搜索服务配置文件
chore(dependencies): 更新依赖库版本
```

## GitHub Copilot 中文提交说明模板

### 功能开发提交模板
```
# GitHub Copilot 提示：新功能开发提交说明（中文）

feat(search): 实现酒店品牌搜索功能

- 集成Elasticsearch搜索引擎
- 支持品牌名称模糊匹配
- 添加品牌搜索结果排序

Closes #123
```

### Bug修复提交模板
```
# GitHub Copilot 提示：Bug修复提交说明（中文）

fix(search): 修复地理位置搜索精度问题

- 优化Geo-spatial查询参数
- 修复坐标转换逻辑
- 添加搜索结果验证

Fixes #456
```

### 代码重构提交模板
```
# GitHub Copilot 提示：代码重构提交说明（中文）

refactor(search): 重构搜索服务架构

- 提取搜索策略接口
- 优化缓存处理逻辑
- 统一异常处理机制

Related to #789
```

### 性能优化提交模板
```
# GitHub Copilot 提示：性能优化提交说明（中文）

perf(search): 优化酒店搜索性能

- 添加Redis缓存层
- 优化Elasticsearch查询语句
- 实现搜索结果预热机制

Improves #101
```

## 日常开发提交工作流（中文优先）

### 开发过程中的提交
```
# GitHub Copilot 提示：开发阶段提交（中文）

# 功能实现中
style(search): 完成搜索控制器基础结构
feat(search): 实现品牌搜索核心逻辑
test(search): 添加基础单元测试

# 代码优化
refactor(search): 优化搜索结果处理逻辑
perf(search): 添加缓存提升查询性能
```

### 功能完成提交
```
# GitHub Copilot 提示：功能完成提交（中文）

feat(search): 完成酒店搜索功能开发

- 支持品牌、酒店名、地理位置搜索
- 集成Elasticsearch和Redis
- 实现搜索结果分页和排序
- 添加完整的单元测试覆盖

Completes #123
```

## 特殊场景提交说明（中文）

### 紧急修复提交
```
# GitHub Copilot 提示：紧急修复提交（中文）

fix(search): 紧急修复生产环境搜索异常

- 修复ES连接池配置问题
- 优化搜索超时处理
- 添加监控日志

Hotfix for production issue
```

### 配置更新提交
```
# GitHub Copilot 提示：配置更新提交（中文）

chore(config): 更新搜索服务配置

- 调整Elasticsearch连接参数
- 优化Redis缓存配置
- 更新搜索权重设置

Related to #456
```

## GitHub Copilot 中文提交生成配置

### 中文提交说明生成提示
```
# 在GitHub Copilot中使用以下提示模板（中文优先）：

/*
根据以下代码变更，生成符合Conventional Commits规范的提交说明：
- 使用中文描述（除非技术术语需要英文）
- 变更类型：[feat/fix/refactor/perf等]
- 变更范围：[search/user/auth等，使用英文]
- 变更描述：[使用简洁的中文描述]
- 详细说明：[可选的详细变更内容，使用中文]
- 关联任务：[相关的Issue编号]

示例格式：
feat(search): 实现酒店品牌搜索功能

- 集成Elasticsearch搜索引擎
- 支持模糊匹配查询

Closes #123
*/
```

### 分支操作提示（中文）
```
# GitHub Copilot 分支操作辅助提示（中文）：

/*
按照Git Flow工作流，执行以下操作：
1. 从dev分支创建新的功能分支
2. 分支命名规范：feature/模块-功能描述（使用英文）
3. 确保分支操作符合团队规范
4. 提交信息使用中文描述功能变更
*/
```

### 多语言使用规范
```
# GitHub Copilot 多语言使用指导：

/*
提交说明多语言使用规范：
1. 主要描述使用中文
2. 技术术语、模块名、变量名保持英文
3. 分支名、标签名使用英文
4. 配置项、代码引用使用英文
5. 用户可见的功能描述使用中文

示例：
✅ 正确：feat(search): 优化酒店地理位置搜索算法
✅ 正确：fix(api): 解决Elasticsearch geo_point类型映射错误
❌ 错误：feat(search): optimize hotel geo search algorithm
*/
```

## 中文提交最佳实践

### 提交信息长度控制
```
# GitHub Copilot 提示：中文提交长度控制

/*
中文提交信息长度规范：
- 主题行（subject）：不超过50个字符（中文）
- 正文行（body）：每行不超过72个字符
- 使用简洁明了的中文表述
- 避免冗长的技术细节描述
*/
```

### 中文语法规范
```
# GitHub Copilot 提示：中文语法规范

/*
中文提交语法规范：
- 使用祈使句，如"添加"、"修复"、"优化"
- 避免使用"了"、"的"等冗余词汇
- 保持语句简洁有力
- 使用标准中文标点符号
*/
```

