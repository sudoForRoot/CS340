from pymongo import MongoClient
from pymongo.errors import PyMongoError

class CRUD:
    """
    A class to perform CRUD operations on MongoDB database.
    
    Attributes:
        client (MongoClient): MongoDB client connection
        db (Database): MongoDB database reference
        collection (Collection): MongoDB collection reference
    """
    
    def __init__(self, db_name, collection_name, username=None, password=None, host='localhost', port=27017):
        """
        Initialize the CRUD object with database connection details.
        
        Args:
            db_name (str): Name of the database
            collection_name (str): Name of the collection
            username (str, optional): MongoDB username. Defaults to None.
            password (str, optional): MongoDB password. Defaults to None.
            host (str, optional): MongoDB host. Defaults to 'localhost'.
            port (int, optional): MongoDB port. Defaults to 27017.
        """
        try:
            if username and password:
                self.client = MongoClient(
                    host=host,
                    port=port,
                    username=username,
                    password=password,
                    authSource=db_name,
                    authMechanism='SCRAM-SHA-1'
                )
            else:
                self.client = MongoClient(host, port)
                
            self.db = self.client[db_name]
            self.collection = self.db[collection_name]
            
        except PyMongoError as e:
            print(f"Error connecting to MongoDB: {e}")
            raise

    def create(self, document):
        """
        Insert a document into the collection.
        
        Args:
            document (dict): Document to insert
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            result = self.collection.insert_one(document)
            return result.acknowledged
        except PyMongoError as e:
            print(f"Error creating document: {e}")
            return False

    def read(self, query):
        """
        Query for documents in the collection.
        
        Args:
            query (dict): Query criteria
            
        Returns:
            list: List of matching documents (empty list if none found)
        """
        try:
            cursor = self.collection.find(query)
            return list(cursor)
        except PyMongoError as e:
            print(f"Error reading documents: {e}")
            return []

    def update(self, query, update_data):
        """
        Update documents matching the query.
        
        Args:
            query (dict): Query criteria
            update_data (dict): Update operations and values
            
        Returns:
            int: Number of documents modified
        """
        try:
            result = self.collection.update_many(query, update_data)
            return result.modified_count
        except PyMongoError as e:
            print(f"Error updating documents: {e}")
            return 0

    def delete(self, query):
        """
        Delete documents matching the query.
        
        Args:
            query (dict): Query criteria
            
        Returns:
            int: Number of documents deleted
        """
        try:
            result = self.collection.delete_many(query)
            return result.deleted_count
        except PyMongoError as e:
            print(f"Error deleting documents: {e}")
            return 0

    def __del__(self):
        """Close the MongoDB connection when the object is destroyed."""
        if hasattr(self, 'client'):
            self.client.close()