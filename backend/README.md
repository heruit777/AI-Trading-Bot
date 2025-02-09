# Step to perform before starting devlopment
NOTE: Run all the backend stuff from root of your project

1. Run docker redis
2. Run the fastapi dev backend/web_server.py. Open Postman and hit /login endpoint to get the url, click on it and you will get access_token. Change the access_token of upstox in .env file. 
3. I have implemented a mock websocket server('dummy_ws_server.py') that sends tick data. Run it if you are using demo functions of brokers. (Just for testing purpose). Command uv run dummy_ws_server.py or python -m backend.dummy_ws_server.
4. You may have to delete the variable 'in_trade' which tells that we are currently executing a trade
harsh@debian12:~/coding/AI_Trading_Bot$ docker exec -it <container_id> bash
root@ebcce0d3fcd1:/data# redis-cli 
127.0.0.1:6379> DEL in_trade

# Important Points ( And I want to deploy the project)
1. At 9:45 trade will be executed for all the users in the db. Depending on the broker object linked to the user a broker object will be instantiated.
2. The backend deployed on render has a route '/start-bot' that will create a user to broker map and when the strategy finds a trade it will execute trade for all the users.
3. The updates should be displayed in realtime to the respective users on the frontend.
4. Some frontend features like history, reports etc to improve user experience.

# List of Commands
1. fastapi dev backend/web_server.py
2. python -m backend.dummy_ws_server
3. start docker, docker start <container_id>
4. Go in frontend, pnpm dev
5. npx prisma studio (for the database)
