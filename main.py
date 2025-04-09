from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, constr
from pymongo import MongoClient
from bson import ObjectId
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Initialize FastAPI application
app = FastAPI()

# MongoDB connection setup using environment variable
client = MongoClient(os.getenv("MONGO_URI"))
db = client.multimedia_db  # Database name

# Define MongoDB collections
sprites_collection = db.sprites
audio_collection = db.audio
scores_collection = db.scores

# ------------------ Pydantic Models with Input Validation ------------------ #

class Sprite(BaseModel):
    sprite_name: constr(strip_whitespace=True, min_length=1, max_length=50)
    sprite_image: constr(strip_whitespace=True, min_length=5)
    size: constr(strip_whitespace=True, min_length=3)
    created_at: constr(strip_whitespace=True, min_length=5)

class Audio(BaseModel):
    audio_name: constr(strip_whitespace=True, min_length=1, max_length=50)
    audio_file: constr(strip_whitespace=True, min_length=5)
    duration: float
    created_at: constr(strip_whitespace=True, min_length=5)

class PlayerScore(BaseModel):
    player_name: constr(strip_whitespace=True, min_length=1, max_length=30)
    score: int
    level: int
    timestamp: constr(strip_whitespace=True, min_length=5)

# ------------------ API Endpoints ------------------ #

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

# ------- SPRITES -------

@app.post("/upload_sprite")
def upload_sprite(sprite: Sprite):
    sprite_data = sprite.dict()
    result = sprites_collection.insert_one(sprite_data)
    sprite_data["_id"] = str(result.inserted_id)
    return {"message": "Sprite uploaded!", "data": sprite_data}

@app.get("/sprites")
def get_sprites():
    sprites = list(sprites_collection.find())
    for s in sprites:
        s["_id"] = str(s["_id"])
    return {"sprites": sprites}

@app.delete("/delete_sprite/{sprite_id}")
def delete_sprite(sprite_id: str):
    result = sprites_collection.delete_one({"_id": ObjectId(sprite_id)})
    if result.deleted_count == 1:
        return {"message": f"Sprite {sprite_id} deleted successfully"}
    raise HTTPException(status_code=404, detail="Sprite not found")

# ------- AUDIO -------

@app.post("/upload_audio")
def upload_audio(audio: Audio):
    audio_data = audio.dict()
    result = audio_collection.insert_one(audio_data)
    audio_data["_id"] = str(result.inserted_id)
    return {"message": "Audio uploaded!", "data": audio_data}

@app.get("/audio")
def get_audio():
    audio = list(audio_collection.find())
    for a in audio:
        a["_id"] = str(a["_id"])
    return {"audio": audio}

@app.delete("/delete_audio/{audio_id}")
def delete_audio(audio_id: str):
    result = audio_collection.delete_one({"_id": ObjectId(audio_id)})
    if result.deleted_count == 1:
        return {"message": f"Audio {audio_id} deleted successfully"}
    raise HTTPException(status_code=404, detail="Audio not found")

# ------- SCORES -------

@app.post("/player_score")
def add_score(score: PlayerScore):
    score_data = score.dict()
    result = scores_collection.insert_one(score_data)
    score_data["_id"] = str(result.inserted_id)
    return {"message": "Score received!", "data": score_data}

@app.get("/player_scores")
def get_scores():
    scores = list(scores_collection.find())
    for s in scores:
        s["_id"] = str(s["_id"])
    return {"scores": scores}

@app.delete("/delete_score/{score_id}")
def delete_score(score_id: str):
    result = scores_collection.delete_one({"_id": ObjectId(score_id)})
    if result.deleted_count == 1:
        return {"message": f"Score {score_id} deleted successfully"}
    raise HTTPException(status_code=404, detail="Score not found")
