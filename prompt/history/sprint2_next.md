# Sprint 2 输入 Prompt

> 📌 历史存档文件：`/prompt/history/sprint2_next.md`。如需继续迭代，请将下述 Prompt 内容发送给 AI 并按当前规范保存下一轮 Prompt。

---

你是一位资深的全栈开发工程师，正在与我共同开发"汇农亩场"农产品交易平台。我们已完成 Sprint 1（项目初始化与基础接口跑通），现在进入 **Sprint 2：数据库连接与用户模型设计**。

## 项目背景（延续 Sprint 1）

- **技术栈**：FastAPI（后端）+ Vue 3（前端）+ MySQL（数据库）
- **Sprint 1 成果**：
  - 后端目录结构已建立，`/api/health` 和 `/api/products`（Mock 数据）接口已就绪。
  - 前端页面可以调用后端接口并渲染商品卡片列表。
  - 项目结构如下：
    ```
    backend/
    ├── main.py
    ├── requirements.txt
    └── app/
        ├── models/product.py
        └── routers/{health,products}.py
    frontend/
    └── src/{App.vue, components/ProductList.vue, api/index.js}
    ```

## Sprint 2 任务目标

请完成以下内容：

### 1. 数据库连接配置

- 使用 **SQLAlchemy**（异步版本 `asyncmy` 或 `aiomysql`）连接 MySQL。
- 配置文件使用 `backend/app/core/config.py`，通过 `.env` 文件管理数据库连接信息（`DB_HOST`, `DB_PORT`, `DB_USER`, `DB_PASSWORD`, `DB_NAME`）。
- 在 `backend/app/database.py` 中创建 `AsyncEngine` 和 `AsyncSession`。

### 2. 用户模型设计

设计并实现以下数据库表（ORM 模型，放在 `backend/app/models/user.py`）：

| 字段名       | 类型         | 说明                         |
|------------|------------|----------------------------|
| id         | INT PK AI  | 主键，自增                     |
| username   | VARCHAR(50)| 用户名，唯一                   |
| email      | VARCHAR(100)| 邮箱，唯一                   |
| hashed_password | VARCHAR(128) | 加密后的密码              |
| role       | ENUM       | 用户角色：`consumer` / `seller` |
| is_active  | BOOLEAN    | 是否激活，默认 True            |
| created_at | DATETIME   | 注册时间                     |

### 3. 用户注册 / 登录接口

- `POST /api/auth/register`：接收 `username`, `email`, `password`, `role`，注册新用户（密码用 `bcrypt` 加密）。
- `POST /api/auth/login`：接收 `email` + `password`，验证成功后返回 JWT Token。
- 使用 `python-jose` 生成 JWT，有效期 30 分钟。
- 新增 `backend/app/routers/auth.py` 路由文件。

### 4. 前端对接（可选，优先后端）

- 在前端添加一个简单的**登录表单**组件 `frontend/src/components/LoginForm.vue`。
- 登录成功后将 JWT 存入 `localStorage`，并在页面顶部展示用户名。

## 输出要求

1. 提供所有新增/修改文件的完整代码，并在代码块上方注明文件路径。
2. 提供数据库初始化 SQL（或 Alembic migration 命令）。
3. 提供更新后的 `requirements.txt`。
4. 更新 Sprint 3 的 Prompt，保存到 `/prompt/output/sprint3_next.md`，内容聚焦于**商品模型持久化与分类管理**。
