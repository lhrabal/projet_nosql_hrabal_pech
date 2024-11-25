from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from motor.motor_asyncio import AsyncIOMotorClient
import redis.asyncio as redis
import os
from dotenv import load_dotenv

# Charger les variables d'environnement
load_dotenv()

# Configuration MongoDB et Redis
MONGO_URI = os.getenv("MONGO_URI", "mongodb://mongodb:27017")
REDIS_HOST = os.getenv("REDIS_HOST", "redis")
REDIS_PORT = int(os.getenv("REDIS_PORT", 6379))

# Initialisation des clients
mongo_client = AsyncIOMotorClient(MONGO_URI)
mongo_db = mongo_client["nosql_project"]
redis_client = redis.Redis(host=REDIS_HOST, port=REDIS_PORT)

# Initialisation de l'application FastAPI
app = FastAPI()

origins = [
    "http://localhost:3000",
    "http://localhost:8000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class FormData(BaseModel):
    message: str

@app.post("/submit")
async def submit_data(data: FormData):
    try:
        await mongo_db.forms.insert_one(data.dict())

        await redis_client.set("form_data", data.message)

        return {"message": "Data saved in MongoDB and Redis!"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/data/redis")
async def get_redis_data():
    value = await redis_client.get("form_data")
    if value is None:
        return {"error": "Key not found"}
    
    data = value.decode("utf-8")
    
    return {"form_data": data}

@app.get("/data/mongodb")
async def get_mongo_data():
    cursor = mongo_db.forms.find({})
    
    data = []
    async for document in cursor:
        document["_id"] = str(document["_id"])
        data.append(document)
    
    return {"data": data}