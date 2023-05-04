import pymongo
from pymongo.errors import PyMongoError
from utils.JsonResponse import ConvertJsonResponse as cvtJson
from utils.ErrorMessage import errorMessage
from flask import *
from pymongo import ReturnDocument
from configs.database import Database


class Trend(Database):
    def __init__(self):
        self.__db = self.ConnectMongoDB()

    def trending(self, type):
        try:
            if type == "all":
                page = request.args.get("page", default=1, type=int)
                trending = cvtJson(self.__db["trendings"].find_one({"page": page}))
                return {
                    "page": page,
                    "results": trending["results"],
                    "total_pages": trending["total_pages"],
                }
            else:
                return errorMessage(400)
        except:
            return {"results": [], "total_pages": 0}
