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
                    .skip(page * 10)
                    .limit(10)
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

                total_movie = cvtJson(
                    self.__db["movies"].find(
                        {
                            "$or": [
                                {"name": {"$regex": query, "$options": "i"}},
                                {"title": {"$regex": query, "$options": "i"}},
                                {"original_title": {"$regex": query, "$options": "i"}},
                                {"original_name": {"$regex": query, "$options": "i"}},
                            ]
                        }
                    )
                )

                total_tv = cvtJson(
                    self.__db["tvs"].find(
                        {
                            "$or": [
                                {"name": {"$regex": query, "$options": "i"}},
                                {"title": {"$regex": query, "$options": "i"}},
                                {"original_title": {"$regex": query, "$options": "i"}},
                                {"original_name": {"$regex": query, "$options": "i"}},
                            ]
                        }
                    )
                )

                return {
                    "results": result,
                    "movie": movie,
                    "tv": tv,
                    "total": len(total_movie) + len(total_tv),
                    "total_movie": len(total_movie),
                    "total_tv": len(total_tv),
                    "page_size": 20,
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
                    .skip(page * 20)
                    .limit(20)
                    .sort([("views", pymongo.DESCENDING)])
                )

                total = cvtJson(
                    self.__db["tvs"].find(
                        {
                            "$or": [
                                {"name": {"$regex": query, "$options": "i"}},
                                {"title": {"$regex": query, "$options": "i"}},
                                {"original_title": {"$regex": query, "$options": "i"}},
                                {"original_name": {"$regex": query, "$options": "i"}},
                            ]
                        }
                    )
                )

                return {
                    "results": tv,
                    "total": len(total),
                    "page_size": 20,
                }
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
                    .skip(page * 20)
                    .limit(20)
                    .sort([("views", pymongo.DESCENDING)])
                )
                total = cvtJson(
                    self.__db["movies"].find(
                        {
                            "$or": [
                                {"name": {"$regex": query, "$options": "i"}},
                                {"title": {"$regex": query, "$options": "i"}},
                                {"original_title": {"$regex": query, "$options": "i"}},
                                {"original_name": {"$regex": query, "$options": "i"}},
                            ]
                        }
                    )
                )

                return {
                    "results": movie,
                    "total": len(total),
                    "page_size": 20,
                }
            else:
                return errorMessage(400)
        except:
            return {"results": []}
