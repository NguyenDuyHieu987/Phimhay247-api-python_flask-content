import pymongo
from collections import ChainMap
from bson import json_util, ObjectId
from utils.JsonResponse import ConvertJsonResponse as cvtJson
import json
from collections import defaultdict
import pyfpgrowth
from flask import *


myclient = pymongo.MongoClient(
    "mongodb+srv://admin:hieusen123@the-movie-database.fczrzon.mongodb.net/Phimhay247_DB"
)

db = myclient["Phimhay247_DB"]


def get_recommend(userid):
    skip = request.args.get("skip", default=1, type=int) - 1

    list = db["lists"].find_one({"id": str(userid)}, {"items": {"$slice": [0, 20]}})
    watchlist = db["watchlists"].find_one(
        {"id": str(userid)}, {"items": {"$slice": [0, 20]}}
    )

    genres = []
    countries = []
    for x in list["items"]:
        genres.append([x1["id"] for x1 in x["genres"]])
        countries.append([x["original_language"]])

    for x in watchlist["items"]:
        genres.append([x1["id"] for x1 in x["genres"]])
        countries.append([x["original_language"]])

    if len(genres) == 0 and len(countries) == 0:
        return {"results": []}
    else:
        patterns_genres = pyfpgrowth.find_frequent_patterns(genres, 5)

        if len(patterns_genres) == 0:
            patterns_genres = pyfpgrowth.find_frequent_patterns(genres, 1)

        patterns_genres_single = [
            (item[0], item1)
            for item, item1 in patterns_genres.items()
            if len(item) == 1
        ]

        patterns_countries = pyfpgrowth.find_frequent_patterns(countries, 3)

        if len(patterns_countries) == 0:
            patterns_countries = pyfpgrowth.find_frequent_patterns(countries, 1)

        patterns_genres_desc = sorted(
            patterns_genres_single,
            key=lambda item: item[1],
            reverse=True,
        )

        patterns_countries_desc = sorted(
            patterns_countries.items(), key=lambda item: item[1], reverse=True
        )

        frequency_genres_dict = []

        for pattern in patterns_genres_desc:
            frequency_genres_dict.append(({"id": pattern[0]}))

        frequency_countries_list = [x for x in patterns_countries_desc[0][0]]

        movie = cvtJson(
            db["movies"]
            .find(
                {
                    "$and": [
                        {"original_language": {"$in": frequency_countries_list}},
                        {
                            "genres": {
                                "$elemMatch": {
                                    "$or": [ChainMap(*frequency_genres_dict)]
                                }
                            }
                        },
                    ]
                },
                {"images": 0, "credits": 0, "videos": 0, "production_companies": 0},
            )
            .skip(skip * 10)
            .limit(10)
            .sort([("views", pymongo.DESCENDING)])
        )

        tv = cvtJson(
            db["tvs"]
            .find(
                {
                    "$and": [
                        {"original_language": {"$in": frequency_countries_list}},
                        {
                            "genres": {
                                "$elemMatch": {
                                    "$or": [ChainMap(*frequency_genres_dict)]
                                }
                            }
                        },
                    ]
                },
                {"images": 0, "credits": 0, "videos": 0, "production_companies": 0},
            )
            .skip(skip * 10)
            .limit(10)
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
