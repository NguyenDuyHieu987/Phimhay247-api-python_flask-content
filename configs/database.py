import pymongo
import os


class Database:
    def __init__(self):
        self.__dbMongo = None

    def ConnectMongoDB(self):
        try:
            myclient = pymongo.MongoClient(os.getenv("MONGODB_URI"))

            self.__dbMongo = myclient["Phimhay247_DB"]
            return self.__dbMongo
        except:
            pass
