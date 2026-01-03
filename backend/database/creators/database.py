from odmantic import AIOEngine
from motor.motor_asyncio import AsyncIOMotorClient

client = AsyncIOMotorClient("mongodb://localhost:27017")
engine = AIOEngine(motor_client=client, database="Cmi-city")