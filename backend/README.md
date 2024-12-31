# Step to perform before starting devlopment
1. Run docker redis
2. change the access_token of upstox in .env file. Run the fastapi dev backend/web_server.py.
3. I have implemented a mock websocket server('dummy_ws_server.py') that sends tick data. Run it if you are using demo functions of brokers. (Just for testing purpose)
4. You may have to delete the variable 'in_trade' which tells that we are currently executing a trade
harsh@debian12:~/coding/AI_Trading_Bot$ docker exec -it <container_id> bash
root@ebcce0d3fcd1:/data# redis-cli 
127.0.0.1:6379> DEL in_trade
