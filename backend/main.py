import os
import motor.motor_asyncio
import asyncio
import asyncpg
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

# Charger les variables d'environnement
load_dotenv()

# Configuration MongoDB
MONGO_URI = os.getenv("MONGO_URI", "mongodb://mongodb:27017")
mongo_client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_URI)
mongo_db = mongo_client["nosql_project"]

# Configuration PostgreSQL
POSTGRES_USER = os.getenv("POSTGRES_USER", "user")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD", "password")
POSTGRES_DB = os.getenv("POSTGRES_DB", "nosql_project")
POSTGRES_HOST = os.getenv("POSTGRES_HOST", "postgres")
POSTGRES_PORT = os.getenv("POSTGRES_PORT", "5432")

# Initialisation de FastAPI
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Connexion PostgreSQL
async def get_postgres_connection():
    for _ in range(5):  # Réessayer 5 fois
        try:
            conn = await asyncpg.connect(
                user=POSTGRES_USER,
                password=POSTGRES_PASSWORD,
                database=POSTGRES_DB,
                host=POSTGRES_HOST,
                port=POSTGRES_PORT,
            )
            await conn.execute("""
            CREATE TABLE IF NOT EXISTS form_data (
                id SERIAL PRIMARY KEY,
                message TEXT NOT NULL
            );
            """)
            return conn
        except Exception as e:
            print(f"PostgreSQL connection failed: {e}. Retrying...")
            await asyncio.sleep(5)  # Attendre 5 secondes avant de réessayer
    raise HTTPException(status_code=500, detail="Unable to connect to PostgreSQL.")


# Modèle de données
class FormData(BaseModel):
    message: str

# Route pour soumettre des données (MongoDB et PostgreSQL)
@app.post("/submit")
async def submit_data(data: FormData):
    try:
        # Sauvegarde dans MongoDB
        mongo_collection = mongo_db.get_collection("form_data")
        await mongo_collection.insert_one({"message": data.message})

        # Sauvegarde dans PostgreSQL
        conn = await get_postgres_connection()
        await conn.execute(
            "INSERT INTO form_data(message) VALUES($1)", data.message
        )
        await conn.close()

        return {"message": "Data saved in MongoDB and PostgreSQL!"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Route pour récupérer les données de PostgreSQL
@app.get("/data/postgres")
async def get_postgres_data():
    try:
        conn = await get_postgres_connection()
        result = await conn.fetch("SELECT id, message FROM form_data")
        await conn.close()

        data = [{"id": record["id"], "message": record["message"]} for record in result]
        return {"form_data": data}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Route pour récupérer les données de MongoDB
@app.get("/data/mongodb")
async def get_mongo_data():
    try:
        mongo_collection = mongo_db.get_collection("form_data")
        cursor = mongo_collection.find()

        data = [{"_id": str(record["_id"]), "message": record["message"]} for record in await cursor.to_list(length=100)]
        return {"form_data": data}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
