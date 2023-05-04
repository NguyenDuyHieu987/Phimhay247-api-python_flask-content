import pymongo
from pymongo.errors import PyMongoError
from utils.JsonResponse import ConvertJsonResponse as cvtJson
from utils.ErrorMessage import errorMessage
from flask import *
from configs.database import Database


class Year(Database):
    def __init__(self):
        self.__db = self.ConnectMongoDB()

    def years(self, type):
        try:
            if type == "all":
                genres = cvtJson(self.__db["years"].find())
                return genres
            else:
                return errorMessage(400)
        except:
            return []
