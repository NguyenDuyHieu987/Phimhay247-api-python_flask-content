import pymongo
from pymongo.errors import PyMongoError
from utils.JsonResponse import ConvertJsonResponse as cvtJson
from utils.ErrorMessage import BadRequestMessage
from flask import *
from pymongo import ReturnDocument
from datetime import datetime
from configs.database import Database
import os
import jwt

#   createdAt: { type: Date, default: Date.now },
#   updatedAt: { type: Date, default: Date.now },


class WatchList(Database):
    def __init__(self):
        self.__db = self.ConnectMongoDB()

    def getwatchlist(self):
        try:
            user_token = request.headers["Authorization"].replace("Bearer ", "")

            jwtUser = jwt.decode(
                user_token,
                str(os.getenv("JWT_TOKEN_SECRET")),
                algorithms=["HS256"],
            )

            skip = request.args.get("skip", default=0, type=int)
            if skip == 0:
                watchlist = self.__db["watchlists"].find_one(
                    {"id": jwtUser["id"]}, {"items": {"$slice": [skip * 20, 20]}}
                )
                total = self.__db["watchlists"].aggregate(
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
                # total = self.__db["watchlists"].find_one({"id": jwtUser["id"]})

                return {
                    "result": cvtJson(watchlist),
                    "total": cvtJson(total)[0]["total"],
                }

            elif skip > 0:
                watchlist = self.__db["watchlists"].find_one(
                    {"id": jwtUser["id"]}, {"items": {"$slice": [skip * 20, 20]}}
                )
                return {
                    "result": cvtJson(watchlist["items"]),
                    "total": len(watchlist["items"]),
                }
        except jwt.ExpiredSignatureError as e:
            return {"is_token_expired": True, "result": "Token is expired"}
        except jwt.exceptions.DecodeError as e:
            return {"is_invalid_token": True, "result": "Token is invalid"}
        except:
            return {"success": False, "result": "Failed to get history"}

    def getitem_watchlist(self, idmovie):
        try:
            user_token = request.headers["Authorization"].replace("Bearer ", "")

            jwtUser = jwt.decode(
                user_token,
                str(os.getenv("JWT_TOKEN_SECRET")),
                algorithms=["HS256"],
            )
            item_watchlists = self.__db["watchlists"].find_one(
                {"id": jwtUser["id"]}, {"items": {"$elemMatch": {"id": int(idmovie)}}}
            )
            if "items" in item_watchlists:
                return {"success": True, "result": cvtJson(item_watchlists["items"][0])}
            else:
                return {"success": False, "result": "Fail to get item in watchlist"}

        except jwt.ExpiredSignatureError as e:
            return {"is_token_expired": True, "result": "Token is expired"}
        except jwt.exceptions.DecodeError as e:
            return {"is_invalid_token": True, "result": "Token is invalid"}
        except:
            return {"success": False, "result": "Fail to get item in watchlist"}

    def search_watchlist(self):
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
                watchlist = self.__db["watchlists"].find_one(
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
                if "items" in watchlist:
                    return {
                        "results": cvtJson(watchlist["items"]),
                        "total": len(watchlist["items"]),
                    }
                else:
                    return {"results": [], "total": 0}

            else:
                watchlist = self.__db["watchlists"].find_one({"id": jwtUser["id"]})
                total = self.__db["watchlists"].aggregate(
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
                    "results": cvtJson(watchlist["items"]),
                    "total": cvtJson(total)[0]["total"],
                }
        except jwt.ExpiredSignatureError as e:
            return {"is_token_expired": True, "result": "Token is expired"}
        except jwt.exceptions.DecodeError as e:
            return {"is_invalid_token": True, "result": "Token is invalid"}
        except:
            return {"success": False, "result": "Failed to search history"}

    def additem_watchlist(self):
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
                    {"id": int(media_id)},
                    {
                        "images": 0,
                        "credits": 0,
                        "videos": 0,
                        "production_companies": 0,
                    },
                )

                if movie != None:
                    item_watchlists = self.__db["watchlists"].find_one(
                        {"id": jwtUser["id"]},
                        {"items": {"$elemMatch": {"id": int(media_id)}}},
                    )

                    if "items" not in item_watchlists:
                        self.__db["watchlists"].find_one_and_update(
                            {"id": jwtUser["id"]},
                            {
                                # "$addToSet": {
                                "$push": {
                                    "items": {
                                        "$each": [
                                            {
                                                "id": int(media_id),
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
                            "results": "Add item to watchlist suucessfully",
                        }
                    else:
                        # self.__db["watchlists"].update_one(
                        #     {"items": {"$elemMatch": {"id": int(media_id)}}},
                        #     {
                        #         "$set": {
                        #             "items.$[element].percent": float(percent),
                        #             "items.$[element].seconds": float(seconds),
                        #         }
                        #     },
                        #     upsert=False,
                        #     array_filters=[
                        #         {"element.id": int(media_id)},
                        #     ],
                        # )

                        old_duration = item_watchlists["items"][0]["duration"]
                        old_seconds = item_watchlists["items"][0]["seconds"]
                        old_percent = item_watchlists["items"][0]["percent"]

                        if (
                            float(seconds) > old_seconds
                            and float(percent) > old_percent
                        ):
                            self.__db["watchlists"].find_one_and_update(
                                {"id": jwtUser["id"]},
                                {"$pull": {"items": {"id": int(media_id)}}},
                                {"new": True},
                                upsert=True,
                                return_document=ReturnDocument.AFTER,
                            )
                            self.__db["watchlists"].find_one_and_update(
                                {"id": jwtUser["id"]},
                                {
                                    # "$addToSet": {
                                    "$push": {
                                        "items": {
                                            "$each": [
                                                {
                                                    "id": int(media_id),
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
                            self.__db["watchlists"].find_one_and_update(
                                {"id": jwtUser["id"]},
                                {"$pull": {"items": {"id": int(media_id)}}},
                                {"new": True},
                                upsert=True,
                                return_document=ReturnDocument.AFTER,
                            )
                            self.__db["watchlists"].find_one_and_update(
                                {"id": jwtUser["id"]},
                                {
                                    # "$addToSet": {
                                    "$push": {
                                        "items": {
                                            "$each": [
                                                {
                                                    "id": int(media_id),
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
                            "results": "Update item from watchlist suucessfully",
                        }
                else:
                    return {
                        "success": False,
                        "results": "Failed to add item to watchlist",
                    }

            elif media_type == "tv":
                tv = self.__db["tvs"].find_one(
                    {"id": int(media_id)},
                    {
                        "images": 0,
                        "credits": 0,
                        "videos": 0,
                        "production_companies": 0,
                        "seasons": 0,
                    },
                )

                if tv != None:
                    item_watchlists = self.__db["watchlists"].find_one(
                        {"id": jwtUser["id"]},
                        {"items": {"$elemMatch": {"id": int(media_id)}}},
                    )

                    if "items" not in item_watchlists:
                        self.__db["watchlists"].find_one_and_update(
                            {"id": jwtUser["id"]},
                            {
                                # "$addToSet": {
                                "$push": {
                                    "items": {
                                        "$each": [
                                            {
                                                "id": int(media_id),
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
                            "results": "Add item to watchlist suucessfully",
                        }
                    else:
                        # self.__db["watchlists"].update_one(
                        #     {"items": {"$elemMatch": {"id": int(media_id)}}},
                        #     {
                        #         "$set": {
                        #             "items.$[element].percent": float(percent),
                        #             "items.$[element].seconds": float(seconds),
                        #         }
                        #     },
                        #     upsert=False,
                        #     array_filters=[
                        #         {"element.id": int(media_id)},
                        #     ],
                        # )

                        old_duration = item_watchlists["items"][0]["duration"]
                        old_seconds = item_watchlists["items"][0]["seconds"]
                        old_percent = item_watchlists["items"][0]["percent"]

                        if (
                            float(seconds) > old_seconds
                            and float(percent) > old_percent
                        ):
                            self.__db["watchlists"].find_one_and_update(
                                {"id": jwtUser["id"]},
                                {"$pull": {"items": {"id": int(media_id)}}},
                                {"new": True},
                                upsert=True,
                                return_document=ReturnDocument.AFTER,
                            )

                            self.__db["watchlists"].find_one_and_update(
                                {"id": jwtUser["id"]},
                                {
                                    # "$addToSet": {
                                    "$push": {
                                        "items": {
                                            "$each": [
                                                {
                                                    "id": int(media_id),
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
                            self.__db["watchlists"].find_one_and_update(
                                {"id": jwtUser["id"]},
                                {"$pull": {"items": {"id": int(media_id)}}},
                                {"new": True},
                                upsert=True,
                                return_document=ReturnDocument.AFTER,
                            )
                            self.__db["watchlists"].find_one_and_update(
                                {"id": jwtUser["id"]},
                                {
                                    # "$addToSet": {
                                    "$push": {
                                        "items": {
                                            "$each": [
                                                {
                                                    "id": int(media_id),
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
                            "results": "Update item from watchlist suucessfully",
                        }

                else:
                    return {
                        "success": False,
                        "results": "Failed to add or update item to watchlist",
                    }

        except jwt.ExpiredSignatureError as e:
            return {"is_token_expired": True, "result": "Token is expired"}
        except jwt.exceptions.DecodeError as e:
            return {"is_invalid_token": True, "result": "Token is invalid"}
        except:
            return {
                "success": False,
                "results": "Failed to add or update item to watchlist",
            }

    def remove_item_watchlist(self):
        try:
            user_token = request.headers["Authorization"].replace("Bearer ", "")

            jwtUser = jwt.decode(
                user_token,
                str(os.getenv("JWT_TOKEN_SECRET")),
                algorithms=["HS256"],
            )
            media_id = request.form["media_id"]

            self.__db["watchlists"].find_one_and_update(
                {"id": jwtUser["id"]},
                {"$pull": {"items": {"id": int(media_id)}}},
                {"new": True},
                upsert=True,
                return_document=ReturnDocument.AFTER,
            )

            list = cvtJson(self.__db["watchlists"].find_one({"id": jwtUser["id"]}))

            return {"success": True, "results": list["items"]}

        except jwt.ExpiredSignatureError as e:
            return {"is_token_expired": True, "result": "Token is expired"}
        except jwt.exceptions.DecodeError as e:
            return {"is_invalid_token": True, "result": "Token is invalid"}
        except:
            return {"success": False, "result": "Failed to remove item from watchlist"}

    def removeall_item_watchlist(self):
        try:
            user_token = request.headers["Authorization"].replace("Bearer ", "")

            jwtUser = jwt.decode(
                user_token,
                str(os.getenv("JWT_TOKEN_SECRET")),
                algorithms=["HS256"],
            )
            self.__db["watchlists"].find_one_and_update(
                {"id": jwtUser["id"]},
                {"$set": {"items": []}},
                {"new": True},
                upsert=True,
                return_document=ReturnDocument.AFTER,
            )

            list = cvtJson(self.__db["watchlists"].find_one({"id": jwtUser["id"]}))

            return {"success": True, "results": list["items"]}

        except jwt.ExpiredSignatureError as e:
            return {"is_token_expired": True, "result": "Token is expired"}
        except jwt.exceptions.DecodeError as e:
            return {"is_invalid_token": True, "result": "Token is invalid"}
        except:
            return {
                "success": False,
                "result": "Failed to remove all item from watchlist",
            }
