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

# Model for incoming score data
class PlayerScore(BaseModel):
    player_name: str
    score: int

@app.get("/")
def read_root():
    return {"message": "Hello, FastAPI is working!"}

@app.post("/player_score")
def add_score(score: PlayerScore):
    # Insert the score into MongoDB
    score_data = {"player_name": score.player_name, "score": score.score}
    result = scores_collection.insert_one(score_data)
    return {"message": "Score received!", "data": score_data, "id": str(result.inserted_id)}

@app.get("/test_connection")
def test_connection():
    try:
        # Try fetching something from the "scores" collection to test the connection
        count = scores_collection.count_documents({})
        return {"message": "Connected to MongoDB!", "scores_count": count}
    except Exception as e:
        return {"message": "Error connecting to MongoDB", "error": str(e)}
