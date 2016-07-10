# coding=utf8
from django.http import HttpResponse
from django.shortcuts import render  # for test method
from django.views.decorators.csrf import csrf_exempt

from student.bussiness_logic import info
from student.bussiness_logic import account
from student.bussiness_logic.err_code_msg import ERROR_ACCOUNT_DOESNOTEXIST
from student.bussiness_logic.err_code_msg import ERROR_ACCOUNT_DOESNOTEXIST_MSG
# from student.bussiness_logic.err_code_msg import ERROR_CHANGE_PWD
# from student.bussiness_logic.err_code_msg import ERROR_CHANGE_PWD_MSG
# from student.bussiness_logic.err_code_msg import ERROR_GET_STU_DOESNOTEXIST
# from student.bussiness_logic.err_code_msg import ERROR_GET_STU_DOESNOTEXIST_MSG
# from student.bussiness_logic.err_code_msg import ERROR_GET_STU_IDMISS
# from student.bussiness_logic.err_code_msg import ERROR_GET_STU_IDMISS_MSG
from student.bussiness_logic.err_code_msg import ERROR_METHOD
from student.bussiness_logic.err_code_msg import ERROR_METHOD_MSG
from student.bussiness_logic.err_code_msg import ERROR_REGISTER_IDEXIST
from student.bussiness_logic.err_code_msg import ERROR_REGISTER_IDEXIST_MSG
# from student.bussiness_logic.err_code_msg import ERROR_UPDATE_STU_AVATAR_INVALID
# from student.bussiness_logic.err_code_msg import ERROR_UPDATE_STU_AVATAR_INVALID_MSG
# from student.bussiness_logic.err_code_msg import ERROR_UPDATE_STU_AVATAR_SAVE_FAILED
# from student.bussiness_logic.err_code_msg import ERROR_UPDATE_STU_AVATAR_SAVE_FAILED_MSG
# from student.bussiness_logic.err_code_msg import ERROR_UPDATE_STU_DOESNOTEXIST
# from student.bussiness_logic.err_code_msg import ERROR_UPDATE_STU_DOESNOTEXIST_MSG
# from student.bussiness_logic.err_code_msg import ERROR_UPDATE_STU_IDMISS
# from student.bussiness_logic.err_code_msg import ERROR_UPDATE_STU_IDMISS_MSG
# from student.bussiness_logic.err_code_msg import ERROR_VERIFY_STU
# from student.bussiness_logic.err_code_msg import ERROR_LOGIN_STU_DOESNOTEXIST
# from student.bussiness_logic.err_code_msg import ERROR_LOGIN_STU_DOESNOTEXIST_MSG
from student.bussiness_logic.err_code_msg import ERROR_LOGIN_STU_NONACTIVATED
from student.bussiness_logic.err_code_msg import ERROR_LOGIN_STU_NONACTIVATED_MSG
from student.bussiness_logic.err_code_msg import ERROR_LOGIN_STU_WRONG_PWD
from student.bussiness_logic.err_code_msg import ERROR_LOGIN_STU_WRONG_PWD_MSG
from student.bussiness_logic.err_code_msg import ERROR_STU_DOESNOTEXIST
from student.bussiness_logic.err_code_msg import ERROR_STU_DOESNOTEXIST_MSG
from student.bussiness_logic.err_code_msg import ERROR_WRONG_CREDENTIAL
from student.bussiness_logic.err_code_msg import ERROR_WRONG_CREDENTIAL_MSG

from student.bussiness_logic.err_code_msg import SUCCEED

from student.bussiness_logic.tag import ERROR_AVATAR_FILE_INVALID
from student.bussiness_logic.tag import ERROR_AVATAR_SAVE_FAILED
from student.bussiness_logic.tag import ERROR_ACTIVATE_DOESNOTEXIST
from student.bussiness_logic.tag import ERROR_CHANGE_PWD_DOESNOTEXIST
from student.bussiness_logic.tag import ERROR_GET_INFO_DOESNOTEXIST
from student.bussiness_logic.tag import ERROR_LOGIN_DOESNOTEXIST
from student.bussiness_logic.tag import ERROR_LOGIN_NONACTIVATED
from student.bussiness_logic.tag import ERROR_LOGIN_WRONG_PWD
from student.bussiness_logic.tag import ERROR_RESET_DOESNOTEXIST
from student.bussiness_logic.tag import GOOD_LOGIN
from student.bussiness_logic.tag import GOOD_REGISTER
from student.bussiness_logic.tag import GOOD_UPDATE_INFO
from student.bussiness_logic.tag import GOOD_CHANGE_PWD
from student.bussiness_logic.tag import GOOD_RESET_MAIL

