# Sprint 1 初始化 Prompt 存档

## 输入 Prompt（发送给 AI 的完整内容）

你是一位资深的全栈开发工程师。现在需要你从零开始带我开发并复现一个农产品交易项目。

### Project Context（项目宏观背景）

- **项目名称**："汇农亩场"农产品交易平台
- **整体目标**：搭建一个类似于"淘宝"的农产品交易平台，实现供销商到消费者的直接交易。
- **技术栈要求**：
  - 后端：Python (FastAPI)
  - 前端：JavaScript (Vue)
  - 数据库：MySQL（我将提供公网 IP）
- **长期规划**：在完成传统前后端开发后，将引入 Agent 技术，提供智能体交互场景（如：农产品交易顾问）。

### Current Task（本轮任务：Sprint 1）

由于 token 长度限制，我们采用敏捷迭代的方式。本轮你需要完成以下工作：

1. **项目初始化**：设计并输出前后端的基础目录结构。
2. **跑通简单交互**：
   - 后端：编写一个简单的测试接口（例如 `/api/health` 或模拟的商品列表接口）。
   - 前端：编写一个基础页面，能够发起请求调用上述后端接口，并将结果渲染到页面上。
3. **环境说明**：请提供前后端项目的启动命令。

### Output Requirements（输出要求）

1. 请提供上述代码的完整实现，并在代码块上方注明完整的文件路径。
2. **Prompt 存档**：
   - 请生成一段 Markdown 格式的内容，包含本次完整的 Prompt，并保存在 `/prompt/input/sprint1_init.md`。
   - 请基于本轮任务的结果，帮我撰写**下一步（Sprint 2：数据库连接与用户模型设计）**需要输入的 Prompt，并保存在 `/prompt/output/sprint2_next.md`。

---

## Sprint 1 交付结果

### 项目目录结构

```
HarvestHub/
├── backend/
│   ├── main.py                  # FastAPI 应用入口
│   ├── requirements.txt         # Python 依赖
│   └── app/
│       ├── __init__.py
│       ├── models/
│       │   ├── __init__.py
│       │   └── product.py       # 商品数据模型
│       └── routers/
│           ├── __init__.py
│           ├── health.py        # 健康检查路由
│           └── products.py      # 商品列表路由（Mock 数据）
├── frontend/
│   ├── index.html
│   ├── package.json
│   ├── vite.config.js
│   └── src/
│       ├── main.js
│       ├── App.vue              # 根组件（含健康检查状态展示）
│       ├── api/
│       │   └── index.js         # axios 封装 + API 函数
│       └── components/
│           └── ProductList.vue  # 商品列表组件
└── prompt/
    ├── input/
    │   └── sprint1_init.md      # 本文件
    └── output/
        └── sprint2_next.md      # Sprint 2 Prompt
```

### 启动命令

**后端：**

```bash
cd backend
pip install -r requirements.txt
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

**前端：**

```bash
cd frontend
npm install
npm run dev
```

访问地址：
- 前端页面：http://localhost:5173
- 后端 API 文档：http://localhost:8000/docs
- 健康检查：http://localhost:8000/api/health
- 商品列表：http://localhost:8000/api/products
