import pymongo
from pymongo.errors import PyMongoError
from utils.JsonResponse import ConvertJsonResponse as cvtJson
from utils.ErrorMessage import errorMessage
from flask import *
from configs.database import Database


# myclient = pymongo.MongoClient(
#     "mongodb+srv://admin:hieusen123@the-movie-database.fczrzon.mongodb.net/Phimhay247_DB"
# )

# db = myclient["Phimhay247_DB"]


class Genre(Database):
    def __init__(self):
        self.__db = self.ConnectMongoDB()

    def genres(self, type):
        try:
            if type == "all":
                genres = cvtJson(self.__db["genres"].find())
                return genres
            else:
                return errorMessage(400)
        except:
            return []
