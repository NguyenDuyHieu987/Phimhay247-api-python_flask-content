import pymongo
from pymongo.errors import PyMongoError
from utils.JsonResponse import ConvertJsonResponse as cvtJson
from utils.ErrorMessage import errorMessage
from flask import *
from configs.database import Database


class MovieSlug(Database):
    def __init__(self):
        self.__db = self.ConnectMongoDB()

    def movie_slug(self, slug):
        try:
            if slug == "phimle":
                page = (request.args.get("page", default=1, type=int)) - 1

                phimle = cvtJson(
                    self.__db["movies"]
                    .find(
                        {},
                        {
                            "images": 0,
                            "credits": 0,
                            "videos": 0,
                            "production_companies": 0,
                        },
                    )
                    .skip(page * 20)
                    .limit(20)
                )

                return {
                    "page": page + 1,
                    "results": phimle,
                    "total": self.__db["movies"].count_documents({}),
                }
            elif slug == "nowplaying":
                page = request.args.get("page", default=1, type=int) - 1
                nowplaying = cvtJson(
                    self.__db["nowplayings"].find({}).skip(page * 20).limit(20)
                )
                return {
                    "page": page + 1,
                    "results": nowplaying,
                    "total": self.__db["nowplayings"].count_documents({}),
                }
            elif slug == "upcoming":
                page = request.args.get("page", default=1, type=int) - 1
                upcoming = cvtJson(
                    self.__db["upcomings"].find({}).skip(page * 20).limit(20)
                )
                return {
                    "page": page + 1,
                    "results": upcoming,
                    "total": self.__db["upcomings"].count_documents({}),
                }
            elif slug == "popular":
                page = request.args.get("page", default=1, type=int) - 1
                popular = cvtJson(
                    self.__db["populars"].find({}).skip(page * 20).limit(20)
                )
                return {
                    "page": page + 1,
                    "results": popular,
                    "total": self.__db["populars"].count_documents({}),
                }
            elif slug == "toprated":
                page = request.args.get("page", default=1, type=int) - 1
                toprated = cvtJson(
                    self.__db["toprateds"].find({}).skip(page * 20).limit(20)
                )
                return {
                    "page": page + 1,
                    "results": toprated,
                    "total": self.__db["toprateds"].count_documents({}),
                }
            else:
                return errorMessage(400)
        except:
            return {
                "results": [],
                "total": 0,
            }
        # finally:
        #     return errorMessage(400)