from student.utility.tag import NO_INPUT
from student.utility import json_helper


def post(request):
    """  test  """
    return render(request, 'post.html')


@csrf_exempt
def register(request):
    if request.method == "POST":
        acnt = request.POST.get('account')
        pwd = request.POST.get('pwd')

        tag = account.register(account=acnt, pwd=pwd)
        # 如果注册成功
        if tag == GOOD_REGISTER:
            err = SUCCEED
            json_ctx = {'err': err}
        # 如果账号已存在
        else:
            err = ERROR_REGISTER_IDEXIST
            msg = ERROR_REGISTER_IDEXIST_MSG
            json_ctx = {'err': err, 'msg': msg}
        return HttpResponse(json_helper.dumps(json_ctx))

    # 如果请求的方法是GET
    json_ctx = {'err': ERROR_METHOD, 'msg': ERROR_METHOD_MSG}
    return HttpResponse(json_helper.dumps(json_ctx))


@csrf_exempt
def activate(request):
    """
    账号激活
    成功返回 {err：SUCCEED}
    失败返回相应err和msg的JSON
    """
    if request.method == 'POST':
        cipher = request.POST.get('account')  # cipher: 由后端加密后的stu_id, 只能通过邮件获得

        tag = account.activate(account_cipher=cipher)
        # 如果账号不存在
        if tag == ERROR_ACTIVATE_DOESNOTEXIST:
            return HttpResponse(json_helper.dumps(
                {'err': ERROR_ACCOUNT_DOESNOTEXIST, 'msg': ERROR_ACCOUNT_DOESNOTEXIST_MSG}
            ))
        # 如果激活成功
        return HttpResponse(json_helper.dumps({'err': SUCCEED}))

    # 如果请求的方法是GET
    else:
        return HttpResponse(json_helper.dumps(
            {'err': ERROR_METHOD, 'msg': ERROR_METHOD_MSG}
        ))


@csrf_exempt
def login(request):
    """
    登陆
    成功：返回 {'err': SUCCEED }
    失败：返回相应的err和msg的JSON
    """
    if request.method == 'POST':
        acnt = request.POST.get('account')
        pwd = request.POST.get('pwd')

        tag = account.login(account=acnt, pwd=pwd)
        # 如果登陆成功
        if tag == GOOD_LOGIN:
            json_ctx = {'err': SUCCEED}
        # 如果账号未激活
        elif tag == ERROR_LOGIN_NONACTIVATED:
            json_ctx = {'err': ERROR_LOGIN_STU_NONACTIVATED,
                        'msg': ERROR_LOGIN_STU_NONACTIVATED_MSG}
        # 如果密码错误
        elif tag == ERROR_LOGIN_WRONG_PWD:
            json_ctx = {'err': ERROR_LOGIN_STU_WRONG_PWD,
                        'msg': ERROR_LOGIN_STU_WRONG_PWD_MSG}
        # 如果账号不存在（tag == ERROR_LOGIN_DOESNOTEXIST）
        else:
            json_ctx = {'err': ERROR_ACCOUNT_DOESNOTEXIST,
                        'msg': ERROR_ACCOUNT_DOESNOTEXIST_MSG}
        return HttpResponse(json_helper.dumps(json_ctx))

    # 如果请求的方法是GET
    else:
        return HttpResponse(json_helper.dumps(
            {'err': ERROR_METHOD, 'msg': ERROR_METHOD_MSG}
        ))


@csrf_exempt
def send_rsmail(request):
    """
    发送账号重置邮件
    send_rsmail: send reset mail
    成功: 返回 {err: SUCCEED}
    失败：返回相应的err和msg的JSON
    """
    if request.method == 'POST':
        acnt = request.POST.get('account')
        tag = account.send_reset_mail(acnt)

        if tag == GOOD_RESET_MAIL:
            return HttpResponse(json_helper.dumps({'err': SUCCEED}))
        # 如果账号不存在（tag == ERROR_RESET_MAIL_DOESNOTEXIST）
        else:
            return HttpResponse(json_helper.dumps(
                {'err': ERROR_ACCOUNT_DOESNOTEXIST, 'msg': ERROR_ACCOUNT_DOESNOTEXIST_MSG}
            ))

    # 如果请求的方法是GET
    else:
        return HttpResponse(json_helper.dumps(
            {'err': ERROR_METHOD, 'msg': ERROR_METHOD_MSG}
        ))


