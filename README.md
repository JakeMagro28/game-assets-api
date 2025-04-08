# Game Asset API

This is a FastAPI-based backend application for handling game assets like sprites, audio files, and player scores. It uses MongoDB Atlas as the backend database.

---

## 🚀 Features

- Upload and retrieve sprites, audio, and player scores
- Credentials securely stored using `.env`
- Fully documented with Swagger UI
- Ready for deployment

---

## 📁 Project Structure



Project structure

game-assets-api/ 
├── main.py # FastAPI app with all routes and models 
├── .env.example # Example config (without secrets) 
├── requirements.txt # Frozen list of dependencies 
├── README.md # Setup instructions and project overview


Setup instructions 
Clone the Repository 

git clone https://github.com/your-username/game-assets-api.git
cd game-assets-api

create Virtual Environment
python -m venv env
# Activate the virtual environment
# On Windows:
.\env\Scripts\activate
# On Mac/Linux:
source env/bin/activate


Install Dependencies
pip install -r requirements.txt

Configure Environment Variables
create a .env file based on .env.example 

MONGO_URI=mongodb+srv://<username>:<password>@cluster0.mongodb.net/multimedia_db

Run the API 

uvicorn main:app --reload

Then Go to http://127.0.0.1:8000/docs

API Endpoint overview

sprites 
POST /upload_sprite -Upload a sprite
GET /sprites -Get all sprites

Audio 
POST /upload_audio -Upload an audio asset
GET /audio -Get all audio entries

Scores
POST /player_score -submit a player score
GET /player_scores  -Get all player scores


Security 
MongoDB URI is stored in .env (excluded from GitHub)

.env.example provided for environment setup

Input validation via Pydantic constr() — protects against injection & blank fields

Author 
Developed by Jake Magro
For Database Essentials Home Assignment = Game asset API


Notes 

MongoDB Notes
“Collections are automatically created when first data is inserted.”

“No authentication is applied to endpoints (for simplicity of assignment).”

FastAPI Notes
“Swagger UI available at /docs for easy API testing.”

“FastAPI automatically validates input formats using Pydantic models.”

Validation/Security Notes
“Pydantic constraints prevent injection by rejecting empty or malformed input fields.”

“All sensitive credentials are stored in a .env file, excluded from version control.”