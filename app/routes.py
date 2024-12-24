from flask import Blueprint, render_template, jsonify
import subprocess
from pymongo import MongoClient
from config import MONGO_URI


app_routes = Blueprint('app_routes', __name__)

# MongoDB connection
client = MongoClient(MONGO_URI)
db = client['twitter_trends']
collection = db['trends']

@app_routes.route('/')
def home():
    return render_template('index.html')

@app_routes.route('/run-script', methods=['POST'])
def run_script():
    # Run the Selenium script
    result = subprocess.run(["python", "scripts/selenium_script.py"], capture_output=True, text=True)
    return jsonify({"message": "Script executed successfully!"})

@app_routes.route('/results', methods=['GET'])
def results():
    # Fetch results from MongoDB
    trends = list(collection.find({}, {"_id": 0}))
    return jsonify(trends)
