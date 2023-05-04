import pymongo
from pymongo.errors import PyMongoError
from utils.JsonResponse import ConvertJsonResponse as cvtJson
from utils.ErrorMessage import errorMessage
from flask import *
import random
from configs.database import Database


class Search(Database):
    def __init__(self):
        self.__db = self.ConnectMongoDB()

    def search(self, type):
        try:
            query = request.args.get("query", default="", type=str)
            page = request.args.get("page", default=1, type=int) - 1
            if type == "multi":
                movie = cvtJson(
                    self.__db["movies"]
                    .find(
                        {
                            "$or": [
                                {"name": {"$regex": query, "$options": "i"}},
                                {"title": {"$regex": query, "$options": "i"}},
                                {"original_title": {"$regex": query, "$options": "i"}},
                                {"original_name": {"$regex": query, "$options": "i"}},
                            ]
                        }
                    )
                    .skip(page * 5)
                    .limit(5)
                    .sort([("views", pymongo.DESCENDING)])
                )

                tv = cvtJson(
                    self.__db["tvs"]
                    .find(
                        {
                            "$or": [
                                {"name": {"$regex": query, "$options": "i"}},
                                {"title": {"$regex": query, "$options": "i"}},
                                {"original_title": {"$regex": query, "$options": "i"}},
                                {"original_name": {"$regex": query, "$options": "i"}},
                            ]
                        }
                    )
                    .skip(page * 10)
                    .limit(10)
                    .sort([("views", pymongo.DESCENDING)])
                )
                result = movie + tv
                # random.shuffle(result)

                return {
                    "results": result,
                    "movie": movie,
                    "tv": tv,
                    # "total": ,
                    # "totalMovie": ,
                    # "totalTv": ,
                }
            elif type == "tv":
                query = request.args.get("query", default="", type=str)

                tv = cvtJson(
                    self.__db["tvs"]
                    .find(
                        {
                            "$or": [
                                {"name": {"$regex": query, "$options": "i"}},
                                {"title": {"$regex": query, "$options": "i"}},
                                {"original_title": {"$regex": query, "$options": "i"}},
                                {"original_name": {"$regex": query, "$options": "i"}},
                            ]
                        }
                    )
                    .skip(page * 10)
                    .limit(10)
                    .sort([("views", pymongo.DESCENDING)])
                )

                return {"results": tv}
            elif type == "movie":
                query = request.args.get("query", default="", type=str)
                movie = cvtJson(
                    self.__db["movies"]
                    .find(
                        {
                            "$or": [
                                {"name": {"$regex": query, "$options": "i"}},
                                {"title": {"$regex": query, "$options": "i"}},
                                {"original_title": {"$regex": query, "$options": "i"}},
                                {"original_name": {"$regex": query, "$options": "i"}},
                            ]
                        }
                    )
                    .skip(page * 10)
                    .limit(10)
                    .sort([("views", pymongo.DESCENDING)])
                )

                return {"results": movie}
            else:
                return errorMessage(400)
        except:
            return {"results": []}
