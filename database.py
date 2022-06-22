from pymongo import MongoClient
from dotenv import load_dotenv
import os
import certifi

class MongoDB:
    def __init__(self):
        # load .env
        load_dotenv()

        # Connect DB
        ca = certifi.where()
        mongo_url = os.environ.get('MONGO_URL')
        self.client = MongoClient(mongo_url, tlsCAFile=ca)
        self.db = self.client.dev_interview