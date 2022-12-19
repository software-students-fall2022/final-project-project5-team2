from pymongo import MongoClient
from dotenv import load_dotenv
import certifi

import os

class Database(object):

    load_dotenv()
    url = os.getenv('MONGODB_CONNSTRING')
    database=None
    client=None
    ca = certifi.where()
    
    @staticmethod
    def initialize():
        connection= MongoClient(Database.url, tlsCAFile=Database.ca)
        try:
            Database.client=connection
            Database.database = connection.app
            print(' *', 'Connected to MongoDB!') 
        except Exception as e:
            print(' *', "Failed to connect to MongoDB at")
            print('Database connection error:', e)

    @staticmethod
    def insert_one(collection, data):
        return Database.database[collection].insert_one(data)

    @staticmethod
    def find(collection, query="", field=""):
        return (Database.database[collection].find(query,field))

    @staticmethod  
    def get_all(collection):
        return Database.find(collection)

    @staticmethod
    def find_single(collection, query, field=""):
        return (Database.database[collection].find_one(query,field))

    @staticmethod
    def delete(collection, query):
        return Database.database[collection].delete_one(query)

    @staticmethod
    def update(collection, search, query):
        return Database.database[collection].update_one(search,query)

    @staticmethod
    def count(collection, query):
        return Database.database[collection].count_documents(query)

    @staticmethod
    def close():
        Database.client.close()