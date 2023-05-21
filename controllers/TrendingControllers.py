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
                page = request.args.get("page", default=1, type=int) - 1
                trending = cvtJson(
                    self.__db["trendings"].find({}).skip(page * 20).limit(20)
                )
                return {
                    "page": page,
                    "results": trending,
                    "total": self.__db["trendings"].count_documents({}),
                    "page_size": 20,
                }
            else:
                return errorMessage(400)
        except:
            return {"results": [], "total_pages": 0}
