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
            limit = request.args.get("limit", default=20, type=int)

            list = cvtJson(
                self.__db["lists"]
                .find({"user_id": jwtUser["id"]})
                .skip(0)
                .limit(20)
                .sort([("created_at", pymongo.DESCENDING)])
            )

            history = cvtJson(
                self.__db["histories"]
                .find({"user_id": jwtUser["id"]})
                .skip(0)
                .limit(20)
                .sort([("created_at", pymongo.DESCENDING)])
            )

            if len(list) == 0 and len(history) == 0:
                return {
                    "results": [],
                }

            genres = []
            countries = []

            for x in list:
                for x1 in x["genres"]:
                    if "id" in x1:
                        if x1["id"] not in [x2["id"] for x2 in genres]:
                            genres.append({"id": x1["id"]})

                if x["original_language"] not in countries:
                    countries.append(x["original_language"])

            for x in history:
                for x1 in x["genres"]:
                    if "id" in x1:
                        if x1["id"] not in [x2["id"] for x2 in genres]:
                            genres.append({"id": x1["id"]})

                if x["original_language"] not in countries:
                    countries.append(x["original_language"])

            movie = cvtJson(
                self.__db["movies"]
                .find(
                    {
                        "$or": [
                            {"original_language": {"$in": countries}},
                            {"genres": {"$elemMatch": {"$or": genres}}},
                        ]
                    },
                )
                .skip(page * int(limit / 2))
                .limit(int(limit / 2))
                .sort([("views", pymongo.DESCENDING)])
            )

            tv = cvtJson(
                self.__db["tvs"]
                .find(
                    {
                        "$or": [
                            {"original_language": {"$in": countries}},
                            {"genres": {"$elemMatch": {"$or": genres}}},
                        ]
                    },
                )
                .skip(page * int(limit / 2))
                .limit(int(limit / 2))
                .sort([("views", pymongo.DESCENDING)])
            )

            result = movie + tv

            response = {
                "page": page + 1,
                "results": result,
                "movie": movie,
                "tv": tv,
                "page_size": limit,
            }

            return response

        except jwt.ExpiredSignatureError as e:
            make_response().delete_cookie(
                "user_token", samesite="lax", secure=True, httponly=False
            )
            InternalServerErrorMessage("Token is expired")
        except (jwt.exceptions.DecodeError, jwt.exceptions.InvalidSignatureError) as e:
            make_response().delete_cookie(
                "user_token", samesite="lax", secure=True, httponly=False
            )
            InternalServerErrorMessage("Token is invalid")
        except PyMongoError as e:
            InternalServerErrorMessage(e._message)
        except Exception as e:
            InternalServerErrorMessage(e)
