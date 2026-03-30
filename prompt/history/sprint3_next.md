# Sprint 3 输入 Prompt

> 📌 历史存档文件：`/prompt/history/sprint3_next.md`。如需继续迭代，请将下述 Prompt 内容发送给 AI 并按当前规范保存下一轮 Prompt。

---

你是一位资深的全栈开发工程师，正在与我共同开发"汇农亩场"农产品交易平台。我们已完成 **Sprint 2（数据库连接与用户认证）**，现在进入 **Sprint 3：商品模型持久化与分类管理**。

## 项目背景（延续 Sprint 2）

- **技术栈**：FastAPI（后端）+ Vue 3（前端）+ MySQL（数据库）
- **Sprint 2 成果**：
  - 后端已接入 MySQL（SQLAlchemy Async + aiomysql）
  - 已有 `users` 用户表与注册/登录接口（JWT）
  - 前端已支持登录并保存 Token

## Sprint 3 任务目标

请完成以下内容：

### 1. 商品模型持久化（替换 Mock 数据）

- 在后端新增并实现商品 ORM 模型（如 `backend/app/models/product.py`）并映射到 MySQL 表。
- 将现有 `/api/products` 与 `/api/products/{id}` 从 Mock 列表改为数据库查询。
- 字段至少包含：
  - `id`、`name`、`description`、`price`、`unit`、`stock`、`image_url`、`seller_id`、`category_id`、`created_at`。

### 2. 分类管理模块

- 新增商品分类模型（`Category`），支持层级前先做一级分类：
  - `id`、`name`（唯一）、`description`、`is_active`、`created_at`。
- 提供分类接口：
  - `GET /api/categories`：查询分类列表
  - `POST /api/categories`：新增分类（仅 seller 或管理员可扩展）

### 3. 商品 CRUD 接口

- 至少实现：
  - `POST /api/products`：创建商品
  - `GET /api/products`：商品列表（支持分页、按分类筛选）
  - `GET /api/products/{id}`：商品详情
  - `PUT /api/products/{id}`：更新商品
  - `DELETE /api/products/{id}`：下架/删除商品
- 保持响应结构统一，补充必要的请求/响应 Schema。

### 4. 数据初始化与迁移

- 提供建表 SQL 或 Alembic migration。
- 准备最少 5 条商品与 3 条分类的初始化数据（seed）。

### 5. 前端基础对接

- 前端分类筛选下拉框接入 `GET /api/categories`。
- 商品列表改为真实后端分页数据。
- 新增一个简易“发布商品”表单（可先不做完整权限页）。

## 输出要求

1. 提供所有新增/修改文件的完整代码，并在代码块上方注明文件路径。
2. 给出数据库迁移/初始化命令与示例数据导入方式。
3. 说明接口调试方式（可用 curl 或 Swagger）。
4. 保持与现有代码风格一致，确保可直接运行。
