# HarvestHub

推荐 Python 版本：`>= 3.11`

## 首次运行：添加 `JWT_SECRET_KEY`

```bash
grep -q '^JWT_SECRET_KEY=' .env || echo "JWT_SECRET_KEY=$(python -c 'import secrets; print(secrets.token_urlsafe(48))')" >> .env
```

## 安装并配置 MySQL 业务用户

```sql
sudo mysql
CREATE DATABASE IF NOT EXISTS harvesthub CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
CREATE USER IF NOT EXISTS 'harvesthub'@'127.0.0.1' IDENTIFIED BY '123';
GRANT ALL PRIVILEGES ON harvesthub.* TO 'harvesthub'@'127.0.0.1';
FLUSH PRIVILEGES;
EXIT;
```

## Sprint 3：建表与初始化数据

### 方式 A（推荐）：启动后端自动建表 + seed 数据导入

```bash
cd backend
pip install -r requirements.txt
uvicorn main:app --reload --host 0.0.0.0 --port 8000

# 新开终端执行 seed（需已存在 users/categories/products 表）
mysql -h 127.0.0.1 -u harvesthub -p123 harvesthub < sql/002_sprint3_seed.sql
```

### 方式 B：手动 SQL 建表 + seed

```bash
cd backend
mysql -h 127.0.0.1 -u harvesthub -p123 harvesthub < sql/001_sprint3_schema.sql
mysql -h 127.0.0.1 -u harvesthub -p123 harvesthub < sql/002_sprint3_seed.sql
```

## 01 - 测试方式

### 后端启动

```bash
cd backend
pip install -r requirements.txt
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### 前端启动

```bash
cd frontend
npm install
npm run dev
# 或指定 host/port：
npm run dev -- --host 0.0.0.0 --port 6006
```

> 自定义服务通过 proxy agent 暴露服务。
> 6006 端口服务访问地址：`172.17.x.x:52051`

然后在本地浏览器打开：<http://172.17.x.x:52051>

## 02 - Sprint 3 API 调试

启动后访问 Swagger：<http://127.0.0.1:8000/docs>

### 示例：分类列表

```bash
curl -X GET 'http://127.0.0.1:8000/api/categories'
```

### 示例：商品列表（分页 + 分类筛选）

```bash
curl -X GET 'http://127.0.0.1:8000/api/products?page=1&page_size=6&category_id=1'
```

### 示例：登录并创建商品

```bash
TOKEN=$(curl -s -X POST 'http://127.0.0.1:8000/api/auth/login' \
  -H 'Content-Type: application/json' \
  -d '{"email":"seed_seller@harvesthub.local","password":"Seller@123"}' | python -c 'import sys,json;print(json.load(sys.stdin)["access_token"])')

curl -X POST 'http://127.0.0.1:8000/api/products' \
  -H "Authorization: Bearer ${TOKEN}" \
  -H 'Content-Type: application/json' \
  -d '{
    "name":"测试商品",
    "description":"用于接口调试",
    "price":9.90,
    "unit":"斤",
    "stock":20,
    "image_url":"https://placehold.co/300x200?text=测试",
    "category_id":1
  }'
```
