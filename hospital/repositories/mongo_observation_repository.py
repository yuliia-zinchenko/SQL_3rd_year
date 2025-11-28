import os
from pymongo import MongoClient
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

class ObservationRepository:
    def __init__(self, use_local=False):
        if use_local:
            CONNECTION_STRING = "mongodb://localhost:27017/"
        else:

            CONNECTION_STRING = os.getenv("MONGO_CONNECTION_STRING")
            if not CONNECTION_STRING:
                raise ValueError("No MONGO_CONNECTION_STRING found in .env file")
        
        client = MongoClient(CONNECTION_STRING)
        self.db = client['hospital_nosql_db']
        self.collection = self.db['medical_observations']
    def add_observation(self, record_id, observation_type, results, notes=""):
        document = {
            "record_id": record_id, 
            "observation_date": datetime.utcnow(),
            "type": observation_type,
            "results": results,
            "doctor_notes": notes
        }
        result = self.collection.insert_one(document)
        print(f"MongoDB: Observation for record_id {record_id} added.")
        return result.inserted_id

    def get_observations_by_record_id(self, record_id):
        print(f"MongoDB: Fetching observations for record_id {record_id}.")
        return list(self.collection.find({"record_id": record_id}))