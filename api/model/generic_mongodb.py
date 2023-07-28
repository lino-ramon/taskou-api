import pymongo
import os
from bson import json_util

class GenericMongoDB(object):
    db_host: str
    db_port: int
    db_user: str
    db_password: str
    db_autosource: str
    db_name: str

    def __init__(self) -> None:
        self.db_host = os.getenv('MONGO_HOST', "localhost")
        self.db_port = int(os.getenv('MONGO_PORT', 27017))
        self.db_user = os.getenv('MONGO_USER', "root")
        self.db_password = os.getenv('MONGO_PASSWORD', "taskouMONGODB1")
        self.db_autosource = os.getenv('MONGO_AUTOSOURCE', "admin")
        self.db_name = os.getenv('MONGO_NAME', "taskoudb")
        self.mongo_database = self.connect()

    def connect(self):
        return pymongo.MongoClient(
            host=self.db_host,
            port=self.db_port,
            username=self.db_user,
            password=self.db_password
        ).get_database(self.db_name)

    def get_collection(self, collection: str):
        return self.mongo_database[collection]