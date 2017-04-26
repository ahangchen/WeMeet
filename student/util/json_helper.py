import json


def dumps(json_ctx):
    return json.dumps(json_ctx, ensure_ascii=False)


def dumps_err(err_code, json_ctx):
    return json.dumps({'err': err_code, 'res': json_ctx}, ensure_ascii=False)


def dump_err_msg(err_code, err_msg):
    return json.dumps({'err': err_code, 'msg': err_msg}, ensure_ascii=False)
