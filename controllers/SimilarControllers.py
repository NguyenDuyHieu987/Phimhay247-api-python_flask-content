import pymongo
from pymongo.errors import PyMongoError
from collections import ChainMap
from utils.JsonResponse import ConvertJsonResponse as cvtJson
from utils.ErrorMessage import BadRequestMessage, InternalServerErrorMessage
from utils.exceptions import NotInTypeError
from flask import *
from configs.database import Database
from utils.exceptions import DefaultError


class Similar(Database):
    def __init__(self):
        self.__db = self.ConnectMongoDB()

    def get_similar(self, type, movieid):
        try:
            page = request.args.get("page", default=1, type=int) - 1
            limit = request.args.get("limit", default=12, type=int)

            if type == "movie":
                movie = self.__db["movies"].find_one({"id": str(movieid)})

                if tv != None:
                    genres = movie["genres"]
                    country = movie["original_language"]

                    new_genres = [{"id": int(x["id"])} for x in genres]

                    movie_similar = cvtJson(
                        self.__db["movies"]
                        .find(
                            {
                                "id": {
                                    "$nin": [str(movieid)],
                                },
                                "$or": [
                                    {"original_language": {"$regex": country}},
                                    {
                                        "genres": {
                                            "$elemMatch": {
                                                "$or": [ChainMap(*new_genres)]
                                            }
                                        }
                                    },
                                ],
                            },
                        )
                        .skip(page * limit)
                        .limit(limit)
                        .sort([("views", pymongo.DESCENDING)])
                    )
                    return {
                        "page": page + 1,
                        "results": movie_similar,
                        "page_size": limit,
                    }
                else:
                    raise DefaultError("Movie is not exist")

            elif type == "tv":
                tv = self.__db["tvs"].find_one({"id": str(movieid)})

                if tv != None:
                    genres = tv["genres"]
                    country = tv["original_language"]

                    new_genres = [{"id": int(x["id"])} for x in genres]

                    tv_similar = cvtJson(
                        self.__db["tvs"]
                        .find(
                            {
                                "id": {
                                    "$nin": [str(movieid)],
                                },
                                "$or": [
                                    {"original_language": {"$regex": country}},
                                    {
                                        "genres": {
                                            "$elemMatch": {
                                                "$or": [ChainMap(*new_genres)]
                                            }
                                        }
                                    },
                                ],
                            },
                        )
                        .skip(page * limit)
                        .limit(limit)
                        .sort([("views", pymongo.DESCENDING)])
                    )

                    return {
                        "page": page + 1,
                        "results": tv_similar,
                        "page_size": limit,
                    }
                else:
                    raise DefaultError("Movie is not exist")
            else:
                raise NotInTypeError("similar", type)
        except PyMongoError as e:
            InternalServerErrorMessage(e._message)
        except NotInTypeError as e:
            BadRequestMessage(e.message)
        except DefaultError as e:
            BadRequestMessage(e.message)
        except Exception as e:
            InternalServerErrorMessage(e)
