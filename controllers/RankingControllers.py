import pymongo
from pymongo.errors import PyMongoError
from utils.JsonResponse import ConvertJsonResponse as cvtJson
from utils.ErrorMessage import BadRequestMessage, InternalServerErrorMessage
from utils.exceptions import NotInTypeError
from flask import *
from configs.database import Database


class Rank(Database):
    def __init__(self):
        self.__db = self.ConnectMongoDB()

    def ranking(self, slug):
        try:
            page = request.args.get("page", default=1, type=int) - 1
            limit = request.args.get("limit", default=20, type=int)

            if slug == "day":
                movie = (
                    self.__db["movies"]
                    .find({})
                    .skip(0 * limit / 2)
                    .limit(limit / 2)
                    .sort([("views", pymongo.DESCENDING)])
                )

                tv = (
                    self.__db["tvs"]
                    .find({})
                    .skip(0 * limit / 2)
                    .limit(limit / 2)
                    .sort([("views", pymongo.DESCENDING)])
                )

                return {
                    "page": page + 1,
                    "results": cvtJson(movie + tv),
                    "page_size": limit,
                }
            elif slug == "week":
                movie = (
                    self.__db["movies"]
                    .find({})
                    .skip(1 * limit / 2)
                    .limit(limit / 2)
                    .sort([("views", pymongo.DESCENDING)])
                )

                tv = (
                    self.__db["tvs"]
                    .find({})
                    .skip(1 * limit / 2)
                    .limit(limit / 2)
                    .sort([("views", pymongo.DESCENDING)])
                )

                return {
                    "page": page + 1,
                    "results": cvtJson(movie + tv),
                    "page_size": limit,
                }
            elif slug == "month":
                movie = (
                    self.__db["movies"]
                    .find({})
                    .skip(2 * limit / 2)
                    .limit(limit / 2)
                    .sort([("views", pymongo.DESCENDING)])
                )

                tv = (
                    self.__db["tvs"]
                    .find({})
                    .skip(2 * limit / 2)
                    .limit(limit / 2)
                    .sort([("views", pymongo.DESCENDING)])
                )

                return {
                    "page": page + 1,
                    "results": cvtJson(movie + tv),
                    "page_size": limit,
                }
            elif slug == "all":
                movie = (
                    self.__db["movies"]
                    .find({})
                    .skip(3 * limit / 2)
                    .limit(limit / 2)
                    .sort([("views", pymongo.DESCENDING)])
                )

                tv = (
                    self.__db["tvs"]
                    .find({})
                    .skip(3 * limit / 2)
                    .limit(limit / 2)
                    .sort([("views", pymongo.DESCENDING)])
                )

                return {
                    "page": page + 1,
                    "results": cvtJson(movie + tv),
                    "page_size": limit,
                }
            else:
                raise NotInTypeError("ranking", type)
        except PyMongoError as e:
            InternalServerErrorMessage(e._message)
        except NotInTypeError as e:
            BadRequestMessage(e.message)
        except Exception as e:
            InternalServerErrorMessage(e)
