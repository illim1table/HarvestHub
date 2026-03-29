# HarvestHub
推荐Python版本>=3.11
第一次运行需要添加JWT_SECRET_KEY:
grep -q '^JWT_SECRET_KEY=' .env || echo "JWT_SECRET_KEY=$(python -c 'import secrets; print(secrets.token_urlsafe(48))')" >> .env
安装并配置MYSQL业务用户：
sudo mysql
CREATE DATABASE IF NOT EXISTS harvesthub CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
CREATE USER IF NOT EXISTS 'harvesthub'@'127.0.0.1' IDENTIFIED BY '123';
GRANT ALL PRIVILEGES ON harvesthub.* TO 'harvesthub'@'127.0.0.1';
FLUSH PRIVILEGES;
EXIT;
01-测试方式：
cd backend
pip install -r requirements.txt
uvicorn main:app --reload --host 0.0.0.0 --port 8000
cd frontend
npm install
npm run dev(npm run dev -- --host 0.0.0.0 --port 6006) 
//自定义服务通过proxy agent暴露的服务
//6006端口服务访问地址：
//172.17.x.x:52051
然后在本地浏览器打开：http://172.17.x.x:52051