@csrf_exempt
def reset(request):
    """
    重置密码，修改账号状态为未激活
    成功：返回{'err': SUCCEED, 'credential': credential, 'account': acnt}
                              credential: 用户修改密码的凭据; account: 未加密的账号
    失败：返回相应的err和msg
    """
    if request.method == 'POST':
        account_cipher = request.POST['account']  # account_cipher: 由后端加密后的account，只能通过邮件获得

        obj = account.reset(account_cipher)
        # 如果账号不存在
        if obj == ERROR_RESET_DOESNOTEXIST:
            return HttpResponse(json_helper.dumps(
                {'err': ERROR_ACCOUNT_DOESNOTEXIST, 'msg': ERROR_ACCOUNT_DOESNOTEXIST_MSG}
            ))
        # 如果账号存在，obj是{'credential': credential, 'account': account}
        else:
            credential = obj['credential']
            acnt = obj['account']
            return HttpResponse(json_helper.dumps(
                {'err': SUCCEED,
                 'credential': credential,
                 'account': acnt}
            ))

    # 如果请求的方法是GET
    else:
        return HttpResponse(json_helper.dumps(
            {'err': ERROR_METHOD, 'msg': ERROR_METHOD_MSG}
        ))


@csrf_exempt
def change_pwd(request):
    """
    修改密码
    成功: 返回 {err: SUCCEED}
    失败：返回相应的err和msg的JSON
    """
    if request.method == 'POST':
        acnt = request.POST.get('account')
        credential = request.POST.get('credential')
        pwd = request.POST.get('pwd')

        tag = account.change_pwd(acnt, credential, pwd)
        # 如果修改密码成功
        if tag == GOOD_CHANGE_PWD:
            return HttpResponse(json_helper.dumps({'err': SUCCEED}))
        # 如果账号不存在
        elif tag == ERROR_CHANGE_PWD_DOESNOTEXIST:
            return HttpResponse(json_helper.dumps(
                {'err': ERROR_ACCOUNT_DOESNOTEXIST, 'msg': ERROR_ACCOUNT_DOESNOTEXIST_MSG}
            ))
        # 如果凭据错误（tag == ERROR_CHANGE_PWD_WRONG_CREDENTIAL)
        else:
            return HttpResponse(json_helper.dumps(
                {'err': ERROR_WRONG_CREDENTIAL,
                 'msg': ERROR_WRONG_CREDENTIAL_MSG}
            ))

    # 如果请求的方法是GET
    else:
        return HttpResponse(json_helper.dumps(
            {'err': ERROR_METHOD, 'msg': ERROR_METHOD_MSG}
        ))


@csrf_exempt
def get_info(request):
    """
    获取学生信息
    成功： 返回err: SUCCEED，头像路径，姓名，学校，学历，年级，专业，所在地，联系方式（tel），邮箱
    失败：返回相应的err和msg的JSON
    """
    if request.method == 'POST':
        acnt = request.POST.get('account')
        obj = info.get(acnt)
        # 如果学生不存在
        if obj == ERROR_GET_INFO_DOESNOTEXIST:
            return HttpResponse(json_helper.dumps(
                {'err': ERROR_STU_DOESNOTEXIST, 'msg': ERROR_STU_DOESNOTEXIST_MSG}
            ))
        # 如果获取学生信息成功, 返回前端请求的信息
        else:
            return HttpResponse(json_helper.dumps(
                {'err': SUCCEED,
                 'avatar_path': obj.avatar_path,
                 'name': obj.name,
                 'school': obj.school,
                 'edu_background': obj.edu_background,
                 'grade': obj.grade,
                 'major': obj.major,
                 'location': obj.location,
                 'tel': obj.tel,
                 'mail': obj.mail}
            ))

    # 如果请求的方法是GET
    else:
        return HttpResponse(json_helper.dumps(
            {'err': ERROR_METHOD, 'msg': ERROR_METHOD_MSG}
        ))


