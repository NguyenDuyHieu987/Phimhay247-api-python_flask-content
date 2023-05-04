import pymongo
from collections import ChainMap
from utils.JsonResponse import ConvertJsonResponse as cvtJson
from flask import *
from configs.database import Database


class Similar(Database):
    def __init__(self):
        self.__db = self.ConnectMongoDB()

    def get_similar(self, type, movieid):
        if type == "movie":
            movie_similar = self.__db["movies"].find_one({"id": int(movieid)})
            genres = movie_similar["genres"]
            country = movie_similar["original_language"]

            new_genres = [{"id": int(x["id"])} for x in genres]

            movie = cvtJson(
                self.__db["movies"]
                .find(
                    {
                        "id": {
                            "$nin": [int(movieid)],
                        },
                        "$or": [
                            {"original_language": {"$regex": country}},
                            {
                                "genres": {
                                    "$elemMatch": {"$or": [ChainMap(*new_genres)]}
                                }
                            },
                        ],
                    },
                    {"images": 0, "credits": 0, "videos": 0, "production_companies": 0},
                )
                .skip(0)
                .limit(20)
                .sort([("views", pymongo.DESCENDING)])
            )
            return {
                "results": movie,
            }
        elif type == "tv":
            tv_similar = self.__db["tvs"].find_one({"id": int(movieid)})
            genres = tv_similar["genres"]
            country = tv_similar["original_language"]

            new_genres = [{"id": int(x["id"])} for x in genres]

            tv = cvtJson(
                self.__db["tvs"]
                .find(
                    {
                        "id": {
                            "$nin": [int(movieid)],
                        },
                        "$or": [
                            {"original_language": {"$regex": country}},
                            {
                                "genres": {
                                    "$elemMatch": {"$or": [ChainMap(*new_genres)]}
                                }
                            },
                        ],
                    },
                    {"images": 0, "credits": 0, "videos": 0, "production_companies": 0},
                )
                .skip(0)
                .limit(20)
                .sort([("views", pymongo.DESCENDING)])
            )
            return {
                "results": tv,
            }
