import pymongo
from pymongo.errors import PyMongoError
from utils.JsonResponse import ConvertJsonResponse as cvtJson
from utils.ErrorMessage import BadRequestMessage, InternalServerErrorMessage
from utils.exceptions import NotInTypeError
from flask import *
from configs.database import Database


class MovieSlug(Database):
    def __init__(self):
        self.__db = self.ConnectMongoDB()

    def movie_slug(self, slug):
        try:
            if slug == "all":
                page = request.args.get("page", default=1, type=int) - 1

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
                    "page_size": 20,
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
                    "page_size": 20,
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
                    "page_size": 20,
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
                    "page_size": 20,
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
                    "page_size": 20,
                }
            else:
                raise NotInTypeError("movie slug", slug)
        except PyMongoError as e:
            InternalServerErrorMessage(e._message)
        except NotInTypeError as e:
            BadRequestMessage(e.message)
        except Exception as e:
            InternalServerErrorMessage(e)
