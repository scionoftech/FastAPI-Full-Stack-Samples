import json


def get_json(data):
    return json.loads(data.to_json())
