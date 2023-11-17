import pymongo
from pymongo.errors import PyMongoError
from utils.JsonResponse import ConvertJsonResponse as cvtJson
from utils.ErrorMessage import BadRequestMessage, InternalServerErrorMessage
from utils.exceptions import DefaultError
from flask import *
from pymongo import ReturnDocument
from configs.database import Database
import os
import jwt
import uuid
from datetime import datetime


class Rate(Database):
    def __init__(self):
        self.__db = self.ConnectMongoDB()

    def get_rating(self, type, id):
        try:
            user_token = request.headers["Authorization"].replace(
                "Bearer ", ""
            ) or request.cookies.get("user_token")

            jwtUser = jwt.decode(
                user_token,
                str(os.getenv("JWT_SIGNATURE_SECRET")),
                algorithms=["HS256"],
            )

            rate = self.__db["rates"].find_one(
                {
                    "user_id": jwtUser["id"],
                    "movie_id": str(id),
                    "movie_type": type,
                }
            )

            if rate != None:
                return {"success": True, "result": cvtJson(rate)}
            else:
                return {
                    "success": False,
                    "result": "This movie is not rated",
                }

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
        except DefaultError as e:
            BadRequestMessage(e.message)
        except PyMongoError as e:
            InternalServerErrorMessage(e._message)
        except Exception as e:
            InternalServerErrorMessage(e)

    def rating(self, type, id):
        try:
            user_token = request.headers["Authorization"].replace(
                "Bearer ", ""
            ) or request.cookies.get("user_token")

            jwtUser = jwt.decode(
                user_token,
                str(os.getenv("JWT_SIGNATURE_SECRET")),
                algorithms=["HS256"],
            )

            rateValue = float(request.form["value"])
            if type == "movie":
                movie_dumps = self.__db["movies"].find_one({"id": str(id)})

                if movie_dumps != None:
                    new_vote_average = (
                        movie_dumps["vote_count"] * movie_dumps["vote_average"]
                        + rateValue
                    ) / (movie_dumps["vote_count"] + 1)

                    new_movie = self.__db["movies"].find_one_and_update(
                        {"id": str(id)},
                        {
                            "$set": {
                                "vote_average": new_vote_average,
                                "vote_count": movie_dumps["vote_count"] + 1,
                            },
                        },
                        return_document=ReturnDocument.AFTER,
                    )

                    idRate = str(uuid.uuid4())

                    if new_movie != None:
                        resultInsert1 = self.__db["rates"].insert_one(
                            {
                                "id": idRate,
                                "rate_value": rateValue,
                                "user_id": jwtUser["id"],
                                "movie_id": str(id),
                                "movie_type": "movie",
                                "created_at": str(datetime.now()),
                                "updated_at": str(datetime.now()),
                            }
                        )

                        if resultInsert1.acknowledged == False:
                            raise DefaultError("Rate movie failed")
                    else:
                        raise DefaultError("Rate movie failed")

                    return {
                        "success": True,
                        "vote_average": new_movie["vote_average"],
                        "vote_count": new_movie["vote_count"],
                    }
                else:
                    raise DefaultError("Movie is not exists")

            elif type == "tv":
                tv_dumps = self.__db["tvs"].find_one({"id": str(id)})

                if tv_dumps != None:
                    new_vote_average = (
                        tv_dumps["vote_count"] * tv_dumps["vote_average"] + rateValue
                    ) / (tv_dumps["vote_count"] + 1)

                    new_tv = self.__db["tvs"].find_one_and_update(
                        {"id": str(id)},
                        {
                            "$set": {
                                "vote_average": new_vote_average,
                                "vote_count": tv_dumps["vote_count"] + 1,
                            },
                        },
                        return_document=ReturnDocument.AFTER,
                    )

                    idRate = str(uuid.uuid4())

                    if new_tv != None:
                        resultInsert2 = self.__db["rates"].insert_one(
                            {
                                "id": idRate,
                                "rate_value": rateValue,
                                "user_id": jwtUser["id"],
                                "movie_id": str(id),
                                "movie_type": "tv",
                                "created_at": str(datetime.now()),
                                "updated_at": str(datetime.now()),
                            }
                        )
                        if resultInsert2.acknowledged == False:
                            raise DefaultError("Update rate movie failed")
                    else:
                        raise DefaultError("Update rate movie failed")

                    return {
                        "success": True,
                        "vote_average": new_tv["vote_average"],
                        "vote_count": new_tv["vote_count"],
                    }
                else:
                    raise DefaultError("Movie is not exists")

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
        except DefaultError as e:
            BadRequestMessage(e.message)
        except PyMongoError as e:
            InternalServerErrorMessage(e._message)
        except Exception as e:
            InternalServerErrorMessage(e)
