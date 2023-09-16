import pymongo
from pymongo.errors import PyMongoError
from collections import ChainMap
from utils.JsonResponse import ConvertJsonResponse as cvtJson
from utils.ErrorMessage import BadRequestMessage, InternalServerErrorMessage
import pyfpgrowth
from flask import *
from configs.database import Database
import os
import jwt


class Recommend(Database):
    def __init__(self):
        self.__db = self.ConnectMongoDB()

    def get_recommend(self):
        try:
            user_token = request.headers["Authorization"].replace(
                "Bearer ", ""
            ) or request.cookies.get("user_token")

            jwtUser = jwt.decode(
                user_token,
                str(os.getenv("JWT_SIGNATURE_SECRET")),
                algorithms=["HS256"],
            )

            page = request.args.get("page", default=1, type=int) - 1
            limit = request.args.get("limit", default=6, type=int)

            list = self.__db["lists"].find({"user_id": jwtUser["id"]}).skip(0).limit(20)

            history = (
                self.__db["histories"]
                .find({"user_id": jwtUser["id"]})
                .skip(0)
                .limit(20)
            )

            genres = []
            countries = []

            for x in list:
                genres.append([x1["id"] for x1 in x["genres"]])
                countries.append([x["original_language"]])

            for x in history:
                genres.append([x1["id"] for x1 in x["genres"]])
                countries.append([x["original_language"]])

            if len(genres) == 0 and len(countries) == 0:
                return {"results": []}
            else:
                minSup_Genres = 5
                minSup_Countries = 5
                patterns_genres = pyfpgrowth.find_frequent_patterns(
                    genres, minSup_Genres
                )

                while len(patterns_genres) == 0:
                    minSup_Genres -= 1
                    patterns_genres = pyfpgrowth.find_frequent_patterns(
                        genres, minSup_Genres
                    )

                patterns_genres_single = [
                    (item[0], item1)
                    for item, item1 in patterns_genres.items()
                    if len(item) == 1
                ]

                patterns_countries = pyfpgrowth.find_frequent_patterns(
                    countries, minSup_Countries
                )

                while len(patterns_countries) == 0:
                    minSup_Countries -= 1
                    patterns_countries = pyfpgrowth.find_frequent_patterns(
                        countries, minSup_Countries
                    )

                patterns_genres_desc = sorted(
                    patterns_genres_single,
                    key=lambda item: item[1],
                    reverse=True,
                )

                patterns_countries_desc = sorted(
                    patterns_countries.items(),
                    key=lambda item: item[1],
                    reverse=True,
                )

                frequency_genres_dict = []

                for pattern in patterns_genres_desc:
                    frequency_genres_dict.append(({"id": pattern[0]}))

                frequency_countries_list = [x for x in patterns_countries_desc[0][0]]

                movie = cvtJson(
                    self.__db["movies"]
                    .find(
                        {
                            "$or": [
                                {
                                    "original_language": {
                                        "$in": frequency_countries_list
                                    }
                                },
                                {
                                    "genres": {
                                        "$elemMatch": {
                                            "$or": [ChainMap(*frequency_genres_dict)]
                                        }
                                    }
                                },
                            ]
                        },
                    )
                    .skip(page * limit)
                    .limit(limit)
                    .sort([("views", pymongo.DESCENDING)])
                )

                tv = cvtJson(
                    self.__db["tvs"]
                    .find(
                        {
                            "$or": [
                                {
                                    "original_language": {
                                        "$in": frequency_countries_list
                                    }
                                },
                                {
                                    "genres": {
                                        "$elemMatch": {
                                            "$or": [ChainMap(*frequency_genres_dict)]
                                        }
                                    }
                                },
                            ]
                        },
                    )
                    .skip(page * limit)
                    .limit(limit)
                    .sort([("views", pymongo.DESCENDING)])
                )

                result = movie + tv

                return {
                    "results": result,
                    "movie": movie,
                    "tv": tv,
                    # "total": ,
                    # "totalMovie": ,
                    # "totalTv": ,
                }

        except jwt.ExpiredSignatureError as e:
            make_response().delete_cookie("user_token")
            InternalServerErrorMessage("Token is expired")
        except (jwt.exceptions.DecodeError, jwt.exceptions.InvalidSignatureError) as e:
            make_response().delete_cookie("user_token")
            InternalServerErrorMessage("Token is invalid")
        except PyMongoError as e:
            InternalServerErrorMessage(e._message)
        except Exception as e:
            InternalServerErrorMessage(e)
