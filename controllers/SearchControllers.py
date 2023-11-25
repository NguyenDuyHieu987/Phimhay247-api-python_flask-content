import pymongo
from pymongo.errors import PyMongoError
from utils.JsonResponse import ConvertJsonResponse as cvtJson
from utils.ErrorMessage import BadRequestMessage, InternalServerErrorMessage
from utils.exceptions import NotInTypeError
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
            limit = request.args.get("limit", default=20, type=int)

            if type == "all":
                movie = cvtJson(
                    self.__db["movies"]
                    .find(
                        {
                            "$or": [
                                {"name": {"$regex": query, "$options": "i"}},
                                {"original_name": {"$regex": query, "$options": "i"}},
                            ]
                        }
                    )
                    .skip(page * (limit / 2))
                    .limit((limit / 2))
                    .sort([("views", pymongo.DESCENDING)])
                )

                tv = cvtJson(
                    self.__db["tvs"]
                    .find(
                        {
                            "$or": [
                                {"name": {"$regex": query, "$options": "i"}},
                                {"original_name": {"$regex": query, "$options": "i"}},
                            ]
                        }
                    )
                    .skip(page * (limit / 2))
                    .limit((limit / 2))
                    .sort([("views", pymongo.DESCENDING)])
                )

                result = movie + tv

                # random.shuffle(result)

                total_movie = self.__db["movies"].count_documents(
                    {
                        "$or": [
                            {"name": {"$regex": query, "$options": "i"}},
                            {"original_name": {"$regex": query, "$options": "i"}},
                        ]
                    }
                )

                total_tv = self.__db["tvs"].count_documents(
                    {
                        "$or": [
                            {"name": {"$regex": query, "$options": "i"}},
                            {"original_name": {"$regex": query, "$options": "i"}},
                        ]
                    }
                )

                return {
                    "page": page + 1,
                    "results": result,
                    "movie": movie,
                    "tv": tv,
                    "total": total_movie + total_tv,
                    "total_movie": total_movie,
                    "total_tv": total_tv,
                    "page_size": limit,
                }

            elif type == "tv":
                tv = cvtJson(
                    self.__db["tvs"]
                    .find(
                        {
                            "$or": [
                                {"name": {"$regex": query, "$options": "i"}},
                                {"original_name": {"$regex": query, "$options": "i"}},
                            ]
                        }
                    )
                    .skip(page * limit)
                    .limit(limit)
                    .sort([("views", pymongo.DESCENDING)])
                )

                total = self.__db["tvs"].count_documents(
                    {
                        "$or": [
                            {"name": {"$regex": query, "$options": "i"}},
                            {"original_name": {"$regex": query, "$options": "i"}},
                        ]
                    }
                )

                return {
                    "page": page + 1,
                    "results": tv,
                    "total": total,
                    "page_size": limit,
                }
            elif type == "movie":
                movie = cvtJson(
                    self.__db["movies"]
                    .find(
                        {
                            "$or": [
                                {"name": {"$regex": query, "$options": "i"}},
                                {"original_name": {"$regex": query, "$options": "i"}},
                            ]
                        }
                    )
                    .skip(page * limit)
                    .limit(limit)
                    .sort([("views", pymongo.DESCENDING)])
                )

                total = self.__db["movies"].count_documents(
                    {
                        "$or": [
                            {"name": {"$regex": query, "$options": "i"}},
                            {"original_name": {"$regex": query, "$options": "i"}},
                        ]
                    }
                )

                return {
                    "page": page + 1,
                    "results": movie,
                    "total": total,
                    "page_size": limit,
                }
            else:
                raise NotInTypeError("search", type)
        except PyMongoError as e:
            InternalServerErrorMessage(e._message)
        except NotInTypeError as e:
            BadRequestMessage(e.message)
        except Exception as e:
            InternalServerErrorMessage(e)
