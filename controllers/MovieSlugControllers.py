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
            page = request.args.get("page", default=1, type=int) - 1
            limit = request.args.get("limit", default=20, type=int)

            if slug == "all":
                phimle = cvtJson(
                    self.__db["movies"].find({}).skip(page * limit).limit(limit)
                )

                return {
                    "page": page + 1,
                    "results": phimle,
                    "total": self.__db["movies"].count_documents({}),
                    "page_size": limit,
                }
            elif slug == "nowplaying":
                page = request.args.get("page", default=1, type=int) - 1
                nowplaying = cvtJson(
                    self.__db["nowplayings"].find({}).skip(page * limit).limit(limit)
                )
                return {
                    "page": page + 1,
                    "results": nowplaying,
                    "total": self.__db["nowplayings"].count_documents({}),
                    "page_size": limit,
                }
            elif slug == "upcoming":
                page = request.args.get("page", default=1, type=int) - 1
                upcoming = cvtJson(
                    self.__db["upcomings"].find({}).skip(page * limit).limit(limit)
                )
                return {
                    "page": page + 1,
                    "results": upcoming,
                    "total": self.__db["upcomings"].count_documents({}),
                    "page_size": limit,
                }
            elif slug == "popular":
                page = request.args.get("page", default=1, type=int) - 1
                popular = cvtJson(
                    self.__db["populars"].find({}).skip(page * limit).limit(limit)
                )
                return {
                    "page": page + 1,
                    "results": popular,
                    "total": self.__db["populars"].count_documents({}),
                    "page_size": limit,
                }
            elif slug == "toprated":
                page = request.args.get("page", default=1, type=int) - 1
                toprated = cvtJson(
                    self.__db["toprateds"].find({}).skip(page * limit).limit(limit)
                )
                return {
                    "page": page + 1,
                    "results": toprated,
                    "total": self.__db["toprateds"].count_documents({}),
                    "page_size": limit,
                }
            else:
                raise NotInTypeError("movie slug", slug)
        except PyMongoError as e:
            InternalServerErrorMessage(e._message)
        except NotInTypeError as e:
            BadRequestMessage(e.message)
        except Exception as e:
            InternalServerErrorMessage(e)

    def filter(self, slug):
        try:
            page = request.args.get("page", default=1, type=int) - 1
            limit = request.args.get("limit", default=20, type=int)

            sort_by = request.args.get("sort_by", default="", type=str)

            primary_release_date_gte = request.args.get(
                "primary_release_date_gte", default="", type=str
            )

            primary_release_date_lte = request.args.get(
                "primary_release_date_lte", default="", type=str
            )

            with_genres = request.args.get("with_genres", default="", type=str)

            with_original_language = request.args.get(
                "with_original_language", default="", type=str
            )

            def convert_release_date(date_gte, data_lte):
                if date_gte != "":
                    return {
                        "release_date": {
                            "$gte": date_gte,
                            "$lte": data_lte,
                        }
                    }

                elif date_gte == "" and data_lte != "":
                    return {
                        "release_date": {
                            "$lte": data_lte,
                        }
                    }
                return {}

            release_date = convert_release_date(
                primary_release_date_gte, primary_release_date_lte
            )

            def convert_genres(genre):
                if genre != "":
                    return {
                        "genres": {
                            "$elemMatch": {
                                # "id": int(with_genres.split(",")[0]),
                                # "name": with_genres.split(",")[1],
                                "id": int(with_genres)
                            }
                        }
                    }
                else:
                    return {}

            genres = convert_genres(with_genres)

            def convert_original_language(language):
                if language != "":
                    return {"original_language": {"$regex": with_original_language}}
                else:
                    return {}

            original_language = convert_original_language(with_original_language)

            result = {
                "page": page + 1,
                "results": [],
                "page_size": limit,
                "total": 0,
            }

            if slug == "all":
                if sort_by != "":
                    if sort_by == "views_desc":
                        movie = cvtJson(
                            self.__db["movies"]
                            .find(
                                {
                                    "$and": [
                                        release_date,
                                        genres,
                                        original_language,
                                    ]
                                }
                            )
                            .skip(page * limit)
                            .limit(limit)
                            .sort([("views", pymongo.DESCENDING)])
                        )

                        result["results"] = movie

                    elif sort_by == "release_date_desc":
                        movie = cvtJson(
                            self.__db["movies"]
                            .find(
                                {
                                    "$and": [
                                        release_date,
                                        genres,
                                        original_language,
                                    ]
                                }
                            )
                            .skip(page * limit)
                            .limit(limit)
                            .sort([("release_date", pymongo.DESCENDING)])
                        )

                        result["results"] = movie

                    elif sort_by == "revenue_desc":
                        movie = cvtJson(
                            self.__db["movies"]
                            .find(
                                {
                                    "$and": [
                                        release_date,
                                        genres,
                                        original_language,
                                    ]
                                }
                            )
                            .skip(page * limit)
                            .limit(limit)
                            .sort([("revenue", pymongo.DESCENDING)])
                        )

                        result["results"] = movie

                    elif sort_by == "vote_average_desc":
                        movie = cvtJson(
                            self.__db["movies"]
                            .find(
                                {
                                    "$and": [
                                        release_date,
                                        genres,
                                        original_language,
                                    ]
                                }
                            )
                            .skip(page * limit)
                            .limit(limit)
                            .sort([("vote_average", pymongo.DESCENDING)])
                        )

                        result["results"] = movie

                    elif sort_by == "vote_count_desc":
                        movie = cvtJson(
                            self.__db["movies"]
                            .find(
                                {
                                    "$and": [
                                        release_date,
                                        genres,
                                        original_language,
                                    ]
                                }
                            )
                            .skip(page * limit)
                            .limit(limit)
                            .sort([("vote_count", pymongo.DESCENDING)])
                        )

                        result["results"] = movie
                else:
                    movie = cvtJson(
                        self.__db["movies"]
                        .find(
                            {
                                "$and": [
                                    release_date,
                                    genres,
                                    original_language,
                                ]
                            }
                        )
                        .skip(page * limit)
                        .limit(limit)
                    )

                    result["results"] = movie

                result["total"] = self.__db["movies"].count_documents(
                    {
                        "$and": [
                            release_date,
                            genres,
                            original_language,
                        ]
                    }
                )
            elif slug == "nowplaying":
                movie = cvtJson(
                    self.__db["nowplayings"]
                    .find(
                        {
                            "$and": [
                                release_date,
                                genres,
                                original_language,
                            ]
                        }
                    )
                    .skip(page * limit)
                    .limit(limit)
                )

                result["results"] = movie

                result["total"] = self.__db["nowplayings"].count_documents(
                    {
                        "$and": [
                            release_date,
                            genres,
                            original_language,
                        ]
                    }
                )
            elif slug == "upcoming":
                movie = cvtJson(
                    self.__db["upcomings"]
                    .find(
                        {
                            "$and": [
                                release_date,
                                genres,
                                original_language,
                            ]
                        }
                    )
                    .skip(page * limit)
                    .limit(limit)
                )

                result["results"] = movie

                result["total"] = self.__db["upcomings"].count_documents(
                    {
                        "$and": [
                            release_date,
                            genres,
                            original_language,
                        ]
                    }
                )
            elif slug == "popular":
                movie = cvtJson(
                    self.__db["populars"]
                    .find(
                        {
                            "$and": [
                                release_date,
                                genres,
                                original_language,
                            ]
                        }
                    )
                    .skip(page * limit)
                    .limit(limit)
                )

                result["results"] = movie

                result["total"] = self.__db["populars"].count_documents(
                    {
                        "$and": [
                            release_date,
                            genres,
                            original_language,
                        ]
                    }
                )
            elif slug == "toprated":
                movie = cvtJson(
                    self.__db["toprateds"]
                    .find(
                        {
                            "$and": [
                                release_date,
                                genres,
                                original_language,
                            ]
                        }
                    )
                    .skip(page * limit)
                    .limit(limit)
                )

                result["results"] = movie

                result["total"] = self.__db["toprateds"].count_documents(
                    {
                        "$and": [
                            release_date,
                            genres,
                            original_language,
                        ]
                    }
                )
            else:
                raise NotInTypeError("movie discover", slug)

            return result
        except NotInTypeError as e:
            BadRequestMessage(e.message)
        except PyMongoError as e:
            InternalServerErrorMessage(e._message)
        except Exception as e:
            InternalServerErrorMessage(e)
