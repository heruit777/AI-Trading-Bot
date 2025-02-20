import os
import httpx
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from dotenv import load_dotenv
from urllib.parse import urlencode
from backend.brokers.brokerFactory import BrokerFactory, BrokerType
from backend.bot.Bot import Bot
from bson import ObjectId
from starlette.middleware.cors import CORSMiddleware
from backend.monitoring.monitoring import Monitoring
from contextlib import asynccontextmanager
import asyncio
import json
from backend.db.db import database, get_trade_count_for_today
import backend.config as config
from backend.logger_config import logger


# Good practice to define env varialbes before the app starts and we can use pydantic to validate the env file
load_dotenv(override=True)
# client_id = os.getenv('UPSTOX_API_KEY')
# client_secret = os.getenv('UPSTOX_API_SECRET')
redirect_uri = 'http://127.0.0.1:8000/oauth/callback'

@asynccontextmanager
async def lifespan(app: FastAPI):
    monitor = Monitoring.get_instance()
    asyncio.create_task(send_pnl_updates(monitor))
    yield
    print(f'Final History: {monitor.history}')
    
app = FastAPI(lifespan=lifespan)

# app = FastAPI()
# Allow CORS for specific origins (you can adjust this as needed)
origins = [
    "http://localhost:3000",  # Replace with your frontend URL
    # "https://yourfrontenddomain.com",  # If you have a production frontend
]



# Adding CORS middleware to FastAPI app
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # List of allowed origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all HTTP methods (GET, POST, etc.)
    allow_headers=["*"],  # Allows all headers
)

@app.get('/')
def check():
    return {"status": "Healthy"}

@app.get('/login')
async def login(client_id: str, client_secret: str, user_id: str):
    base_url = "https://api.upstox.com/v2/login/authorization/dialog"
    query = {
        "client_id": client_id,
        "redirect_uri": redirect_uri,
        "state": user_id,
        "response_type": "code"
    }
    query = urlencode(query)
    url = base_url+'?'+query

    # Save to the database
    user = await database['Broker'].find_one({"userId": ObjectId(user_id)})
    if not user:
        await database['Broker'].insert_one({
            'userId': ObjectId(user_id),
            'api_key': client_id,
            'api_secret': client_secret
        })
        return {"url": url}
    
    if not user['api_key'] and not user['api_secret']:
        # both are missing so write them
        await database['Broker'].update_one({"userId": ObjectId(user_id)}, {
            "$set": {"api_key": client_id, "api_secret": client_secret}
        })
    
    return {"url":url}

@app.get("/oauth/callback")
async def oauth_callback(code: str, state: str | None = None):
    # Perform further actions like exchanging the code for an access token
    # return {
    #     "message": "Authorization successful",
    #     "code": code,
    #     "state": state
    # }
    # Get the apikey and secret from the db, state has userid
    userId = state
    if userId:
        user = await database['Broker'].find_one({"userId": ObjectId(userId)})
        if not user or not user['api_key'] or not user['api_secret']:
            return {"status": "error", "msg": "User not found"}
    
    client_id = user["api_key"]
    client_secret = user["api_secret"]
        
    base_url = 'https://api.upstox.com/v2/login/authorization/token'
    headers = {
        'accept': 'application/json',
        'Content-Type': 'application/x-www-form-urlencoded',
    }
    data = {
        'code': code,
        'client_id': client_id,
        'client_secret': client_secret,
        'redirect_uri': redirect_uri,
        'grant_type': 'authorization_code'
    }
    async with httpx.AsyncClient() as client:
        res = await client.post(base_url, headers=headers, data=data)
        data = res.json()
        
    if res.status_code == 200:
        return {'status': 'success', 'access_token': data['access_token']}
    # TODO: find a way to directly put access token inside the textbox in frontend.
    # I think you can send a pretty UI that displays you will be redirected to the website in 5 seconds
    return data

