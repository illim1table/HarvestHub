# HarvestHub

推荐 Python 版本：`>= 3.11`

## 项目博客
https://blog.csdn.net/A15280019132/article/details/159582097?spm=1001.2014.3001.5501

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

## Sprint 4-5：订单与支付模拟能力

```bash
cd backend
# 新环境可直接顺序执行；已执行过 Sprint 3 建表时，仅补执行 003/004/005 即可
mysql -h 127.0.0.1 -u harvesthub -p123 harvesthub < sql/001_sprint3_schema.sql
mysql -h 127.0.0.1 -u harvesthub -p123 harvesthub < sql/003_sprint4_schema.sql
mysql -h 127.0.0.1 -u harvesthub -p123 harvesthub < sql/005_sprint5_schema.sql
mysql -h 127.0.0.1 -u harvesthub -p123 harvesthub < sql/002_sprint3_seed.sql
mysql -h 127.0.0.1 -u harvesthub -p123 harvesthub < sql/004_sprint4_seed.sql
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

## 02 - Sprint 5 API 调试（支付回调 + 状态流转 + 卖家订单）

启动后访问 Swagger：<http://127.0.0.1:8000/docs>

### 1) 买家登录

```bash
BUYER_TOKEN=$(curl -s -X POST 'http://127.0.0.1:8000/api/auth/login' \
  -H 'Content-Type: application/json' \
  -d '{"email":"seed_buyer@harvesthub.local","password":"Buyer@123"}' | python -c 'import sys,json;print(json.load(sys.stdin)["access_token"])')
```

### 2) 卖家登录

```bash
SELLER_TOKEN=$(curl -s -X POST 'http://127.0.0.1:8000/api/auth/login' \
  -H 'Content-Type: application/json' \
  -d '{"email":"seed_seller@harvesthub.local","password":"Seller@123"}' | python -c 'import sys,json;print(json.load(sys.stdin)["access_token"])')
```

### 3) 买家创建订单

```bash
ORDER_ID=$(curl -s -X POST 'http://127.0.0.1:8000/api/orders' \
  -H "Authorization: Bearer ${BUYER_TOKEN}" \
  -H 'Content-Type: application/json' \
  -d '{"items":[{"product_id":1,"quantity":1}]}' | python -c 'import sys,json;print(json.load(sys.stdin)["data"]["id"])')
```

### 4) 模拟支付成功回调

```bash
curl -X POST 'http://127.0.0.1:8000/api/payments/mock' \
  -H 'Content-Type: application/json' \
  -d "{\"order_id\":${ORDER_ID},\"trade_no\":\"MOCK-${ORDER_ID}-001\",\"pay_status\":\"success\"}"
```

### 5) 买家确认收货（paid -> completed）

```bash
curl -X PUT "http://127.0.0.1:8000/api/orders/${ORDER_ID}/confirm" \
  -H "Authorization: Bearer ${BUYER_TOKEN}"
```

### 6) 卖家查看订单列表与详情

```bash
curl -X GET 'http://127.0.0.1:8000/api/seller/orders?status=completed' \
  -H "Authorization: Bearer ${SELLER_TOKEN}"

curl -X GET "http://127.0.0.1:8000/api/seller/orders/${ORDER_ID}" \
  -H "Authorization: Bearer ${SELLER_TOKEN}"
```

### 7) 重复支付回调幂等验证

```bash
curl -X POST 'http://127.0.0.1:8000/api/payments/mock' \
  -H 'Content-Type: application/json' \
  -d "{\"order_id\":${ORDER_ID},\"trade_no\":\"MOCK-${ORDER_ID}-001\",\"pay_status\":\"success\"}"
```
