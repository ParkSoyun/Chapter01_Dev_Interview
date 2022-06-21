from flask import Flask, render_template, request, jsonify
from pymongo import MongoClient
from dotenv import load_dotenv
import os

# load .env
load_dotenv()

# Connect DB
mongo_url = os.environ.get('MONGO_URL')
client = MongoClient(mongo_url)
db = client.dbsparta

app = Flask(__name__)


@app.route('/')
def home():
    return render_template('index.html', signIn = False)


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)
