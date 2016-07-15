import json


def dumps(json_ctx):
    return json.dumps(json_ctx, ensure_ascii=False)


def dict2err_json(err_code, res_dict):
    return "{'err': %d, 'res': '%s'}" % (err_code, dumps(res_dict))
