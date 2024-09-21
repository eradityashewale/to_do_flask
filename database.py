from pymongo import MongoClient
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

client = MongoClient('mongodb://localhost:27017/')
db = client['todo_db']
todos_collection = db['todos']

# Initialize Limiter
limiter = Limiter(
    get_remote_address,
    default_limits=["200 per day", "50 per hour"]  # Set your rate limits
)
