# coding=utf8
import json
from django.http import HttpResponse
from django.shortcuts import render  # for test method
from django.views.decorators.csrf import csrf_exempt

from student.bussiness_logic import stu_info_op
from student.bussiness_logic.err_code_msg import ERROR_GET_STU_DOESNOTEXIST
from student.bussiness_logic.err_code_msg import ERROR_GET_STU_DOESNOTEXIST_MSG
from student.bussiness_logic.err_code_msg import ERROR_GET_STU_IDMISS
from student.bussiness_logic.err_code_msg import ERROR_GET_STU_IDMISS_MSG
from student.bussiness_logic.err_code_msg import ERROR_METHOD
from student.bussiness_logic.err_code_msg import ERROR_METHOD_MSG
from student.bussiness_logic.err_code_msg import ERROR_REGISTER_IDEXIST
from student.bussiness_logic.err_code_msg import ERROR_REGISTER_IDEXIST_MSG
from student.bussiness_logic.err_code_msg import ERROR_UPDATE_STU_AVATAR_INVALID
from student.bussiness_logic.err_code_msg import ERROR_UPDATE_STU_AVATAR_INVALID_MSG
from student.bussiness_logic.err_code_msg import ERROR_UPDATE_STU_AVATAR_SAVE_FAILED
from student.bussiness_logic.err_code_msg import ERROR_UPDATE_STU_AVATAR_SAVE_FAILED_MSG
from student.bussiness_logic.err_code_msg import ERROR_UPDATE_STU_DOESNOTEXIST
from student.bussiness_logic.err_code_msg import ERROR_UPDATE_STU_DOESNOTEXIST_MSG
from student.bussiness_logic.err_code_msg import ERROR_UPDATE_STU_IDMISS
from student.bussiness_logic.err_code_msg import ERROR_UPDATE_STU_IDMISS_MSG
from student.bussiness_logic.err_code_msg import SUCCEED
from student.bussiness_logic.err_code_msg import SUCCEED_GET_STU_MSG
from student.bussiness_logic.err_code_msg import SUCCEED_REGISTER_MSG
from student.bussiness_logic.err_code_msg import SUCCEED_UPDATE_STU_MSG

from student.bussiness_logic.tag import ERROR_AVATAR_FILE_INVALID
from student.bussiness_logic.tag import ERROR_AVATAR_SAVE_FAILED
from student.bussiness_logic.tag import ERROR_GET_INFO
from student.bussiness_logic.tag import GOOD_REGISTER
from student.bussiness_logic.tag import GOOD_UPDATE_INFO

from student.utility.tag import NO_INPUT


def post(request):
    """method for test"""
    return render(request, 'post.html')


@csrf_exempt
def register_stu(request):
    if request.method == "POST":
        stu_id = request.POST.get('stu_id')
        pwd = request.POST.get('pwd')

        tag = stu_info_op.register(stu_id=stu_id, pwd=pwd)
        if tag == GOOD_REGISTER:
            err = SUCCEED
            msg = SUCCEED_REGISTER_MSG
        else:
            err = ERROR_REGISTER_IDEXIST
            msg = ERROR_REGISTER_IDEXIST_MSG

        json_ctx = {'err': err, 'msg': msg}
        return HttpResponse(json.dumps(json_ctx, ensure_ascii=False))

    # if request method is get
    json_ctx = {'err': ERROR_METHOD, 'msg': ERROR_METHOD_MSG}
    return HttpResponse(json.dumps(json_ctx, ensure_ascii=False))


@csrf_exempt
def update_stu_info(request):
    if request.method == "POST":
        stu_id = request.POST.get('stu_id', NO_INPUT)
        # check if stu_id is posted
        if stu_id == NO_INPUT:
            json_ctx = {'err': ERROR_UPDATE_STU_IDMISS,
                        'msg': ERROR_UPDATE_STU_IDMISS_MSG}
            return HttpResponse(json.dumps(json_ctx, ensure_ascii=False))

        # if stu_id is posted
        stu_name = request.POST.get('stu_name', NO_INPUT)
        stu_school = request.POST.get('stu_school', NO_INPUT)
        stu_tel = request.POST.get('stu_tel', NO_INPUT)
        stu_mail = request.POST.get('stu_mail', NO_INPUT)
        stu_avatar = request.FILES.get('stu_avatar', NO_INPUT)

        tag = stu_info_op.update_info(stu_id=stu_id,
                                      name=stu_name,
                                      school=stu_school,
                                      tel=stu_tel,
                                      mail=stu_mail,
                                      avatar=stu_avatar)

        if tag == GOOD_UPDATE_INFO:
            err = SUCCEED
            msg = SUCCEED_UPDATE_STU_MSG
        elif tag == ERROR_AVATAR_SAVE_FAILED:
            err = ERROR_UPDATE_STU_AVATAR_SAVE_FAILED
            msg = ERROR_UPDATE_STU_AVATAR_SAVE_FAILED_MSG
        elif tag == ERROR_AVATAR_FILE_INVALID:
            err = ERROR_UPDATE_STU_AVATAR_INVALID
            msg = ERROR_UPDATE_STU_AVATAR_INVALID_MSG
        else:
            err = ERROR_UPDATE_STU_DOESNOTEXIST
            msg = ERROR_UPDATE_STU_DOESNOTEXIST_MSG

        json_ctx = {'err': err, 'msg': msg}
        return HttpResponse(json.dumps(json_ctx, ensure_ascii=False))

    # if request method is get
    json_ctx = {'err': ERROR_METHOD, 'msg': ERROR_METHOD_MSG}
    return HttpResponse(json.dumps(json_ctx, ensure_ascii=False))


@csrf_exempt
def get_stu_info(request):
    if request.method == "POST":
        stu_id = request.POST.get('stu_id', NO_INPUT)
        # check if stu_id is posted
        if stu_id == NO_INPUT:
            json_ctx = {'err': ERROR_GET_STU_IDMISS,
                        'msg': ERROR_GET_STU_IDMISS_MSG}
            return HttpResponse(json.dumps(json_ctx, ensure_ascii=False))

        # if stu_id is posted
        temp = stu_info_op.get_info(stu_id)
        # if stu_id exists and return a Stuinfo
        if temp != ERROR_GET_INFO:
            err = SUCCEED
            msg = SUCCEED_GET_STU_MSG
            json_ctx = {'err': err,
                        'msg': msg,
                        'stu_id': temp.id,
                        'stu_name': temp.name,
                        'stu_school': temp.school,
                        'stu_tel': temp.tel,
                        'stu_mail': temp.mail,
                        'stu_avatar': temp.avatar_path}
            return HttpResponse(json.dumps(json_ctx, ensure_ascii=False))

        # if stu_id does not exist
        json_ctx = {'err': ERROR_GET_STU_DOESNOTEXIST,
                    'msg': ERROR_GET_STU_DOESNOTEXIST_MSG}
        return HttpResponse(json.dumps(json_ctx, ensure_ascii=False))

    # if post method is get
    json_ctx = {'err': ERROR_METHOD, 'msg': ERROR_METHOD_MSG}
    return HttpResponse(json.dumps(json_ctx, ensure_ascii=False))


















