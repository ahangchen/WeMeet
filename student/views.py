# coding=utf8
from django.http import HttpResponse
from django.shortcuts import render  # for test method
from django.views.decorators.csrf import csrf_exempt

from student.bussiness_logic import info
from student.bussiness_logic import account
from student.bussiness_logic import avatar
from student.bussiness_logic.err_code_msg import ERR_LOGIN_STU_NONACTIVATED, ERR_LOGIN_STU_NONACTIVATED_MSG, \
                                                 ERR_LOGIN_STU_WRONG_PWD, ERR_LOGIN_STU_WRONG_PWD_MSG, \
                                                 ERR_ACCOUNT_NOTEXIST, ERR_ACCOUNT_NOTEXIST_MSG, \
                                                 ERR_WRONG_CREDENTIAL, ERR_WRONG_CREDENTIAL_MSG, \
                                                 ERR_STU_NOTEXIST, ERR_STU_NOTEXIST_MSG, \
                                                 ERR_REG_IDEXIST, ERR_REG_IDEXIST_MSG, \
                                                 ERR_VALID_CODE, ERR_VALID_CODE_MSG, \
                                                 AVATAR_INVALID, AVATAR_INVALID_MSG,\
                                                 ERR_OUT_DATE, ERR_OUT_DATE_MSG, \
                                                 ERR_METHOD, ERR_METHOD_MSG, \
                                                 FAIL, FAIL_MSG, \
                                                 SUCCEED

# from student.bussiness_logic.err_code_msg import ERROR_CHANGE_PWD
# from student.bussiness_logic.err_code_msg import ERROR_CHANGE_PWD_MSG
# from student.bussiness_logic.err_code_msg import ERROR_GET_STU_DOESNOTEXIST
# from student.bussiness_logic.err_code_msg import ERROR_GET_STU_DOESNOTEXIST_MSG
# from student.bussiness_logic.err_code_msg import ERROR_GET_STU_IDMISS
# from student.bussiness_logic.err_code_msg import ERROR_GET_STU_IDMISS_MSG
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

# from student.bussiness_logic.tag import ERR_AVATAR_FILE_INVALID
# from student.bussiness_logic.tag import ERR_AVATAR_SAVE_FAILED
# from student.bussiness_logic.tag import GOOD_UPDATE_INFO

from student.bussiness_logic.tag import ERR_ACTIVATE_DB
from student.bussiness_logic.tag import ERR_ACTIVATE_NOTEXIST
from student.bussiness_logic.tag import ERR_CHANGE_PWD_NOTEXIST
from student.bussiness_logic.tag import ERR_CHANGE_PWD_WRONG_CREDENTIAL
from student.bussiness_logic.tag import ERR_LOGIN_NOTEXIST
from student.bussiness_logic.tag import ERR_LOGIN_NONACTIVATED
from student.bussiness_logic.tag import ERR_LOGIN_WRONG_PWD
from student.bussiness_logic.tag import ERR_RESET_DB
from student.bussiness_logic.tag import ERR_RESET_NOTEXIST
from student.bussiness_logic.tag import ERR_RESET_OUT_DATE
from student.bussiness_logic.tag import ERR_RESET_MAIL_NOTEXIST
from student.bussiness_logic.tag import OK_LOGIN
from student.bussiness_logic.tag import OK_REG
from student.bussiness_logic.tag import REG_FAIL_DB
from student.bussiness_logic.tag import OK_CHANGE_PWD
from student.bussiness_logic.tag import OK_RESET_MAIL
from student.bussiness_logic.tag import ERR_GET_INFO_DB
from student.bussiness_logic.tag import ERR_GET_INFO_NOTEXIST
from student.bussiness_logic.tag import OK_SAVE_AVATAR
from student.bussiness_logic.tag import ERR_SAVE_AVATAR_FAIL
from student.bussiness_logic.tag import ERR_AVATAR_FILE_INVALID
from student.bussiness_logic.tag import OK_UPDATE_STU_INFO
from student.bussiness_logic.tag import ERR_UPDATE_STU_INFO_DB




# from student.utility.tag import NO_INPUT
from student.utility import json_helper


