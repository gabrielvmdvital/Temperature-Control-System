import json


def load_config(path: str) -> dict:
    with open(path, encoding='utf-8') as fp:
        data = json.load(fp)
    return data

