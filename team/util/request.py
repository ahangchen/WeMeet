from django.http import HttpResponse
from student.utility import json_helper
from team.ctrl.err_code_msg import ERROR_METHOD, ERROR_METHOD_MSG


def is_post(request):
    return request.method == 'POST'


def resp_method_err():
    return HttpResponse(json_helper.dump_err_msg(ERROR_METHOD, ERROR_METHOD_MSG))

