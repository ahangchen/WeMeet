import json


def dumps(json_ctx):
    return json.dumps(json_ctx, ensure_ascii=False)
