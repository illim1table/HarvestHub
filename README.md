# HarvestHub
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
