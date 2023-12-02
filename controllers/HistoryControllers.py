import pymongo
from pymongo.errors import PyMongoError
from utils.JsonResponse import ConvertJsonResponse as cvtJson
from utils.ErrorMessage import BadRequestMessage, InternalServerErrorMessage
from utils.exceptions import DefaultError
from flask import *
from pymongo import ReturnDocument
from datetime import datetime
from configs.database import Database
import os
import jwt
import uuid


class History(Database):
    def __init__(self):
        self.__db = self.ConnectMongoDB()

    def gethistory(self, type):
        try:
            user_token = request.headers["Authorization"].replace(
                "Bearer ", ""
            ) or request.cookies.get("user_token")

            jwtUser = jwt.decode(
                user_token,
                str(os.getenv("JWT_SIGNATURE_SECRET")),
                algorithms=["HS256"],
            )

            skip = request.args.get("skip", default=1, type=int) - 1
            limit = request.args.get("limit", default=20, type=int)

            if type == "all":
                history = (
                    self.__db["histories"]
                    .find(
                        {
                            "user_id": jwtUser["id"],
                        },
                    )
                    .skip(skip * limit)
                    .limit(limit)
                    .sort(
                        [("created_at", pymongo.DESCENDING)],
                    )
                )

                total = self.__db["histories"].count_documents(
                    {
                        "user_id": jwtUser["id"],
                    },
                )

                return {
                    "results": cvtJson(history) if history != None else [],
                    "total": total,
                }

            elif type == "movie":
                history = (
                    self.__db["histories"]
                    .find(
                        {
                            "user_id": jwtUser["id"],
                            "media_type": type,
                        },
                    )
                    .skip(skip * limit)
                    .limit(limit)
                    .sort(
                        [("created_at", pymongo.DESCENDING)],
                    )
                )

                total = self.__db["histories"].count_documents(
                    {
                        "user_id": jwtUser["id"],
                        "media_type": type,
                    },
                )

                return {
                    "results": cvtJson(history) if history != None else [],
                    "total": total,
                }

            elif type == "tv":
                history = (
                    self.__db["histories"]
                    .find(
                        {
                            "user_id": jwtUser["id"],
                            "media_type": type,
                        },
                    )
                    .skip(skip * limit)
                    .limit(limit)
                    .sort(
                        [("created_at", pymongo.DESCENDING)],
                    )
                )

                total = self.__db["histories"].count_documents(
                    {
                        "user_id": jwtUser["id"],
                        "media_type": type,
                    },
                )

                return {
                    "results": cvtJson(history) if history != None else [],
                    "total": total,
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
        except PyMongoError as e:
            InternalServerErrorMessage(e._message)
        except Exception as e:
            InternalServerErrorMessage(e)

    def search_history(self, type):
        try:
            user_token = request.headers["Authorization"].replace(
                "Bearer ", ""
            ) or request.cookies.get("user_token")

            jwtUser = jwt.decode(
                user_token,
                str(os.getenv("JWT_SIGNATURE_SECRET")),
                algorithms=["HS256"],
            )
            # skip = request.args.get("skip", default=0, type=int)
            query = request.args.get("query", default="", type=str)

            if type == "all":
                history = (
                    self.__db["histories"]
                    .find(
                        {
                            "user_id": jwtUser["id"],
                            "$or": [
                                {"name": {"$regex": query, "$options": "i"}},
                                {"original_name": {"$regex": query, "$options": "i"}},
                            ],
                        }
                    )
                    .sort(
                        [("created_at", pymongo.DESCENDING)],
                    )
                )

                return {
                    "results": cvtJson(history) if history != None else [],
                    "total": len(cvtJson(history)) if history != None else 0,
                }

            elif type == "movie":
                history = self.__db["histories"].find(
                    {
                        "user_id": jwtUser["id"],
                        "media_type": type,
                        "$or": [
                            {"name": {"$regex": query, "$options": "i"}},
                            {"original_name": {"$regex": query, "$options": "i"}},
                        ],
                    },
                )

                return {
                    "results": cvtJson(history) if history != None else [],
                    "total": len(cvtJson(history)) if history != None else 0,
                }

            elif type == "tv":
                history = self.__db["histories"].find(
                    {
                        "user_id": jwtUser["id"],
                        "media_type": type,
                        "$or": [
                            {"name": {"$regex": query, "$options": "i"}},
                            {"original_name": {"$regex": query, "$options": "i"}},
                        ],
                    },
                )

                return {
                    "results": cvtJson(history) if history != None else [],
                    "total": len(cvtJson(history)) if history != None else 0,
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
        except PyMongoError as e:
            InternalServerErrorMessage(e._message)
        except Exception as e:
            InternalServerErrorMessage(e)

    def getitem_history(self, type, movieId):
        try:
            user_token = request.headers["Authorization"].replace(
                "Bearer ", ""
            ) or request.cookies.get("user_token")

            jwtUser = jwt.decode(
                user_token,
                str(os.getenv("JWT_SIGNATURE_SECRET")),
                algorithms=["HS256"],
            )

            item_history = self.__db["histories"].find_one(
                {
                    "user_id": jwtUser["id"],
                    "movie_id": movieId,
                    "media_type": type,
                },
            )

            if item_history != None:
                return {
                    "success": True,
                    "result": {
                        "duration": item_history["duration"],
                        "percent": item_history["percent"],
                        "seconds": item_history["seconds"],
                    },
                }
            else:
                return {
                    "success": False,
                    "result": "This movie is not found in your history",
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
        except PyMongoError as e:
            InternalServerErrorMessage(e._message)
        except Exception as e:
            InternalServerErrorMessage(e)

    def additem_history(self):
        try:
            user_token = request.headers["Authorization"].replace(
                "Bearer ", ""
            ) or request.cookies.get("user_token")

            jwtUser = jwt.decode(
                user_token,
                str(os.getenv("JWT_SIGNATURE_SECRET")),
                algorithms=["HS256"],
            )

            movie_id = request.form["movie_id"]
            media_type = request.form["media_type"]
            duration = request.form["duration"]
            percent = request.form["percent"]
            seconds = request.form["seconds"]
            idItemHistory = str(uuid.uuid4())

            if media_type == "movie":
                movie = self.__db["movies"].find_one(
                    {"id": movie_id},
                )

                if movie != None:
                    item_history = self.__db["histories"].find_one(
                        {
                            "user_id": jwtUser["id"],
                            "movie_id": movie_id,
                            "media_type": media_type,
                        },
                    )

                    if item_history == None:
                        self.__db["histories"].insert_one(
                            {
                                "id": str(idItemHistory),
                                "user_id": jwtUser["id"],
                                "movie_id": movie_id,
                                "name": movie["name"],
                                "original_name": movie["original_name"],
                                "original_language": movie["original_language"],
                                "media_type": media_type,
                                "genres": movie["genres"],
                                "backdrop_path": movie["backdrop_path"],
                                "poster_path": movie["poster_path"],
                                "dominant_backdrop_color": movie[
                                    "dominant_backdrop_color"
                                ],
                                "dominant_poster_color": movie["dominant_poster_color"],
                                "duration": float(duration),
                                "percent": float(percent),
                                "seconds": float(seconds),
                                "created_at": str(datetime.now()),
                                "updated_at": str(datetime.now()),
                            }
                        )

                        return {
                            "success": True,
                            "results": "Add item to history suucessfully",
                        }
                    else:
                        old_duration = item_history["duration"]
                        old_seconds = item_history["seconds"]
                        old_percent = item_history["percent"]

                        if (
                            float(seconds) > old_seconds
                            and float(percent) > old_percent
                        ):
                            self.__db["histories"].update_one(
                                {
                                    "user_id": jwtUser["id"],
                                    "movie_id": movie_id,
                                    "media_type": media_type,
                                },
                                {
                                    "$set": {
                                        "percent": float(percent),
                                        "seconds": float(seconds),
                                        "updated_at": str(datetime.now()),
                                    }
                                },
                            )

                        else:
                            self.__db["histories"].update_one(
                                {
                                    "user_id": jwtUser["id"],
                                    "movie_id": movie_id,
                                    "media_type": media_type,
                                },
                                {
                                    "$set": {
                                        "percent": float(percent),
                                        "seconds": float(seconds),
                                        "updated_at": str(datetime.now()),
                                    }
                                },
                            )

                    return {
                        "success": True,
                        "results": "Update item from history suucessfully",
                    }
                else:
                    raise DefaultError("Failed to add item to history")

            elif media_type == "tv":
                tv = self.__db["tvs"].find_one(
                    {"id": movie_id},
                )

                if tv != None:
                    item_history = self.__db["histories"].find_one(
                        {
                            "user_id": jwtUser["id"],
                            "movie_id": movie_id,
                            "media_type": media_type,
                        },
                    )

                    if item_history == None:
                        self.__db["histories"].insert_one(
                            {
                                "id": str(idItemHistory),
                                "user_id": jwtUser["id"],
                                "movie_id": movie_id,
                                "name": tv["name"],
                                "original_name": tv["original_name"],
                                "original_language": tv["original_language"],
                                "media_type": media_type,
                                "genres": tv["genres"],
                                "backdrop_path": tv["backdrop_path"],
                                "poster_path": tv["poster_path"],
                                "dominant_backdrop_color": tv[
                                    "dominant_backdrop_color"
                                ],
                                "dominant_poster_color": tv["dominant_poster_color"],
                                "duration": float(duration),
                                "percent": float(percent),
                                "seconds": float(seconds),
                                "created_at": str(datetime.now()),
                                "updated_at": str(datetime.now()),
                            }
                        )

                        return {
                            "success": True,
                            "results": "Add item to history suucessfully",
                        }
                    else:
                        old_duration = item_history["duration"]
                        old_seconds = item_history["seconds"]
                        old_percent = item_history["percent"]

                        if (
                            float(seconds) > old_seconds
                            and float(percent) > old_percent
                        ):
                            self.__db["histories"].update_one(
                                {
                                    "user_id": jwtUser["id"],
                                    "movie_id": movie_id,
                                    "media_type": media_type,
                                },
                                {
                                    "$set": {
                                        "percent": float(percent),
                                        "seconds": float(seconds),
                                        "updated_at": str(datetime.now()),
                                    }
                                },
                            )

                        else:
                            self.__db["histories"].update_one(
                                {
                                    "user_id": jwtUser["id"],
                                    "movie_id": movie_id,
                                    "media_type": media_type,
                                },
                                {
                                    "$set": {
                                        "percent": float(percent),
                                        "seconds": float(seconds),
                                        "updated_at": str(datetime.now()),
                                    }
                                },
                            )

                        return {
                            "success": True,
                            "results": "Update item from history suucessfully",
                        }
                else:
                    raise DefaultError("Failed to add item to history")

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

    def remove_item_history(self):
        try:
            user_token = request.headers["Authorization"].replace(
                "Bearer ", ""
            ) or request.cookies.get("user_token")

            jwtUser = jwt.decode(
                user_token,
                str(os.getenv("JWT_SIGNATURE_SECRET")),
                algorithms=["HS256"],
            )

            id = request.form["id"]
            movie_id = request.form["movie_id"]
            media_type = request.form["media_type"]

            resultDelete1 = self.__db["histories"].delete_one(
                {
                    "user_id": jwtUser["id"],
                    "movie_id": movie_id,
                    "media_type": media_type,
                },
            )

            if resultDelete1.deleted_count == 1:
                return {
                    "success": True,
                    "results": "Remove item from history suucessfully",
                }
            else:
                raise DefaultError("Delete movie from history failed")

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

    def removeall_item_history(self):
        try:
            user_token = request.headers["Authorization"].replace(
                "Bearer ", ""
            ) or request.cookies.get("user_token")

            jwtUser = jwt.decode(
                user_token,
                str(os.getenv("JWT_SIGNATURE_SECRET")),
                algorithms=["HS256"],
            )

            resultDelete = self.__db["histories"].delete_many(
                {"user_id": jwtUser["id"]},
            )

            if resultDelete.deleted_count >= 1:
                history = (
                    self.__db["histories"]
                    .find({"user_id": jwtUser["id"]})
                    .skip(0)
                    .limit(1)
                )

                return {"success": True, "results": cvtJson(history)}

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
