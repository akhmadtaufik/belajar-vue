from flask import Blueprint
from flask_cors import CORS

tweetBp = Blueprint("tweet", __name__)
CORS(tweetBp, resources={r"/api/*": {"origins": "http://localhost:5173"}})
from app.tweet import routes
