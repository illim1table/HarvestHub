# Sprint 4 输入 Prompt

> 📌 本文件位于仓库根目录下的 `prompt/sprint4_next.md`；在下一轮对话开始时，请将以下内容发送给 AI。

---

你是一位资深的全栈开发工程师，正在与我共同开发"汇农亩场"农产品交易平台。我们已完成 **Sprint 3（商品模型持久化与分类管理）**，现在进入 **Sprint 4：交易下单与订单管理闭环（MVP）**。

## 项目背景（延续 Sprint 1-3）

- **技术栈**：FastAPI（后端）+ Vue 3（前端）+ MySQL（数据库）
- **已完成能力（摘要）**：
  - 用户注册/登录（JWT）
  - 商品与分类持久化（MySQL）
  - 商品列表、详情、发布等基础能力

## Sprint 4 任务目标

请完成以下内容：

### 1. 订单模型与数据库设计

- 新增订单主表与订单项表（例如 `orders`、`order_items`），满足最小交易闭环。
- 建议字段：
  - `orders`：`id`、`buyer_id`、`status`、`total_amount`、`created_at`、`updated_at`
  - `order_items`：`id`、`order_id`、`product_id`、`price`、`quantity`、`amount`
- 订单状态至少包含：`pending`、`paid`、`cancelled`、`completed`（可按枚举或字符串实现）。
- 提供建表 SQL 或 migration。

### 2. 下单与订单查询接口

- `POST /api/orders`：买家创建订单（支持一次提交多个商品项）。
- `GET /api/orders`：当前登录用户订单列表（可按角色区分买家/卖家视角，先实现买家必需能力）。
- `GET /api/orders/{id}`：订单详情（含订单项）。
- `PUT /api/orders/{id}/cancel`：取消未支付订单（需做状态校验）。

### 3. 库存与金额规则

- 下单时校验商品是否存在、是否可售、库存是否充足。
- 成功下单后扣减库存（保证同一事务内一致性）。
- 订单金额由后端基于实时单价计算，不信任前端传入金额。

### 4. 前端最小对接

- 新增简易“购物车/下单”交互（可以从商品列表发起）。
- 新增“我的订单”页面或组件，展示订单列表与详情入口。
- 失败场景（库存不足、未登录）需给出清晰提示。

### 5. 可运行性与接口验证

- 提供最小可复现的调试方式（Swagger 或 curl）。
- 保持现有项目结构与代码风格一致，确保可以直接启动验证。

## 输出要求

1. 提供所有新增/修改文件的完整代码，并在代码块上方注明文件路径。
2. 给出数据库初始化/迁移与数据准备命令。
3. 说明关键接口的请求示例与调试步骤。
4. 路径规范：当前可执行的 Sprint Prompt 放在 `prompt/`（命名为 `prompt/sprintN_next.md`，`N` 为当前 Sprint 编号）；历史 Prompt 统一放在 `prompt/history/`。
5. **必须生成 Sprint 5 的输入 Prompt**（延续迭代），并保存到：`prompt/sprint5_next.md`。
6. Sprint 5 Prompt 需要明确聚焦“支付回调模拟 + 订单状态流转完善 + 卖家订单管理”。
