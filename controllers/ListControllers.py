import pymongo
from pymongo.errors import PyMongoError
from utils.JsonResponse import ConvertJsonResponse as cvtJson
from utils.ErrorMessage import errorMessage
from flask import *
from pymongo import ReturnDocument
from datetime import datetime

myclient = pymongo.MongoClient(
    "mongodb+srv://admin:hieusen123@the-movie-database.fczrzon.mongodb.net/Phimhay247_DB"
)

db = myclient["Phimhay247_DB"]


def getlist(idlist):
    skip = request.args.get("skip", default=0, type=int)
    if skip == 0:
        list = db["lists"].find_one(
            {"id": idlist}, {"items": {"$slice": [skip * 20, 20]}}
        )

        total = db["lists"].aggregate(
            [
                {"$match": {"id": str(idlist)}},
                {
                    "$project": {
                        "total": {"$size": "$items"},
                        #   "result": "$items"
                    }
                },
            ]
        )
        # total = db["lists"].find_one({"id": idlist})

        return {"result": cvtJson(list), "total": cvtJson(total)[0]["total"]}

    elif skip > 0:
        list = db["lists"].find_one(
            {"id": idlist}, {"items": {"$slice": [skip * 20, 20]}}
        )

        return {"result": cvtJson(list["items"]), "total": len(list["items"])}


def search_list(idlist):
    # skip = request.args.get("skip", default=0, type=int)
    query = request.args.get("query", default="", type=str)

    if len(query) != 0:
        list = db["lists"].find_one(
            {"id": idlist},
            {
                "items": {
                    "$elemMatch": {
                        "$or": [
                            {"name": {"$regex": query, "$options": "i"}},
                            {"title": {"$regex": query, "$options": "i"}},
                            {"original_title": {"$regex": query, "$options": "i"}},
                            {"original_name": {"$regex": query, "$options": "i"}},
                        ],
                    },
                }
            },
        )
        if "items" in list:
            return {"results": cvtJson(list["items"]), "total": len(list["items"])}
        else:
            return {"results": [], "total": 0}

    else:
        list = db["lists"].find_one({"id": idlist})
        total = db["lists"].aggregate(
            [
                {"$match": {"id": str(idlist)}},
                {
                    "$project": {
                        "total": {"$size": "$items"},
                        #   "result": "$items"
                    }
                },
            ]
        )
        return {"results": cvtJson(list["items"]), "total": cvtJson(total)[0]["total"]}


def getitem_list(idlist, idmovie):
    try:
        item_lists = db["lists"].find_one(
            {"id": idlist}, {"items": {"$elemMatch": {"id": int(idmovie)}}}
        )
        if "items" in item_lists:
            return {"success": True, "result": cvtJson(item_lists["items"][0])}
        else:
            return {"success": False, "result": "Fail to get item in list"}

    except:
        return {"success": False, "result": "Fail to get item in list"}


def additem_list(idlist):
    try:
        media_type = request.form["media_type"]
        media_id = request.form["media_id"]

        if media_type == "movie":
            movie = db["movies"].find_one(
                {"id": int(media_id)},
                {
                    "images": 0,
                    "credits": 0,
                    "videos": 0,
                    "production_companies": 0,
                },
            )

            if movie != None:
                item_lists = db["lists"].find_one(
                    {"id": idlist}, {"items": {"$elemMatch": {"id": int(media_id)}}}
                )
                if "items" in item_lists:
                    return {
                        "success": False,
                        "exist": True,
                        "result": "Movie already exist in list",
                    }
                else:
                    db["lists"].find_one_and_update(
                        {"id": idlist},
                        {
                            # "$addToSet": {
                            "$push": {
                                "items": {
                                    "$each": [
                                        {
                                            "id": int(media_id),
                                            "title": movie["title"],
                                            "original_title": movie["original_title"],
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
                    return {"success": True, "results": "Add item to list suucessfully"}
            else:
                return {
                    "success": False,
                    "results": "Failed to add item to list",
                }

        elif media_type == "tv":
            tv = db["tvs"].find_one(
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
                item_lists = db["lists"].find_one(
                    {"id": idlist}, {"items": {"$elemMatch": {"id": int(media_id)}}}
                )
                if "items" in item_lists:
                    return {
                        "success": False,
                        "exist": True,
                        "result": "Tv already exist in list",
                    }
                else:
                    db["lists"].find_one_and_update(
                        {"id": idlist},
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
                    return {"success": True, "results": "Add item to list suucessfully"}
            else:
                return {
                    "success": False,
                    "results": "Failed to add item to list",
                }
    except:
        return {
            "success": False,
            "results": "Failed to add item to list",
        }


def remove_item_list(idlist):
    try:
        media_id = request.form["media_id"]

        db["lists"].find_one_and_update(
            {"id": idlist},
            {"$pull": {"items": {"id": int(media_id)}}},
            {"new": True},
            upsert=True,
            return_document=ReturnDocument.AFTER,
        )

        list = cvtJson(db["lists"].find_one({"id": idlist}))

        return {"success": True, "results": list["items"]}
    except:
        return {"success": False, "result": "Failed to remove item from list"}


def removeall_item_list(idlist):
    try:
        db["lists"].find_one_and_update(
            {"id": idlist},
            {"$set": {"items": []}},
            {"new": True},
            upsert=True,
            return_document=ReturnDocument.AFTER,
        )

        list = cvtJson(db["lists"].find_one({"id": idlist}))

        return {"success": True, "results": list["items"]}
    except:
        return {"success": False, "result": "Failed to remove all item from list"}
