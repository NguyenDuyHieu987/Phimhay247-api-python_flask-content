import pymongo
from pymongo.errors import PyMongoError
from utils.JsonResponse import ConvertJsonResponse as cvtJson
from utils.ErrorMessage import errorMessage
from flask import *

myclient = pymongo.MongoClient(
    "mongodb+srv://admin:hieusen123@the-movie-database.fczrzon.mongodb.net/Phimhay247_DB"
)

db = myclient["Phimhay247_DB"]


def detail_tv(id):
    try:
        append_to_response = request.args.get(
            "append_to_response", default="", type=str
        )
        exceptValue = {"images": 0, "credits": 0, "videos": 0}

        if append_to_response != "":
            if "images" in append_to_response.split(","):
                exceptValue.pop("images")
            if "credits" in append_to_response.split(","):
                exceptValue.pop("credits")
            if "videos" in append_to_response.split(","):
                exceptValue.pop("videos")

        tv = db["tvs"].find_one({"id": int(id)}, exceptValue)
        if tv != None:
            return cvtJson(tv)
        else:
            return {"not_found": True}

    except:
        return {}


def edit_tv(id):
    try:
        formMovie = request.form
        db["hieus"].update_one(
            {"id": int(id)},
            {
                "$set": {
                    "title": formMovie["title"],
                    "original_title": formMovie["original_title"],
                    "original_language": formMovie["original_language"],
                    "release_date": formMovie["release_date"],
                    "genres": formMovie["genres"],
                    "overview": formMovie["overview"],
                    "budget": int(formMovie["budget"]),
                    "revenue": int(formMovie["revenue"]),
                    "runtime": int(formMovie["runtime"]),
                    "status": formMovie["status"],
                },
            },
        )
        return {"success": True, "result": "Edit tv successfully"}
    except:
        return {"success": False, "result": "Edit tv failed"}


def update_view_tv(id):
    try:
        tv_dumps = db["tvs"].find_one({"id": int(id)})
        new_views = int(tv_dumps["views"]) + 1

        db["tvs"].update_one(
            {"id": int(id)},
            {
                "$set": {
                    "views": new_views,
                },
            },
        )
        return {"success": True, "result": "Update views of tv successfully"}
    except:
        return {"success": False, "result": "Update views of tv failed"}
