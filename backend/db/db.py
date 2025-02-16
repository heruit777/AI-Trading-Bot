import motor.motor_asyncio
import os
from bson import ObjectId
from dotenv import load_dotenv

load_dotenv(override=True)

MONGO_URI = os.getenv('MONGO_URI')
DB_NAME = os.getenv('DB_NAME')

# Create MongoDB client
client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_URI)
database = client[DB_NAME]

# get balance on user_id
async def get_balance(userId: str) -> float | None:
    user = await database['Broker'].find_one({"userId": ObjectId(userId)})
    if not user:
        return None
    return user['balance']