# check all the user in the db and if any broker is linked (dummy or real ones) then
# we will create a broker instance of the type for that user and store it in the queue.
@app.get('/start-bot')
async def start_bot():
    # Simulate database query for users with linked brokers
    try:
        # users = [
        #     {"user_id": "user_1", "broker_type": "dummy"},
        #     {"user_id": "user_2", "broker_type": "dummy"},
        # ]
        users_with_linked_brokers = await database['Broker'].find().to_list(length=None) # None fetches all the users
        # TODO: we should make some mechanism to encrypt the upstox credentials of the user
        user_broker_map = {}
        print(users_with_linked_brokers)
        for user in users_with_linked_brokers:
            user_id = str(user["userId"])
            broker_type = user["broker_type"]
            access_token = user['access_token']
            api_version = user['api_version']
            user_broker_map[user_id] = BrokerFactory.create_broker(BrokerType[broker_type.upper()], access_token, api_version)

        print(user_broker_map)
        admin_broker = BrokerFactory.create_broker(BrokerType.DUMMY, os.getenv('UPSTOX_ACCESS_TOKEN'), os.getenv('UPSTOX_API_VERSION'))
        bot = Bot(user_broker_map, admin_broker)
        bot.run()
        return {"message": "Brokers initialized and bot started"}
    except Exception as e:
        print(f'Some error occured {e}')
        return {"message": "Failed to start the bot"}
    
# Function to send personalized P&L updates
async def send_pnl_updates(monitor: Monitoring):
    print('Sending Pnl updates to active users')
    while True:
        # print('RUNNING continously')
        if not config.user_connections:
            print('No active users')
            await asyncio.sleep(0.1)
            continue

        for user_id, websocket in list(config.user_connections.items()):
            # ChatGPT gave the following code now improve it
            # print(f'Value of {monitor.user_to_orders}')
            await asyncio.sleep(0.1)
            # print(f'User id [{user_id}] and map: {monitor.user_to_orders} and Status: {user_id in monitor.user_to_orders}')
            if user_id in monitor.user_to_orders:
                try:
                    # Send only this user's P&L
                    order_details = monitor.get_order_details(user_id)
                    # print(order_details)
                    # print(f"Sending {order_details} to User [{user_id}]")
                    # print(f'Value of websocket {websocket}')
                    # print(f'is websocket closed? {websocket.client_state}')
                    await websocket.send_text(json.dumps(order_details))
                except WebSocketDisconnect:
                    del config.user_connections[user_id]
                    print(f'Removed user [{user_id}] because websocket disconnected')
                except Exception as e:
                    # del config.user_connections[user_id]
                    # print(e.with_traceback())
                    print(f'Removed user [{user_id}]')
                    print(f"Error sending PnL to {user_id}: {e}")
            else:
                del config.user_connections[user_id]
                print(f'Removed the user id [{user_id}] as it does not have any trades for him')
                await websocket.close()

        print(f'Tasking is running and connections: {config.user_connections}')

@app.websocket("/ws/trade-updates/{user_id}")
async def websocket_endpoint(websocket: WebSocket, user_id: str):
    if not user_id:
        print(f'No user_id so closing websocket connection with user id [{user_id}]')
        await websocket.close(code=1008)
        return
    
    # check if user_id exists in the db or not.
    user = await database['Broker'].find_one({"userId": ObjectId(user_id)})
    if not user:
        print(f'User Id does not exists in the db')
        await websocket.close(code=1008)
        return
    
    # MAX_TRADES_PER_DAY Limit reached
    trade_count = await get_trade_count_for_today(user_id)
    if(trade_count >= config.MAX_NUMBER_OF_TRADES_PER_DAY):
        print(f"User's MAX TRADE LIMIT reached")
        await websocket.close()
        return 
    
    await websocket.accept()
    config.user_connections[user_id] = websocket
    print(f"User {user_id} connected and Websocket {websocket} and connections : {config.user_connections}")

    try:
        while True:
            await asyncio.sleep(0.1)
            # await websocket.receive_text()
    except WebSocketDisconnect:
        print(f"User {user_id} disconnected")
        del config.user_connections[user_id]  # Remove user on disconnect
    
