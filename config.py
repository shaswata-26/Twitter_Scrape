from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# ProxyMesh credentials
PROXY_USER = os.getenv("PROXY_USER")
PROXY_PASS = os.getenv("PROXY_PASS")

# Twitter credentials
TWITTER_USER = os.getenv("TWITTER_USER")
TWITTER_PASS = os.getenv("TWITTER_PASS")

# MongoDB connection string
MONGO_URI = os.getenv("MONGO_URI")

