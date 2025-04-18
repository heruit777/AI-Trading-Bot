# List of Commands

1. fastapi dev backend/web_server.py (Starts the main backend server)
2. python -m backend.dummy_ws_server (Starts the mock upstox server that return reliance tick price)
3. start docker, docker ps -a, docker start <container_id> (Starts redis)
4. Go in frontend directory, pnpm dev
5. npx prisma studio (for the database)

# To start the bot

1. open postman in vscode, go to AI Trading Bot collection
2. Hit /start-bot endpoint (This will start the bot)

# Points

1. To change your strategy go to Bot.py and change the self.strategy to (RandomStrategy() or LLMStrategy())
2. To fetch real tick from upstox broker go to Bot.py and self.admin_broker.fetch_and_publish_ticks() in asyncio.gather()
3. The monitoring module doesn't have the ability to close the trade based on timing (trade is auto squared off by broker at 15:11 approx.) This will become important if you are deploying your project.
