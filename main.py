from fastapi import FastAPI
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
    """
    Represents metadata for a game sprite asset.
    """
    sprite_name: constr(strip_whitespace=True, min_length=1, max_length=50)
    sprite_image: constr(strip_whitespace=True, min_length=5)  # Ensure it's a valid URL format
    size: constr(strip_whitespace=True, min_length=3)  # e.g. "1024x1024"
    created_at: constr(strip_whitespace=True, min_length=5)  # ISO date string


class Audio(BaseModel):
    """
    Represents metadata for an audio asset.
    """
    audio_name: constr(strip_whitespace=True, min_length=1, max_length=50)
    audio_file: constr(strip_whitespace=True, min_length=5)  # URL or file path
    duration: float  # Duration in seconds
    created_at: constr(strip_whitespace=True, min_length=5)  # ISO date string


class PlayerScore(BaseModel):
    """
    Represents a player's score submission.
    """
    player_name: constr(strip_whitespace=True, min_length=1, max_length=30)
    score: int
    level: int
    timestamp: constr(strip_whitespace=True, min_length=5)  # ISO timestamp

# ------------------ API Endpoints ------------------ #

@app.get("/")
def read_root():
    """
    Root endpoint to verify the API is running.
    """
    return {"message": "Hello, FastAPI is working!"}


@app.get("/test_connection")
def test_connection():
    """
    Tests MongoDB connection by returning the number of score documents.
    """
    try:
        count = scores_collection.count_documents({})
        return {"message": "Connected to MongoDB!", "scores_count": count}
    except Exception as e:
        return {"message": "Error connecting to MongoDB", "error": str(e)}


@app.post("/upload_sprite")
def upload_sprite(sprite: Sprite):
    """
    Uploads a new sprite document to the MongoDB sprites collection.
    """
    sprite_data = sprite.dict()
    result = sprites_collection.insert_one(sprite_data)
    sprite_data["_id"] = str(result.inserted_id)
    return {"message": "Sprite uploaded!", "data": sprite_data}


@app.get("/sprites")
def get_sprites():
    """
    Retrieves all sprite documents from the database.
    """
    sprites = list(sprites_collection.find())
    for s in sprites:
        s["_id"] = str(s["_id"])  # Convert ObjectId to string
    return {"sprites": sprites}


@app.post("/upload_audio")
def upload_audio(audio: Audio):
    """
    Uploads a new audio document to the MongoDB audio collection.
    """
    audio_data = audio.dict()
    result = audio_collection.insert_one(audio_data)
    audio_data["_id"] = str(result.inserted_id)
    return {"message": "Audio uploaded!", "data": audio_data}


@app.get("/audio")
def get_audio():
    """
    Retrieves all audio documents from the database.
    """
    audio = list(audio_collection.find())
    for a in audio:
        a["_id"] = str(a["_id"])
    return {"audio": audio}


@app.post("/player_score")
def add_score(score: PlayerScore):
    """
    Uploads a new player score to the MongoDB scores collection.
    """
    score_data = score.dict()
    result = scores_collection.insert_one(score_data)
    score_data["_id"] = str(result.inserted_id)
    return {"message": "Score received!", "data": score_data}


@app.get("/player_scores")
def get_scores():
    """
    Retrieves all player scores from the database.
    """
    scores = list(scores_collection.find())
    for s in scores:
        s["_id"] = str(s["_id"])
    return {"scores": scores}
