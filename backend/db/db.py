import motor.motor_asyncio
import os
from bson import ObjectId
from datetime import datetime
from dotenv import load_dotenv

load_dotenv(override=True)

MONGO_URI = os.getenv('MONGO_URI')
DB_NAME = os.getenv('DB_NAME')

# Create MongoDB client
client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_URI)
database = client[DB_NAME]

# get balance on user_id
async def get_balance(userId: str) -> float | None:
    broker = await database['Broker'].find_one({"userId": ObjectId(userId)})
    if not broker:
        return None
    return broker['balance']

# get brokerId from userId
async def get_brokerId(userId: str):
    broker = await database['Broker'].find_one({"userId": ObjectId(userId)})
    if not broker:
        return None
    return str(broker['_id'])

# insert a trade into user's broker
async def insert_trade_to_db(brokerId: str, symbol: str, quantity: int, 
                             entry_price: float, exit_price: float, pnl: float, tradeType: str, time: datetime ):
    try:
        await database['Trade'].insert_one({
            "brokerId": ObjectId(brokerId),
            "symbol": symbol,
            "quantity": quantity,
            "entry_price": entry_price,
            "exit_price": exit_price,
            "pnl": pnl,
            "tradeType": tradeType,
            "createdAt": time
        })
    except Exception as e:
        print(f'Some error occured while inserting trade {e}')

