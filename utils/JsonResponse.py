from bson import json_util, ObjectId
import json


def ConvertJsonResponse(data):
    return json.loads(json_util.dumps(data))
