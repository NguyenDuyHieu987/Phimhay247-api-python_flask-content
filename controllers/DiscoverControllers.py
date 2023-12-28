import pymongo
from pymongo.errors import PyMongoError
from utils.JsonResponse import ConvertJsonResponse as cvtJson
from utils.ErrorMessage import BadRequestMessage, InternalServerErrorMessage
from utils.exceptions import NotInTypeError
from flask import *
from configs.database import Database


class Discover(Database):
    def __init__(self):
        self.__db = self.ConnectMongoDB()
        # self.discoverutils = DiscoverUtils(self.ConnectMongoDB())

    def get_slug(self, type):
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

            def convert_first_air_date(date_gte, data_lte):
                if date_gte != "":
                    return {
                        "first_air_date": {
                            "$gte": date_gte,
                            "$lte": data_lte,
                        }
                    }

                elif date_gte == "" and data_lte != "":
                    return {
                        "first_air_date": {
                            "$lte": data_lte,
                        }
                    }

                return {}

            release_date = convert_release_date(
                primary_release_date_gte, primary_release_date_lte
            )

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

            if type == "all":
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
                            .skip(page * int(limit / 2))
                            .limit(int(limit / 2))
                            .sort([("views", pymongo.DESCENDING)])
                        )

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
                            .skip(page * int(limit / 2))
                            .limit(int(limit / 2))
                            .sort([("views", pymongo.DESCENDING)])
                        )

                        result["results"] = movie + tv

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
                            .skip(page * int(limit / 2))
                            .limit(int(limit / 2))
                            .sort([("release_date", pymongo.DESCENDING)])
                        )

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
                            .skip(page * int(limit / 2))
                            .limit(int(limit / 2))
                            .sort([("first_air_date", pymongo.DESCENDING)])
                        )

                        result["results"] = movie + tv

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
                            .skip(page * int(limit / 2))
                            .limit(int(limit / 2))
                            .sort([("revenue", pymongo.DESCENDING)])
                        )

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
                            .skip(page * int(limit / 2))
                            .limit(int(limit / 2))
                            .sort([("revenue", pymongo.DESCENDING)])
                        )

                        result["results"] = movie + tv

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
                            .skip(page * int(limit / 2))
                            .limit(int(limit / 2))
                            .sort([("vote_average", pymongo.DESCENDING)])
                        )

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
                            .skip(page * int(limit / 2))
                            .limit(int(limit / 2))
                            .sort([("vote_average", pymongo.DESCENDING)])
                        )

                        result["results"] = movie + tv

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
                            .skip(page * int(limit / 2))
                            .limit(int(limit / 2))
                            .sort([("vote_count", pymongo.DESCENDING)])
                        )

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
                            .skip(page * int(limit / 2))
                            .limit(int(limit / 2))
                            .sort([("vote_count", pymongo.DESCENDING)])
                        )

                        result["results"] = movie + tv

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
                        .skip(page * int(limit / 2))
                        .limit(int(limit / 2))
                    )

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
                        .skip(page * int(limit / 2))
                        .limit(int(limit / 2))
                    )

                    result["results"] = movie + tv

                result["total"] = self.__db["movies"].count_documents(
                    {
                        "$and": [
                            release_date,
                            genres,
                            original_language,
                        ]
                    }
                ) + self.__db["tvs"].count_documents(
                    {
                        "$and": [
                            first_air_date,
                            genres,
                            original_language,
                        ]
                    }
                )
            elif type == "movie":
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
                            .sort(
                                [("views", pymongo.DESCENDING)],
                            )
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
                            .sort(
                                [("release_date", pymongo.DESCENDING)],
                            )
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
                            .sort(
                                [("revenue", pymongo.DESCENDING)],
                            )
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
                            .sort(
                                [("vote_average", pymongo.DESCENDING)],
                            )
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
                            .sort(
                                [("vote_count", pymongo.DESCENDING)],
                            )
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
            elif type == "tv":
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
            else:
                raise NotInTypeError("discover", type)

            return result

        except NotInTypeError as e:
            BadRequestMessage(e.message)
        except PyMongoError as e:
            InternalServerErrorMessage(e._message)
        except Exception as e:
            InternalServerErrorMessage(e)
