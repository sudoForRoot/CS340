from pymongo import MongoClient
from pymongo.errors import PyMongoError
import pandas as pd

class AnimalShelter:
    def __init__(self, username, password):
        self.client = MongoClient(f'mongodb://{username}:{password}@localhost:27017/AAC')
        self.database = self.client['AAC']
        self.collection = self.database['animals']
        
    def create(self, data):
        try:
            if data is not None:
                result = self.collection.insert_one(data)
                return result.acknowledged
            else:
                raise Exception("Nothing to save, because data parameter is empty")
        except PyMongoError as e:
            print(f"Error creating record: {e}")
            return False
            
    def read(self, query):
        try:
            if query is not None:
                data = pd.DataFrame(list(self.collection.find(query, {"_id": 0})))
                return data
            else:
                raise Exception("Nothing to read, because query parameter is empty")
        except PyMongoError as e:
            print(f"Error reading records: {e}")
            return pd.DataFrame()
            
    def update(self, query, update_data):
        try:
            if query is not None and update_data is not None:
                result = self.collection.update_many(query, {"$set": update_data})
                return result.modified_count
            else:
                raise Exception("Parameters cannot be empty")
        except PyMongoError as e:
            print(f"Error updating records: {e}")
            return 0
            
    def delete(self, query):
        try:
            if query is not None:
                result = self.collection.delete_many(query)
                return result.deleted_count
            else:
                raise Exception("Nothing to delete, because query parameter is empty")
        except PyMongoError as e:
            print(f"Error deleting records: {e}")
            return 0
            
    # Specialized query methods for rescue types
    def get_water_rescue_dogs(self):
        query = {
            "animal_type": "Dog",
            "breed": {"$in": ["Labrador Retriever Mix", "Newfoundland Mix", "Portuguese Water Dog Mix"]},
            "age_upon_outcome_in_weeks": {"$gte": 26, "$lte": 156}
        }
        return self.read(query)
        
    def get_mountain_rescue_dogs(self):
        query = {
            "animal_type": "Dog",
            "breed": {"$in": ["German Shepherd Mix", "Alaskan Malamute Mix", "Old English Sheepdog Mix", 
                             "Siberian Husky Mix", "Rottweiler Mix"]},
            "age_upon_outcome_in_weeks": {"$gte": 26, "$lte": 156}
        }
        return self.read(query)
        
    def get_disaster_rescue_dogs(self):
        query = {
            "animal_type": "Dog",
            "breed": {"$in": ["Doberman Pinscher Mix", "German Shorthaired Pointer Mix", 
                             "Bloodhound Mix", "Golden Retriever Mix"]},
            "age_upon_outcome_in_weeks": {"$gte": 20, "$lte": 300}
        }
        return self.read(query)