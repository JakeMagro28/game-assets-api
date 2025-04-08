from fastapi import FastAPI
from pydantic import BaseModel
from pymongo import MongoClient
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = FastAPI()

# MongoDB connection
client = MongoClient(os.getenv("MONGO_URI"))
db = client.multimedia_db  # Your database name (change if needed)

# Mongo collections
sprites_collection = db.sprites
audio_collection = db.audio
scores_collection = db.scores

# Models

class Sprite(BaseModel):
    sprite_name: str
    sprite_image: str
    size: str
    created_at: str

class Audio(BaseModel):
    audio_name: str
    audio_file: str
    duration: float
    created_at: str

class PlayerScore(BaseModel):
    player_name: str
    score: int
    level: int
    timestamp: str

# Routes

@app.get("/")
def read_root():
    return {"message": "Hello, FastAPI is working!"}

@app.get("/test_connection")
def test_connection():
    try:
        count = scores_collection.count_documents({})
        return {"message": "Connected to MongoDB!", "scores_count": count}
    except Exception as e:
        return {"message": "Error connecting to MongoDB", "error": str(e)}

@app.post("/upload_sprite")
def upload_sprite(sprite: Sprite):
    sprite_data = sprite.dict()
    result = sprites_collection.insert_one(sprite_data)
    sprite_data["_id"] = str(result.inserted_id)
    return {"message": "Sprite uploaded!", "data": sprite_data}

@app.post("/upload_audio")
def upload_audio(audio: Audio):
    audio_data = audio.dict()
    result = audio_collection.insert_one(audio_data)
    audio_data["_id"] = str(result.inserted_id)
    return {"message": "Audio uploaded!", "data": audio_data}

@app.post("/player_score")
def add_score(score: PlayerScore):
    score_data = score.dict()
    result = scores_collection.insert_one(score_data)
    score_data["_id"] = str(result.inserted_id)
    return {"message": "Score received!", "data": score_data}