def post(request):
    """  test  """
    return render(request, 'post.html')


@csrf_exempt
def register(request):
    if request.method == "POST":
        # 如果验证码错误
        # if request.session['code'] != request.POST.get('code'):
        if False:
            return HttpResponse(json_helper.dumps(
                {'err': ERR_VALID_CODE,
                 'msg': ERR_VALID_CODE_MSG}
            ))

        # 如果验证码正确
        acnt = request.POST.get('account')
        pwd = request.POST.get('pwd')

        tag = account.register(acnt=acnt, pwd=pwd)
        # 如果注册成功
        if tag == OK_REG:
           return HttpResponse(json_helper.dumps({"err": SUCCEED}))
        # 如果数据库异常导致注册失败
        elif tag == REG_FAIL_DB:
           return HttpResponse(json_helper.dumps({
                'err': FAIL,
                'msg': FAIL_MSG
            }))
        # 如果账号已存在
        else:
            return HttpResponse(json_helper.dumps({
                'err': ERR_REG_IDEXIST,
                'msg': ERR_REG_IDEXIST_MSG
            }))

    # 如果请求的方法是GET
    return HttpResponse(json_helper.dumps({
        'err': ERR_METHOD,
        'msg': ERR_METHOD_MSG
    }))


@csrf_exempt
def activate(request, cipher):
    # TODO(hjf): 修改返回，改为页面跳转
    """
    账号激活
    请求方法：GET
    @cipher: 由后端加密后的stu_id, 只能通过邮件获得
    成功：返回 {err：SUCCEED}
    失败：返回相应err和msg的JSON
    """
    if request.method == 'GET':
        tag = account.activate(account_cipher=cipher)
        # 如果账号不存在
        if tag == ERR_ACTIVATE_NOTEXIST:
            return HttpResponse(json_helper.dumps({
                'err': ERR_ACCOUNT_NOTEXIST,
                'msg': ERR_ACCOUNT_NOTEXIST_MSG
        }))

        # 如果数据库异常导致激活失败
        elif tag == ERR_ACTIVATE_DB:
            return HttpResponse(json_helper.dumps({
                'err': FAIL,
                'msg': FAIL_MSG
            }))

        # 如果激活成功
        return HttpResponse(json_helper.dumps({'err': SUCCEED}))

    # 如果请求的方法是POST
    else:
        return HttpResponse(json_helper.dumps({
            'err': ERR_METHOD,
            'msg': ERR_METHOD_MSG
        }))


@csrf_exempt
def login(request):
    """
    登陆
    成功：返回 {'err': SUCCEED, 'id': stu_id}
    失败：返回相应的err和msg的JSON
    """
    if request.method == 'POST':
        acnt = request.POST.get('account')
        pwd = request.POST.get('pwd')

        login_rlt = account.login(acnt=acnt, pwd=pwd)
        # 如果登陆成功
        if login_rlt['tag'] == OK_LOGIN:
            json_ctx = {'err': SUCCEED,
                        'id': login_rlt['stu_id']}

        # 如果密码错误
        elif login_rlt['tag'] == ERR_LOGIN_WRONG_PWD:
            json_ctx = {'err': ERR_LOGIN_STU_WRONG_PWD,
                        'msg': ERR_LOGIN_STU_WRONG_PWD_MSG}
        # 如果账号未激活
        elif login_rlt['tag'] == ERR_LOGIN_NONACTIVATED:
            json_ctx = {'err': ERR_LOGIN_STU_NONACTIVATED,
                        'msg': ERR_LOGIN_STU_NONACTIVATED_MSG}
        # 如果账号不存在
        elif login_rlt['tag'] == ERR_LOGIN_NOTEXIST:
            json_ctx = {'err': ERR_ACCOUNT_NOTEXIST,
                        'msg': ERR_ACCOUNT_NOTEXIST_MSG}

        # 如果数据库异常导致登陆失败（tag == ERR_LOGIN_DB)
        else:
            json_ctx = {'err': FAIL,
                        'msg': FAIL_MSG}
        return HttpResponse(json_helper.dumps(json_ctx))

    # 如果请求的方法是GET
    else:
        return HttpResponse(json_helper.dumps({
            'err': ERR_METHOD,
            'msg': ERR_METHOD_MSG
        }))


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

        if tag == OK_RESET_MAIL:
            return HttpResponse(json_helper.dumps({'err': SUCCEED}))
        # 如果账号不存在
        elif tag == ERR_RESET_MAIL_NOTEXIST:
            return HttpResponse(json_helper.dumps({
                'err': ERR_ACCOUNT_NOTEXIST,
                'msg': ERR_ACCOUNT_NOTEXIST_MSG
            }))
        # 如果数据库异常导致无法发送重置邮件(tag == ERR_RESET_MAIL_DB)
        else:
            HttpResponse(json_helper.dumps({
                'err': FAIL,
                'msg': FAIL_MSG
            }))

    # 如果请求的方法是GET
    else:
        return HttpResponse(json_helper.dumps({
            'err': ERR_METHOD, 'msg': ERR_METHOD_MSG
        }))


