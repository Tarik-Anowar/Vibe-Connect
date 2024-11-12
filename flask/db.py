from flask_pymongo import PyMongo
from dotenv import load_dotenv
from bson import ObjectId 
import os

# Load environment variables from .env file
load_dotenv()

# Initialize PyMongo
mongo = PyMongo()

def database_connection(app):
    # Configure MongoDB URI
    app.config["MONGO_URI"] = os.getenv("MONGO_URI")
    mongo.init_app(app)

def fetch_all_posts():
    """
    Fetch all posts from the database.
    Returns:
        List of posts (if found), or a list containing a dummy post if no posts exist.
    """
    posts = mongo.db.posts.find()  # Fetch posts from the 'posts' collection
    posts_list = list(posts)  # Convert the cursor to a list

    if not posts_list:  # Check if no posts were found
        # Create a dummy post
        posts_list = [{
            "_id": ObjectId(),  # Generate a new ObjectId
            "topic": "Sample Topic for Testing",
            "description": "This is a dummy post created to test the functionality.",
            "creator": ObjectId(),  # Use a dummy ObjectId for the creator
            "likes": [],
            "dislikes": [],
            "image": "https://example.com/sample-image.jpg"
        }]

    return posts_list  
