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
