from django.http import HttpResponse
from student.util import json_helper
from team.ctrl.err_code_msg import ERROR_METHOD, MSG_METHOD_ERR, ERR_VALID_CODE, MSG_VALID_CODE_ERR


def is_post(request):
    return request.method == 'POST'


def resp_method_err():
    return HttpResponse(json_helper.dump_err_msg(ERROR_METHOD, MSG_METHOD_ERR))


def is_valid_ok(request):
    print(request.session['code'])
    print(request.POST['code'])
    return request.session['code'].upper() == request.POST.get('code').upper()
    # return True


def resp_valid_err():
    return HttpResponse(json_helper.dump_err_msg(ERR_VALID_CODE, MSG_VALID_CODE_ERR))