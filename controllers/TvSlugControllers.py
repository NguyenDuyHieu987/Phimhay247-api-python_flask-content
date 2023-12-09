import pymongo
from pymongo.errors import PyMongoError
from utils.JsonResponse import ConvertJsonResponse as cvtJson
from utils.ErrorMessage import BadRequestMessage, InternalServerErrorMessage
from utils.exceptions import NotInTypeError
from flask import *
from configs.database import Database


class TVSlug(Database):
    def __init__(self):
        self.__db = self.ConnectMongoDB()

    def tv_slug(self, slug):
        try:
            page = (request.args.get("page", default=1, type=int)) - 1
            limit = request.args.get("limit", default=20, type=int)

            if slug == "all":
                phimbo = cvtJson(
                    self.__db["tvs"].find({}).skip(page * limit).limit(limit)
                )

                return {
                    "page": page + 1,
                    "results": phimbo,
                    "total": self.__db["tvs"].count_documents({}),
                    "page_size": limit,
                }
            elif slug == "airingtoday":
                page = request.args.get("page", default=1, type=int) - 1
                nowplaying = cvtJson(
                    self.__db["tvairingtodays"].find({}).skip(page * limit).limit(limit)
                )
                return {
                    "page": page + 1,
                    "results": nowplaying,
                    "total": self.__db["tvairingtodays"].count_documents({}),
                    "page_size": limit,
                }
            elif slug == "ontheair":
                page = request.args.get("page", default=1, type=int) - 1
                upcoming = cvtJson(
                    self.__db["tvontheairs"].find({}).skip(page * limit).limit(limit)
                )

                return {
                    "page": page + 1,
                    "results": upcoming,
                    "total": self.__db["tvontheairs"].count_documents({}),
                    "page_size": limit,
                }
            elif slug == "popular":
                page = request.args.get("page", default=1, type=int) - 1
                popular = cvtJson(
                    self.__db["tvpopulars"].find({}).skip(page * limit).limit(limit)
                )

                return {
                    "page": page + 1,
                    "results": popular,
                    "total": self.__db["tvpopulars"].count_documents({}),
                    "page_size": limit,
                }
            elif slug == "toprated":
                page = request.args.get("page", default=1, type=int) - 1
                toprated = cvtJson(
                    self.__db["tvtoprateds"].find({}).skip(page * limit).limit(limit)
                )
                return {
                    "page": page + 1,
                    "results": toprated,
                    "total": self.__db["tvtoprateds"].count_documents({}),
                    "page_size": limit,
                }
            else:
                raise NotInTypeError("tv slug", slug)
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

            def convert_first_air_date(date_gte, data_lte):
                if date_gte != "":
                    return {
                        "first_air_date": {
                            "$gte": date_gte,
                            "$lt": data_lte,
                        }
                    }

                elif date_gte == "" and data_lte != "":
                    return {
                        "first_air_date": {
                            "$lt": data_lte,
                        }
                    }

                return {}

            first_air_date = convert_first_air_date(
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
                        tv = cvtJson(
                            self.__db["tvs"]
                            .find(
                                {
                                    "$and": [
                                        first_air_date,
                                        genres,
                                        original_language,
                                    ]
                                }
                            )
                            .skip(page * limit)
                            .limit(limit)
                            .sort([("views", pymongo.DESCENDING)])
                        )

                        result["results"] = tv

                    elif sort_by == "release_date_desc":
                        tv = cvtJson(
                            self.__db["tvs"]
                            .find(
                                {
                                    "$and": [
                                        first_air_date,
                                        genres,
                                        original_language,
                                    ]
                                }
                            )
                            .skip(page * limit)
                            .limit(limit)
                            .sort([("first_air_date", pymongo.DESCENDING)])
                        )

                        result["results"] = tv

                    elif sort_by == "revenue_desc":
                        tv = cvtJson(
                            self.__db["tvs"]
                            .find(
                                {
                                    "$and": [
                                        first_air_date,
                                        genres,
                                        original_language,
                                    ]
                                }
                            )
                            .skip(page * limit)
                            .limit(limit)
                            .sort([("revenue", pymongo.DESCENDING)])
                        )

                        result["results"] = tv

                    elif sort_by == "vote_average_desc":
                        tv = cvtJson(
                            self.__db["tvs"]
                            .find(
                                {
                                    "$and": [
                                        first_air_date,
                                        genres,
                                        original_language,
                                    ]
                                }
                            )
                            .skip(page * limit)
                            .limit(limit)
                            .sort([("vote_average", pymongo.DESCENDING)])
                        )

                        result["results"] = tv

                    elif sort_by == "vote_count_desc":
                        tv = cvtJson(
                            self.__db["tvs"]
                            .find(
                                {
                                    "$and": [
                                        first_air_date,
                                        genres,
                                        original_language,
                                    ]
                                }
                            )
                            .skip(page * limit)
                            .limit(limit)
                            .sort([("vote_count", pymongo.DESCENDING)])
                        )

                        result["results"] = tv
                else:
                    tv = cvtJson(
                        self.__db["tvs"]
                        .find(
                            {
                                "$and": [
                                    first_air_date,
                                    genres,
                                    original_language,
                                ]
                            }
                        )
                        .skip(page * limit)
                        .limit(limit)
                    )

                    result["results"] = tv

                result["total"] = self.__db["tvs"].count_documents(
                    {
                        "$and": [
                            first_air_date,
                            genres,
                            original_language,
                        ]
                    }
                )
            elif slug == "airingtoday":
                tv = cvtJson(
                    self.__db["tvairingtodays"]
                    .find(
                        {
                            "$and": [
                                first_air_date,
                                genres,
                                original_language,
                            ]
                        }
                    )
                    .skip(page * limit)
                    .limit(limit)
                )

                result["results"] = tv

                result["total"] = self.__db["tvairingtodays"].count_documents(
                    {
                        "$and": [
                            first_air_date,
                            genres,
                            original_language,
                        ]
                    }
                )
            elif slug == "ontheair":
                tv = cvtJson(
                    self.__db["tvontheairs"]
                    .find(
                        {
                            "$and": [
                                first_air_date,
                                genres,
                                original_language,
                            ]
                        }
                    )
                    .skip(page * limit)
                    .limit(limit)
                )

                result["results"] = tv

                result["total"] = self.__db["tvontheairs"].count_documents(
                    {
                        "$and": [
                            first_air_date,
                            genres,
                            original_language,
                        ]
                    }
                )
            elif slug == "popular":
                tv = cvtJson(
                    self.__db["tvpopulars"]
                    .find(
                        {
                            "$and": [
                                first_air_date,
                                genres,
                                original_language,
                            ]
                        }
                    )
                    .skip(page * limit)
                    .limit(limit)
                )

                result["results"] = tv

                result["total"] = self.__db["tvpopulars"].count_documents(
                    {
                        "$and": [
                            first_air_date,
                            genres,
                            original_language,
                        ]
                    }
                )
            elif slug == "toprated":
                tv = cvtJson(
                    self.__db["tvtoprateds"]
                    .find(
                        {
                            "$and": [
                                first_air_date,
                                genres,
                                original_language,
                            ]
                        }
                    )
                    .skip(page * limit)
                    .limit(limit)
                )

                result["results"] = tv

                result["total"] = self.__db["tvtoprateds"].count_documents(
                    {
                        "$and": [
                            first_air_date,
                            genres,
                            original_language,
                        ]
                    }
                )
            else:
                raise NotInTypeError("tv discover", slug)

            return result
        except NotInTypeError as e:
            BadRequestMessage(e.message)
        except PyMongoError as e:
            InternalServerErrorMessage(e._message)
        except Exception as e:
            InternalServerErrorMessage(e)
