from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

# Model for incoming score data
class PlayerScore(BaseModel):
    player_name: str
    score: int

@app.get("/")
def read_root():
    return {"message": "Hello, FastAPI is working!"}

@app.post("/player_score")
def add_score(score: PlayerScore):
    # For now, just return the data back (we'll connect to MongoDB later)
    return {"message": "Score received!", "data": score}
