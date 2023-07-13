import pymongo
from pymongo.errors import PyMongoError
from utils.JsonResponse import ConvertJsonResponse as cvtJson
from utils.ErrorMessage import BadRequestMessage, InternalServerErrorMessage
from flask import *
from pymongo import ReturnDocument
from datetime import datetime
from configs.database import Database
import os
import jwt

#   createdAt: { type: Date, default: Date.now },
#   updatedAt: { type: Date, default: Date.now },


class History(Database):
    def __init__(self):
        self.__db = self.ConnectMongoDB()

    def gethistory(self):
        try:
            user_token = request.headers["Authorization"].replace("Bearer ", "")

            jwtUser = jwt.decode(
                user_token,
                str(os.getenv("JWT_TOKEN_SECRET")),
                algorithms=["HS256"],
            )

            skip = request.args.get("skip", default=1, type=int) - 1
            limit = request.args.get("limit", default=20, type=int)

            if skip == 0:
                history = self.__db["histories"].find_one(
                    {"id": jwtUser["id"]}, {"items": {"$slice": [skip * limit, limit]}}
                )
                total = self.__db["histories"].aggregate(
                    [
                        {"$match": {"id": str(jwtUser["id"])}},
                        {
                            "$project": {
                                "total": {"$size": "$items"},
                                #   "result": "$items"
                            }
                        },
                    ]
                )
                # total = self.__db["histories"].find_one({"id": jwtUser["id"]})

                return {
                    "result": cvtJson(history),
                    "total": cvtJson(total)[0]["total"],
                }

            elif skip > 0:
                history = self.__db["histories"].find_one(
                    {"id": jwtUser["id"]}, {"items": {"$slice": [skip * limit, limit]}}
                )
                return {
                    "result": cvtJson(history["items"]),
                    "total": len(history["items"]),
                }
        except jwt.ExpiredSignatureError as e:
            InternalServerErrorMessage("Token is expired")
        except jwt.exceptions.DecodeError as e:
            InternalServerErrorMessage("Token is invalid")
        except PyMongoError as e:
            InternalServerErrorMessage(e._message)
        except Exception as e:
            InternalServerErrorMessage(e)

    def getitem_history(self, type, movieId):
        try:
            user_token = request.headers["Authorization"].replace("Bearer ", "")

            jwtUser = jwt.decode(
                user_token,
                str(os.getenv("JWT_TOKEN_SECRET")),
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
                return {"success": True, "result": cvtJson(item_history)}
            else:
                return {"success": False, "result": "Fail to get item in history"}

        except jwt.ExpiredSignatureError as e:
            InternalServerErrorMessage("Token is expired")
        except jwt.exceptions.DecodeError as e:
            InternalServerErrorMessage("Token is invalid")
        except PyMongoError as e:
            InternalServerErrorMessage(e._message)
        except Exception as e:
            InternalServerErrorMessage(e)

    def search_history(self):
        try:
            user_token = request.headers["Authorization"].replace("Bearer ", "")

            jwtUser = jwt.decode(
                user_token,
                str(os.getenv("JWT_TOKEN_SECRET")),
                algorithms=["HS256"],
            )
            # skip = request.args.get("skip", default=0, type=int)
            query = request.args.get("query", default="", type=str)
            if len(query) != 0:
                history = self.__db["histories"].find_one(
                    {"id": jwtUser["id"]},
                    {
                        "items": {
                            "$elemMatch": {
                                "$or": [
                                    {"name": {"$regex": query, "$options": "i"}},
                                    {
                                        "original_name": {
                                            "$regex": query,
                                            "$options": "i",
                                        }
                                    },
                                ],
                            },
                        }
                    },
                )
                if "items" in history:
                    return {
                        "results": cvtJson(history["items"]),
                        "total": len(history["items"]),
                    }
                else:
                    return {"results": [], "total": 0}

            else:
                history = self.__db["histories"].find_one({"id": jwtUser["id"]})
                total = self.__db["histories"].aggregate(
                    [
                        {"$match": {"id": str(jwtUser["id"])}},
                        {
                            "$project": {
                                "total": {"$size": "$items"},
                            }
                        },
                    ]
                )
                return {
                    "results": cvtJson(history["items"]),
                    "total": cvtJson(total)[0]["total"],
                }
        except jwt.ExpiredSignatureError as e:
            InternalServerErrorMessage("Token is expired")
        except jwt.exceptions.DecodeError as e:
            InternalServerErrorMessage("Token is invalid")
        except PyMongoError as e:
            InternalServerErrorMessage(e._message)
        except Exception as e:
            InternalServerErrorMessage(e)

    def additem_history(self):
        try:
            user_token = request.headers["Authorization"].replace("Bearer ", "")

            jwtUser = jwt.decode(
                user_token,
                str(os.getenv("JWT_TOKEN_SECRET")),
                algorithms=["HS256"],
            )
            media_type = request.form["media_type"]
            media_id = request.form["media_id"]
            duration = request.form["duration"]
            percent = request.form["percent"]
            seconds = request.form["seconds"]

            if media_type == "movie":
                movie = self.__db["movies"].find_one(
                    {"id": str(media_id)},
                    {
                        "images": 0,
                        "credits": 0,
                        "videos": 0,
                        "production_companies": 0,
                    },
                )

                if movie != None:
                    item_history = self.__db["histories"].find_one(
                        {"id": jwtUser["id"]},
                        {"items": {"$elemMatch": {"id": str(media_id)}}},
                    )

                    if "items" not in item_history:
                        self.__db["histories"].find_one_and_update(
                            {"id": jwtUser["id"]},
                            {
                                # "$addToSet": {
                                "$push": {
                                    "items": {
                                        "$each": [
                                            {
                                                "id": str(media_id),
                                                "name": movie["name"],
                                                "original_name": movie["original_name"],
                                                "original_language": movie[
                                                    "original_language"
                                                ],
                                                "media_type": media_type,
                                                "genres": movie["genres"],
                                                "backdrop_path": movie["backdrop_path"],
                                                "poster_path": movie["poster_path"],
                                                "dominant_backdrop_color": movie[
                                                    "dominant_backdrop_color"
                                                ],
                                                "dominant_poster_color": movie[
                                                    "dominant_poster_color"
                                                ],
                                                "duration": float(duration),
                                                "percent": float(percent),
                                                "seconds": float(seconds),
                                                "created_at": str(datetime.now()),
                                                "updated_at": str(datetime.now()),
                                            }
                                        ],
                                        "$position": 0,
                                    }
                                }
                            },
                            {"new": True},
                            upsert=True,
                            return_document=ReturnDocument.AFTER,
                        )
                        return {
                            "success": True,
                            "results": "Add item to history suucessfully",
                        }
                    else:
                        # self.__db["histories"].update_one(
                        #     {"items": {"$elemMatch": {"id": str(media_id)}}},
                        #     {
                        #         "$set": {
                        #             "items.$[element].percent": float(percent),
                        #             "items.$[element].seconds": float(seconds),
                        #         }
                        #     },
                        #     upsert=False,
                        #     array_filters=[
                        #         {"element.id": str(media_id)},
                        #     ],
                        # )

                        old_duration = item_history["items"][0]["duration"]
                        old_seconds = item_history["items"][0]["seconds"]
                        old_percent = item_history["items"][0]["percent"]

                        if (
                            float(seconds) > old_seconds
                            and float(percent) > old_percent
                        ):
                            self.__db["histories"].find_one_and_update(
                                {"id": jwtUser["id"]},
                                {"$pull": {"items": {"id": str(media_id)}}},
                                {"new": True},
                                upsert=True,
                            )

                            self.__db["histories"].find_one_and_update(
                                {"id": jwtUser["id"]},
                                {
                                    # "$addToSet": {
                                    "$push": {
                                        "items": {
                                            "$each": [
                                                {
                                                    "id": str(media_id),
                                                    "name": movie["name"],
                                                    "original_name": movie[
                                                        "original_name"
                                                    ],
                                                    "original_language": movie[
                                                        "original_language"
                                                    ],
                                                    "media_type": media_type,
                                                    "genres": movie["genres"],
                                                    "backdrop_path": movie[
                                                        "backdrop_path"
                                                    ],
                                                    "poster_path": movie["poster_path"],
                                                    "dominant_backdrop_color": movie[
                                                        "dominant_backdrop_color"
                                                    ],
                                                    "dominant_poster_color": movie[
                                                        "dominant_poster_color"
                                                    ],
                                                    "duration": float(duration),
                                                    "percent": float(percent),
                                                    "seconds": float(seconds),
                                                    "created_at": str(datetime.now()),
                                                    "updated_at": str(datetime.now()),
                                                }
                                            ],
                                            "$position": 0,
                                        }
                                    }
                                },
                                {"new": True},
                                upsert=True,
                                return_document=ReturnDocument.AFTER,
                            )
                        else:
                            self.__db["histories"].find_one_and_update(
                                {"id": jwtUser["id"]},
                                {"$pull": {"items": {"id": str(media_id)}}},
                                {"new": True},
                                upsert=True,
                            )

                            self.__db["histories"].find_one_and_update(
                                {"id": jwtUser["id"]},
                                {
                                    # "$addToSet": {
                                    "$push": {
                                        "items": {
                                            "$each": [
                                                {
                                                    "id": str(media_id),
                                                    "name": movie["name"],
                                                    "original_name": movie[
                                                        "original_name"
                                                    ],
                                                    "original_language": movie[
                                                        "original_language"
                                                    ],
                                                    "media_type": media_type,
                                                    "genres": movie["genres"],
                                                    "backdrop_path": movie[
                                                        "backdrop_path"
                                                    ],
                                                    "poster_path": movie["poster_path"],
                                                    "dominant_backdrop_color": movie[
                                                        "dominant_backdrop_color"
                                                    ],
                                                    "dominant_poster_color": movie[
                                                        "dominant_poster_color"
                                                    ],
                                                    "duration": float(old_duration),
                                                    "percent": float(old_percent),
                                                    "seconds": float(old_seconds),
                                                    "created_at": str(datetime.now()),
                                                    "updated_at": str(datetime.now()),
                                                }
                                            ],
                                            "$position": 0,
                                        }
                                    }
                                },
                                {"new": True},
                                upsert=True,
                                return_document=ReturnDocument.AFTER,
                            )

                        return {
                            "success": True,
                            "results": "Update item from history suucessfully",
                        }
                else:
                    return {
                        "success": False,
                        "results": "Failed to add item to history",
                    }

            elif media_type == "tv":
                tv = self.__db["tvs"].find_one(
                    {"id": str(media_id)},
                    {
                        "images": 0,
                        "credits": 0,
                        "videos": 0,
                        "production_companies": 0,
                        "seasons": 0,
                    },
                )

                if tv != None:
                    item_history = self.__db["histories"].find_one(
                        {"id": jwtUser["id"]},
                        {"items": {"$elemMatch": {"id": str(media_id)}}},
                    )

                    if "items" not in item_history:
                        self.__db["histories"].find_one_and_update(
                            {"id": jwtUser["id"]},
                            {
                                # "$addToSet": {
                                "$push": {
                                    "items": {
                                        "$each": [
                                            {
                                                "id": str(media_id),
                                                "name": tv["name"],
                                                "original_name": tv["original_name"],
                                                "original_language": tv[
                                                    "original_language"
                                                ],
                                                "media_type": media_type,
                                                "genres": tv["genres"],
                                                "backdrop_path": tv["backdrop_path"],
                                                "poster_path": tv["poster_path"],
                                                "dominant_backdrop_color": tv[
                                                    "dominant_backdrop_color"
                                                ],
                                                "dominant_poster_color": tv[
                                                    "dominant_poster_color"
                                                ],
                                                "duration": float(duration),
                                                "percent": float(percent),
                                                "seconds": float(seconds),
                                                "created_at": str(datetime.now()),
                                                "updated_at": str(datetime.now()),
                                            }
                                        ],
                                        "$position": 0,
                                    }
                                }
                            },
                            {"new": True},
                            upsert=True,
                            return_document=ReturnDocument.AFTER,
                        )
                        return {
                            "success": True,
                            "results": "Add item to history suucessfully",
                        }
                    else:
                        # self.__db["histories"].update_one(
                        #     {"items": {"$elemMatch": {"id": str(media_id)}}},
                        #     {
                        #         "$set": {
                        #             "items.$[element].percent": float(percent),
                        #             "items.$[element].seconds": float(seconds),
                        #         }
                        #     },
                        #     upsert=False,
                        #     array_filters=[
                        #         {"element.id": str(media_id)},
                        #     ],
                        # )

                        old_duration = item_history["items"][0]["duration"]
                        old_seconds = item_history["items"][0]["seconds"]
                        old_percent = item_history["items"][0]["percent"]

                        if (
                            float(seconds) > old_seconds
                            and float(percent) > old_percent
                        ):
                            self.__db["histories"].find_one_and_update(
                                {"id": jwtUser["id"]},
                                {"$pull": {"items": {"id": str(media_id)}}},
                                {"new": True},
                                upsert=True,
                            )

                            self.__db["histories"].find_one_and_update(
                                {"id": jwtUser["id"]},
                                {
                                    # "$addToSet": {
                                    "$push": {
                                        "items": {
                                            "$each": [
                                                {
                                                    "id": str(media_id),
                                                    "name": tv["name"],
                                                    "original_name": tv[
                                                        "original_name"
                                                    ],
                                                    "original_language": tv[
                                                        "original_language"
                                                    ],
                                                    "media_type": media_type,
                                                    "genres": tv["genres"],
                                                    "backdrop_path": tv[
                                                        "backdrop_path"
                                                    ],
                                                    "poster_path": tv["poster_path"],
                                                    "dominant_backdrop_color": tv[
                                                        "dominant_backdrop_color"
                                                    ],
                                                    "dominant_poster_color": tv[
                                                        "dominant_poster_color"
                                                    ],
                                                    "duration": float(duration),
                                                    "percent": float(percent),
                                                    "seconds": float(seconds),
                                                    "created_at": str(datetime.now()),
                                                    "updated_at": str(datetime.now()),
                                                }
                                            ],
                                            "$position": 0,
                                        }
                                    }
                                },
                                {"new": True},
                                upsert=True,
                                return_document=ReturnDocument.AFTER,
                            )
                        else:
                            self.__db["histories"].find_one_and_update(
                                {"id": jwtUser["id"]},
                                {"$pull": {"items": {"id": str(media_id)}}},
                                {"new": True},
                                upsert=True,
                            )

                            self.__db["histories"].find_one_and_update(
                                {"id": jwtUser["id"]},
                                {
                                    # "$addToSet": {
                                    "$push": {
                                        "items": {
                                            "$each": [
                                                {
                                                    "id": str(media_id),
                                                    "name": tv["name"],
                                                    "original_name": tv[
                                                        "original_name"
                                                    ],
                                                    "original_language": tv[
                                                        "original_language"
                                                    ],
                                                    "media_type": media_type,
                                                    "genres": tv["genres"],
                                                    "backdrop_path": tv[
                                                        "backdrop_path"
                                                    ],
                                                    "poster_path": tv["poster_path"],
                                                    "dominant_backdrop_color": tv[
                                                        "dominant_backdrop_color"
                                                    ],
                                                    "dominant_poster_color": tv[
                                                        "dominant_poster_color"
                                                    ],
                                                    "duration": float(old_duration),
                                                    "percent": float(old_percent),
                                                    "seconds": float(old_seconds),
                                                    "created_at": str(datetime.now()),
                                                    "updated_at": str(datetime.now()),
                                                }
                                            ],
                                            "$position": 0,
                                        }
                                    }
                                },
                                {"new": True},
                                upsert=True,
                                return_document=ReturnDocument.AFTER,
                            )
                        return {
                            "success": True,
                            "results": "Update item from history suucessfully",
                        }

                else:
                    return {
                        "success": False,
                        "results": "Failed to add or update item to history",
                    }

        except jwt.ExpiredSignatureError as e:
            InternalServerErrorMessage("Token is expired")
        except jwt.exceptions.DecodeError as e:
            InternalServerErrorMessage("Token is invalid")
        except PyMongoError as e:
            InternalServerErrorMessage(e._message)
        except Exception as e:
            InternalServerErrorMessage(e)

    def remove_item_history(self):
        try:
            user_token = request.headers["Authorization"].replace("Bearer ", "")

            jwtUser = jwt.decode(
                user_token,
                str(os.getenv("JWT_TOKEN_SECRET")),
                algorithms=["HS256"],
            )

            media_id = request.form["media_id"]

            self.__db["histories"].find_one_and_update(
                {"id": jwtUser["id"]},
                {"$pull": {"items": {"id": str(media_id)}}},
                {"new": True},
                upsert=True,
            )

            list = cvtJson(self.__db["histories"].find_one({"id": jwtUser["id"]}))

            return {"success": True, "results": list["items"]}

        except jwt.ExpiredSignatureError as e:
            InternalServerErrorMessage("Token is expired")
        except jwt.exceptions.DecodeError as e:
            InternalServerErrorMessage("Token is invalid")
        except PyMongoError as e:
            InternalServerErrorMessage(e._message)
        except Exception as e:
            InternalServerErrorMessage(e)

    def removeall_item_history(self):
        try:
            user_token = request.headers["Authorization"].replace("Bearer ", "")

            jwtUser = jwt.decode(
                user_token,
                str(os.getenv("JWT_TOKEN_SECRET")),
                algorithms=["HS256"],
            )
            self.__db["histories"].find_one_and_update(
                {"id": jwtUser["id"]},
                {"$set": {"items": []}},
                {"new": True},
                upsert=True,
                return_document=ReturnDocument.AFTER,
            )

            list = cvtJson(self.__db["histories"].find_one({"id": jwtUser["id"]}))

            return {"success": True, "results": list["items"]}

        except jwt.ExpiredSignatureError as e:
            InternalServerErrorMessage("Token is expired")
        except jwt.exceptions.DecodeError as e:
            InternalServerErrorMessage("Token is invalid")
        except PyMongoError as e:
            InternalServerErrorMessage(e._message)
        except Exception as e:
            InternalServerErrorMessage(e)