def reset_page(request, cipher):
    """
    渲染前端重置密码的页面
    method: GET
    成功：返回渲染页面
    失败：返回相应的err和msg的JSON
    """
    if request.method == 'GET':
        return render(request, '', {'cipher': cipher})  # TODO(hjf): 修改template
    # 如果请求的方法是POST
    else:
        return HttpResponse(json_helper.dumps({
            'err': ERR_METHOD, 'msg': ERR_METHOD_MSG
        }))


@csrf_exempt
def reset(request):
    """
    重置密码，修改账号状态为未激活
    成功：返回{'err': SUCCEED, 'credential': credential, 'account': acnt}
                              credential: 用户修改密码的凭据; account: 未加密的账号
    失败：返回相应的err和msg
    """
    if request.method == 'POST':
        account_cipher = request.POST.get('account')  # account_cipher: 由后端加密后的account，只能通过邮件获得

        obj = account.reset(account_cipher)
        # 如果账号不存在
        if obj == ERR_RESET_NOTEXIST:
            return HttpResponse(json_helper.dumps({
                'err': ERR_ACCOUNT_NOTEXIST,
                'msg': ERR_ACCOUNT_NOTEXIST_MSG
            }))

        # 如果请求已过期
        elif obj == ERR_RESET_OUT_DATE:
            return HttpResponse(json_helper.dumps({
                'err': ERR_OUT_DATE,
                'msg': ERR_OUT_DATE_MSG
            }))

        # 如果数据库异常导致无法重置密码
        elif obj == ERR_RESET_DB:
            return HttpResponse(json_helper.dumps({
                'err': FAIL,
                'msg': FAIL_MSG
            }))

        # 如果账号存在，obj是{'credential': credential, 'account': account}
        else:
            credential = obj['credential']
            acnt = obj['account']
            return HttpResponse(json_helper.dumps({
                'err': SUCCEED,
                'credential': credential,
                'account': acnt
            }))

    # 如果请求的方法是GET
    else:
        return HttpResponse(json_helper.dumps(
            {'err': ERR_METHOD, 'msg': ERR_METHOD_MSG}
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
        if tag == OK_CHANGE_PWD:
            return HttpResponse(json_helper.dumps({'err': SUCCEED}))
        # 如果账号不存在
        elif tag == ERR_CHANGE_PWD_NOTEXIST:
            return HttpResponse(json_helper.dumps({
                'err': ERR_ACCOUNT_NOTEXIST,
                'msg': ERR_ACCOUNT_NOTEXIST_MSG
            }))
        # 如果凭据错误
        elif tag == ERR_CHANGE_PWD_WRONG_CREDENTIAL:
            return HttpResponse(json_helper.dumps({
                'err': ERR_WRONG_CREDENTIAL,
                'msg': ERR_WRONG_CREDENTIAL_MSG
            }))
        # 如果数据库异常导致无法修改密码(tag == ERR_CHANGE_PWD_DB)
        else:
            return HttpResponse(json_helper.dumps({
                'err': FAIL,
                'msg': FAIL_MSG
            }))

    # 如果请求的方法是GET
    else:
        return HttpResponse(json_helper.dumps(
            {'err': ERR_METHOD, 'msg': ERR_METHOD_MSG}
        ))


@csrf_exempt
def get_info(request):
    """
    获取学生信息
    成功： 返回err: SUCCEED，头像路径，姓名，学校，学历，年级，专业，所在地，联系方式（tel），邮箱
    失败：返回相应的err和msg的JSON
    """
    if request.method == 'POST':
        stu_id = request.POST.get('id')
        obj = info.get(stu_id=stu_id)

        # 如果学生不存在
        if obj == ERR_GET_INFO_NOTEXIST:
            return HttpResponse(json_helper.dumps({
                'err': ERR_STU_NOTEXIST,
                'msg': ERR_STU_NOTEXIST_MSG
            }))

        # 如果数据库异常导致无法获取学生信息
        elif obj == ERR_GET_INFO_DB:
            return HttpResponse(json_helper.dumps({
                'err': FAIL,
                'msg': FAIL_MSG
            }))

        # 如果获取学生信息成功, 返回前端请求的信息
        else:
            return HttpResponse(json_helper.dumps({
                'err': SUCCEED,
                'avatar_path': obj.avatar_path,
                'name': obj.name,
                'school': obj.school,
                'edu_background': obj.edu_background,
                'grade': obj.grade,
                'major': obj.major,
                'location': obj.location,
                'tel': obj.tel,
                'mail': obj.mail
            }))

    # 如果请求的方法是GET
    else:
        return HttpResponse(json_helper.dumps({
            'err': ERR_METHOD,
            'msg': ERR_METHOD_MSG
        }))


@csrf_exempt
def save_avatar(request):
    """
    保存上传的头像文件，和更新学生的头像
    成功：返回err:SUCCEED, 头像路径
    失败：返回相应的err和msg的JSON
    """
    if request.method == 'POST':
        stu_id = request.POST.get('id')
        stu_avatar = request.FILES.get('avatar')

        save_rlt = avatar.save(stu_id=stu_id, avatar=stu_avatar)
        # 如果保存头像成功
        if save_rlt['tag'] == OK_SAVE_AVATAR:
            return HttpResponse(json_helper.dumps({
                'err': SUCCEED,
                'path': save_rlt['path']
            }))

        # 如果头像不合法
        elif save_rlt['tag'] == ERR_AVATAR_FILE_INVALID:
            return HttpResponse(json_helper.dumps({
                'err': AVATAR_INVALID,
                'msg': AVATAR_INVALID_MSG
            }))

        # 如果保存失败 tag == ERR_SAVE_AVATAR_FAIL
        else:
            return HttpResponse(json_helper.dumps({
                'err': FAIL,
                'msg': FAIL_MSG
            }))

    # 如果请求的方法是GET
    else:
        return HttpResponse(json_helper.dumps({
                'err': ERR_METHOD,
                'msg': ERR_METHOD_MSG
            }))


@csrf_exempt
def update_info(request):
    """
    修改学生信息
    成功：返回{'err': SUCCEED}
    失败：返回相应的err和msg的JSON
    """
    if request.method == 'POST':
        stu_id = request.POST.get('id')
        avatar_path = request.POST.get('path')
        name = request.POST.get('name')
        school = request.POST.get('school')
        major = request.POST.get('major')
        location = request.POST.get('location')
        edu_background = request.POST.get('edu_background')
        grade = request.POST.get('grade')
        mail = request.POST.get('mail')
        tel = request.POST.get('tel')

        tag = info.update(stu_id=stu_id, avatar_path=avatar_path, name=name, school=school,
                          major=major, location=location, edu_background=edu_background,
                          grade=grade, mail=mail, tel=tel)

        # 如果更新成功
        if tag == OK_UPDATE_STU_INFO:
            return HttpResponse(json_helper.dumps({'err': SUCCEED}))

        # 如果数据库原因（丢失记录或异常）导致更新失败 tag == ERR_UPDATE_STU_INFO_DB
        else:
            return HttpResponse(json_helper.dumps({
                'err': FAIL,
                'msg': FAIL_MSG
            }))

    # 如果请求的方法是GET
    else:
        return HttpResponse(json_helper.dumps({
            'err': ERR_METHOD,
            'msg': ERR_METHOD_MSG
        }))


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
















