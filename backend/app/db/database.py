from motor.motor_asyncio import AsyncIOMotorClient
from app.core.config import settings

# Create the MongoDB client
client = AsyncIOMotorClient(settings.MONGO_URI)

# Access the specific database
db = client.ems_db