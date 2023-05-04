import pymongo
from pymongo.errors import PyMongoError
from utils.JsonResponse import ConvertJsonResponse as cvtJson
from utils.ErrorMessage import errorMessage
from flask import *
from configs.database import Database


class Sortby(Database):
    def __init__(self):
        self.__db = self.ConnectMongoDB()

    def sortby(self, type):
        try:
            if type == "all":
                all_sortbys = cvtJson(self.__db["sortbys"].find())
                return all_sortbys
            else:
                return errorMessage(400)
        except:
            return []