# @csrf_exempt
# def change_pwd(request):
#     if request.method == 'POST':
#         stu_id = request.POST.get('mail')
#         pwd = request.POST.get('pwd')
#         tag = account.change_pwd(stu_id, pwd)
#         if tag == GOOD_CHANGE_PWD:
#             return HttpResponse(json_helper.dump({'err': SUCCEED}))
#         # tag == ERROR_CHANGE_PWD_DOESNOTEXIST
#         else:
#             return HttpResponse(json_helper.dump(
#                 {'err': ERROR_CHANGE_PWD, 'msg': ERROR_CHANGE_PWD_MSG}
#             ))
#     # 如果请求方法错误
#     return HttpResponse(json_helper.dump(
#         {'err': ERROR_METHOD, 'msg': ERROR_METHOD_MSG}
#     ))

# @csrf_exempt
# def update_stu_info(request):
#     if request.method == "POST":
#         stu_id = request.POST.get('stu_id', NO_INPUT)
#         # check if stu_id is posted
#         if stu_id == NO_INPUT:
#             json_ctx = {'err': ERROR_UPDATE_STU_IDMISS,
#                         'msg': ERROR_UPDATE_STU_IDMISS_MSG}
#             return HttpResponse(json.dumps(json_ctx, ensure_ascii=False))
#
#         # if stu_id is posted
#         stu_name = request.POST.get('stu_name', NO_INPUT)
#         stu_school = request.POST.get('stu_school', NO_INPUT)
#         stu_tel = request.POST.get('stu_tel', NO_INPUT)
#         stu_mail = request.POST.get('stu_mail', NO_INPUT)
#         stu_avatar = request.FILES.get('stu_avatar', NO_INPUT)
#
#         tag = stu_info_op.update_info(stu_id=stu_id,
#                                       name=stu_name,
#                                       school=stu_school,
#                                       tel=stu_tel,
#                                       mail=stu_mail,
#                                       avatar=stu_avatar)
#
#         if tag == GOOD_UPDATE_INFO:
#             err = SUCCEED
#             msg = SUCCEED_UPDATE_STU_MSG
#         elif tag == ERROR_AVATAR_SAVE_FAILED:
#             err = ERROR_UPDATE_STU_AVATAR_SAVE_FAILED
#             msg = ERROR_UPDATE_STU_AVATAR_SAVE_FAILED_MSG
#         elif tag == ERROR_AVATAR_FILE_INVALID:
#             err = ERROR_UPDATE_STU_AVATAR_INVALID
#             msg = ERROR_UPDATE_STU_AVATAR_INVALID_MSG
#         else:
#             err = ERROR_UPDATE_STU_DOESNOTEXIST
#             msg = ERROR_UPDATE_STU_DOESNOTEXIST_MSG
#
#         json_ctx = {'err': err, 'msg': msg}
#         return HttpResponse(json.dumps(json_ctx, ensure_ascii=False))
#
#     # if request method is get
#     json_ctx = {'err': ERROR_METHOD, 'msg': ERROR_METHOD_MSG}
#     return HttpResponse(json.dumps(json_ctx, ensure_ascii=False))
#
#
# @csrf_exempt
# def get_stu_info(request):
#     if request.method == "POST":
#         stu_id = request.POST.get('stu_id', NO_INPUT)
#         # check if stu_id is posted
#         if stu_id == NO_INPUT:
#             json_ctx = {'err': ERROR_GET_STU_IDMISS,
#                         'msg': ERROR_GET_STU_IDMISS_MSG}
#             return HttpResponse(json.dumps(json_ctx, ensure_ascii=False))
#
#         # if stu_id is posted
#         temp = stu_info_op.get_info(stu_id)
#         # if stu_id exists and return a Stuinfo
#         if temp != ERROR_GET_INFO:
#             err = SUCCEED
#             msg = SUCCEED_GET_STU_MSG
#             json_ctx = {'err': err,
#                         'msg': msg,
#                         'stu_id': temp.id,
#                         'stu_name': temp.name,
#                         'stu_school': temp.school,
#                         'stu_tel': temp.tel,
#                         'stu_mail': temp.mail,
#                         'stu_avatar': temp.avatar_path}
#             return HttpResponse(json.dumps(json_ctx, ensure_ascii=False))
#
#         # if stu_id does not exist
#         json_ctx = {'err': ERROR_GET_STU_DOESNOTEXIST,
#                     'msg': ERROR_GET_STU_DOESNOTEXIST_MSG}
#         return HttpResponse(json.dumps(json_ctx, ensure_ascii=False))
#
#     # if post method is get
#     json_ctx = {'err': ERROR_METHOD, 'msg': ERROR_METHOD_MSG}
#     return HttpResponse(json.dumps(json_ctx, ensure_ascii=False))
#
















