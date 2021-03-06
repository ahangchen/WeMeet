# coding=utf8
from django.http import HttpResponse
from django.shortcuts import render  # for test method
from django.views.decorators.csrf import csrf_exempt

from student.ctrl import info
from student.ctrl import account
from student.ctrl import avatar
from student.ctrl import resume
from student.ctrl import apply
from student.ctrl import about_me
from student.ctrl import works
from student.ctrl import square
from student.ctrl import skill
from student.ctrl.err_code_msg import ERR_LOGIN_STU_NONACTIVATED, ERR_LOGIN_STU_NONACTIVATED_MSG, \
                                      ERR_LOGIN_STU_WRONG_PWD, ERR_LOGIN_STU_WRONG_PWD_MSG, \
                                      ERR_ACCOUNT_NOTEXIST, ERR_ACCOUNT_NOTEXIST_MSG, \
                                      ERR_WRONG_CREDENTIAL, ERR_WRONG_CREDENTIAL_MSG, \
                                      ERR_STU_NOTEXIST, ERR_STU_NOTEXIST_MSG, \
                                      ERR_REG_IDEXIST, ERR_REG_IDEXIST_MSG, \
                                      ERR_MULTI_APPLY, ERR_MULTI_APPLY_MSG, \
                                      ERR_INTERN_FULL, ERR_INTERN_FULL_MSG, \
                                      ERR_VALID_CODE, ERR_VALID_CODE_MSG, \
                                      RESUME_INVALID, RESUME_INVALID_MSG, \
                                      AVATAR_INVALID, AVATAR_INVALID_MSG, \
                                      ERR_SKILL_FULL, ERR_SKILL_FULL_MSG, \
                                      ERR_PROJ_FULL, ERR_PROJ_FULL_MSG, \
                                      WORKS_INVALID, WORKS_INVALID_MSG, \
                                      ERR_EDU_FULL, ERR_EDU_FULL_MSG, \
                                      ERR_OUT_DATE, ERR_OUT_DATE_MSG, \
                                      WORKS_FULL, WORKS_FULL_MSG, \
                                      ERR_METHOD, ERR_METHOD_MSG, \
                                      NO_INTERN, NO_INTERN_MSG, \
                                      NO_RESUME, NO_RESUME_MSG, \
                                      NO_WORKS, NO_WORKS_MSG, \
                                      NO_APPLY, NO_APPLY_MSG, \
                                      NO_SKILL, NO_SKILL_MSG, \
                                      NO_PROJ, NO_PROJ_MSG, \
                                      NO_EDU, NO_EDU_MSG, \
                                      FAIL, FAIL_MSG, \
                                      OK_DEL_LAST, \
                                      SUCCEED


from student.ctrl.tag import ERR_ACTIVATE_DB
from student.ctrl.tag import ERR_ACTIVATE_NOTEXIST
from student.ctrl.tag import ERR_CHANGE_PWD_NOTEXIST
from student.ctrl.tag import ERR_CHANGE_PWD_WRONG_CREDENTIAL
from student.ctrl.tag import ERR_LOGIN_NOTEXIST
from student.ctrl.tag import ERR_LOGIN_NONACTIVATED
from student.ctrl.tag import ERR_LOGIN_WRONG_PWD
from student.ctrl.tag import ERR_RESET_DB
from student.ctrl.tag import ERR_RESET_NOTEXIST
from student.ctrl.tag import ERR_RESET_OUT_DATE
from student.ctrl.tag import ERR_RESET_MAIL_NOTEXIST
from student.ctrl.tag import OK_LOGIN
from student.ctrl.tag import OK_REG
from student.ctrl.tag import REG_FAIL_DB
from student.ctrl.tag import OK_CHANGE_PWD
from student.ctrl.tag import OK_RESET_MAIL
from student.ctrl.tag import OK_GET_INFO
from student.ctrl.tag import ERR_GET_INFO_DB
from student.ctrl.tag import ERR_GET_INFO_NOTEXIST
from student.ctrl.tag import OK_SAVE_AVATAR
from student.ctrl.tag import ERR_SAVE_AVATAR_FAIL
from student.ctrl.tag import ERR_AVATAR_FILE_INVALID
from student.ctrl.tag import OK_UPDATE_STU_INFO
from student.ctrl.tag import ERR_UPDATE_STU_INFO_DB
from student.ctrl.tag import OK_SAVE_RESUME
from student.ctrl.tag import ERR_RESUME_FILE_INVALID
from student.ctrl.tag import ERR_SAVE_RESUME_FAIL
from student.ctrl.tag import OK_APPLY
from student.ctrl.tag import ERR_APPLY_NO_RESUME
from student.ctrl.tag import ERR_APPLY_EXIST
from student.ctrl.tag import OK_ADD_EDU
from student.ctrl.tag import ERR_ADD_EDU_FULL
from student.ctrl.tag import ERR_ADD_EDU_DB
from student.ctrl.tag import OK_GET_EDU
from student.ctrl.tag import ERR_GET_NO_EDU
from student.ctrl.tag import ERR_GET_EDU_DB
from student.ctrl.tag import OK_GET_INTERN
from student.ctrl.tag import ERR_GET_NO_INTERN
from student.ctrl.tag import ERR_GET_INTERN_DB
from student.ctrl.tag import OK_GET_PROJ
from student.ctrl.tag import ERR_GET_NO_PROJ
from student.ctrl.tag import ERR_GET_PROJ_DB
from student.ctrl.tag import OK_GET_WORKS
from student.ctrl.tag import ERR_GET_NO_WORKS
from student.ctrl.tag import ERR_GET_WORKS_DB
from student.ctrl.tag import OK_GET_SKILL
from student.ctrl.tag import ERR_GET_NO_SKILL
from student.ctrl.tag import ERR_GET_SKILL_DB
from student.ctrl.tag import OK_UPDATE_EDU
from student.ctrl.tag import OK_DEL_EDU
from student.ctrl.tag import OK_DEL_LAST_EDU
from student.ctrl.tag import OK_ADD_INTERN
from student.ctrl.tag import ERR_ADD_INTERN_FULL
from student.ctrl.tag import ERR_ADD_INTERN_DB
from student.ctrl.tag import OK_UPDATE_INTERN
from student.ctrl.tag import ERR_UPDATE_INTERN_DB
from student.ctrl.tag import OK_DEL_INTERN
from student.ctrl.tag import ERR_DEL_INTERN_DB
from student.ctrl.tag import OK_ADD_PROJ
from student.ctrl.tag import ERR_ADD_PROJ_FULL
from student.ctrl.tag import ERR_ADD_PROJ_DB
from student.ctrl.tag import OK_UPDATE_PROJ
from student.ctrl.tag import ERR_UPDATE_PROJ_DB
from student.ctrl.tag import OK_DEL_PROJ
from student.ctrl.tag import ERR_DEL_PROJ_DB
from student.ctrl.tag import OK_ADD_SKILL
from student.ctrl.tag import ERR_ADD_SKILL_FULL
from student.ctrl.tag import ERR_ADD_SKILL_DB
from student.ctrl.tag import OK_UPDATE_SKILL
from student.ctrl.tag import ERR_UPDATE_SKILL_DB
from student.ctrl.tag import OK_DEL_SKILL
from student.ctrl.tag import ERR_DEL_SKILL_DB
from student.ctrl.tag import OK_SAVE_WORKS
from student.ctrl.tag import ERR_SAVE_WORKS_FAIL
from student.ctrl.tag import ERR_WORKS_FILE_INVALID
from student.ctrl.tag import OK_UPDATE_WORKS
from student.ctrl.tag import ERR_UPDATE_WORKS_DB
from student.ctrl.tag import OK_DEL_WORKS
from student.ctrl.tag import ERR_DEL_WORKS_DB
from student.ctrl.tag import OK_GET_RESUME
from student.ctrl.tag import ERR_GET_NO_RESUME
from student.ctrl.tag import ERR_GET_RESUME_DB
from student.ctrl.tag import OK_GET_APPLY
from student.ctrl.tag import ERR_GET_NO_APPLY
from student.ctrl.tag import ERR_GET_APPLY_DB
from student.ctrl.tag import OK_READ_APPLY
from student.ctrl.tag import ERR_READ_APPLY_DB
from student.ctrl.tag import OK_APPLY_INFO
from student.ctrl.tag import ERR_APPLY_INFO_DB
from student.ctrl.tag import OK_REPLY
from student.ctrl.tag import ERR_REPLY_DB
from student.ctrl.tag import OK_HANDLE
from student.ctrl.tag import ERR_STATE
from student.ctrl.tag import ERR_HANDLE_DB
from student.ctrl.tag import OK_DEL_RESUME



# from student.util.tag import NO_INPUT
from student.util import json_helper
from team.util.request import is_valid_ok
from team.util.request import resp_valid_err


def post(request):
    """  test  """
    return render(request, 'post.html')


@csrf_exempt
def register(request):
    if request.method == "POST":
        # 如果验证码错误
        if not is_valid_ok(request):
            return resp_valid_err()

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
        # return HttpResponse(json_helper.dumps({'err': SUCCEED}))
        return render(request, 'stu/act_succ.html')
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


def fetch(request):
    """
    渲染前端重置密码的页面
    method: GET
    成功：返回渲染页面
    失败：返回相应的err和msg的JSON
    """
    return render(request, 'stu/fetch.html', {'hash_tid': request.GET['reset_key'], 'mail': request.GET['mail']})


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
    成功： 返回err: SUCCEED，头像路径，姓名，头衔, 学校, 性别, 年级，一级标签，人气值
    失败：返回相应的err和msg的JSON
    """
    if request.method == 'POST':
        stu_id = request.POST.get('id')
        get_rlt = info.get(stu_id=stu_id)

        # 如果获取学生信息成功, 返回前端请求的信息
        if get_rlt['tag'] == OK_GET_INFO:
            return HttpResponse(json_helper.dumps({
                'err': SUCCEED,
                'avatar_path': get_rlt['stu'].avatar_path,
                'name': get_rlt['stu'].name,
                'title': get_rlt['stu'].title,
                'personal_signature': get_rlt['stu'].personal_signature,
                'sex': get_rlt['stu'].sex,
                'school': get_rlt['stu'].school,
                'grade': get_rlt['stu'].grade,
                # 'label': get_rlt['stu'].label,
                'is_engineering': int(get_rlt['stu'].is_engineering),
                'is_literature': int(get_rlt['stu'].is_literature),
                'is_management': int(get_rlt['stu'].is_management),
                'is_humanity': int(get_rlt['stu'].is_humanity),
                'likes': get_rlt['stu'].likes
            }))

        # 如果学生不存在
        elif get_rlt['tag'] == ERR_GET_INFO_NOTEXIST:
            return HttpResponse(json_helper.dumps({
                'err': ERR_STU_NOTEXIST,
                'msg': ERR_STU_NOTEXIST_MSG
            }))

        # 如果数据库异常导致无法获取学生信息(get_rlt['tag'] == ERR_GET_INFO_DB)
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
        stu_id = request.POST.get('stu_id')
        name = request.POST.get('name')
        title = request.POST.get('title')
        personal_signature = request.POST.get('personal_signature')
        sex = request.POST.get('sex')
        school = request.POST.get('school')
        grade = request.POST.get('grade')
        avatar_path = request.POST.get('avatar_path')
        is_engineering = request.POST.get('is_engineering')
        is_literature = request.POST.get('is_literature')
        is_management = request.POST.get('is_management')
        is_humanity = request.POST.get('is_humanity')

        tag = info.update(stu_id=stu_id, name=name, title=title, personal_signature=personal_signature,
                          sex=sex, school=school, grade=grade, avatar_path=avatar_path,
                          is_engineering=is_engineering, is_literature=is_literature,
                          is_management=is_management, is_humanity=is_humanity)

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


@csrf_exempt
def upload_resume(request):
    """
    保存上传的简历文件
    成功：返回err:SUCCEED, 简历路径
    失败：返回相应的err和msg的JSON
    """
    if request.method == 'POST':
        stu_id = request.POST.get('id')
        resume_file = request.FILES.get('resume')

        upload_rlt = resume.upload(stu_id=stu_id, resume=resume_file)
        # 如果保存上传的简历文件成功
        if upload_rlt['tag'] == OK_SAVE_RESUME:
            return HttpResponse(json_helper.dumps({
                'err': SUCCEED,
                'path': upload_rlt['path']
            }))

        # 如果简历文件不合法
        elif upload_rlt['tag'] == ERR_RESUME_FILE_INVALID:
            return HttpResponse(json_helper.dumps({
                'err': RESUME_INVALID,
                'msg': RESUME_INVALID_MSG
            }))

        # 如果保存失败 tag == ERR_SAVE_RESUME_FAIL
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
def get_resume(request):
    """
    获取学生的简历路径
    成功:返回{
                'err': SUCCEED,
                'resume_path': get_rlt['resume_path'],
            }
    失败：返回相应的err和msg的JSON
    """
    if request.method == 'POST':
        stu_id = request.POST.get('stu_id')
        print(stu_id)
        get_rlt = resume.get(stu_id)

        # 如果获取成功
        if get_rlt['tag'] == OK_GET_RESUME:
            return HttpResponse(json_helper.dumps({
                'err': SUCCEED,
                'resume_path': get_rlt['resume_path'],
            }))

        # 如果该学生没有简历
        elif get_rlt['tag'] == ERR_GET_NO_RESUME:
            return HttpResponse(json_helper.dumps({
                'err': NO_RESUME,
                'msg': NO_RESUME_MSG
            }))

        # get_rlt['tag'] == ERR_GET_RESUME_DB
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
def del_resume(request):
    """
    删除简历
    成功：返回{'err': SUCCEED}
    失败：返回相应的err和msg的JSON
    """
    if request.method == 'POST':
        stu_id = request.POST.get('stu_id')
        del_rlt = resume.delete(stu_id)

        if del_rlt['tag'] == OK_DEL_RESUME:
            return HttpResponse(json_helper.dumps({'err': SUCCEED}))
        else:
            return HttpResponse(json_helper.dumps({
                'err' : FAIL,
                'msg' : FAIL_MSG
            }))

    # 如果请求的方法是GET
    else:
        return HttpResponse(json_helper.dumps({
            'err': ERR_METHOD,
            'msg': ERR_METHOD_MSG
        }))


@csrf_exempt
def job_apply(request):
    """
    投递简历
    成功：返回err:SUCCEED, 投递记录的id
    失败：返回相应的err和msg的JSON
    """
    if request.method == 'POST':
        stu_id = request.POST.get('stu_id')
        job_id = request.POST.get('job_id')

        apply_rlt = resume.apply(stu_id, job_id)
        # 如果投递简历成功
        if apply_rlt['tag'] == OK_APPLY:
            return HttpResponse(json_helper.dumps({
                'err': SUCCEED,
                'apply_id': apply_rlt['apply_id']
            }))
        # 如果学生无简历
        elif apply_rlt['tag'] == ERR_APPLY_NO_RESUME:
            return HttpResponse(json_helper.dumps({
                'err': NO_RESUME,
                'msg': NO_RESUME_MSG
            }))
        # 如果已经投递过同一职位
        elif apply_rlt['tag'] == ERR_APPLY_EXIST:
            return HttpResponse(json_helper.dumps({
                'err': ERR_MULTI_APPLY,
                'msg': ERR_MULTI_APPLY_MSG
            }))
        # 如果投递简历失败 apply_rlt['tag'] == ERR_APPLY_DB:
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
# def add_edu(request):
#     """
#     增加教育经历
#     成功：返回：{
#                 'err': SUCCEED,
#                 'edu_id': add_rlt['edu_id'],
#                 'grade': add_rlt['grade'],
#                 'edu_background': add_rlt['edu_background']
#             }
#     失败：返回相应的err和msg的JSON
#     """
#     if request.method == 'POST':
#         stu_id = request.POST.get('stu_id')
#         major = request.POST.get('major')
#         graduation_year = request.POST.get('graduation_year')
#         background = request.POST.get('edu_background')
#         school = request.POST.get('school')
#
#         add_rlt = info.add_edu(stu_id, major, graduation_year, background, school)
#         # 如果增加教育经历成功
#         if add_rlt['tag'] == OK_ADD_EDU:
#             return HttpResponse(json_helper.dumps({
#                 'err': SUCCEED,
#                 'edu_id': add_rlt['edu_id'],
#                 'grade': add_rlt['grade'],
#                 'edu_background': add_rlt['edu_background']
#             }))
#
#         # 如果教育经历已达上限
#         elif add_rlt['tag'] == ERR_ADD_EDU_FULL:
#             return HttpResponse(json_helper.dumps({
#                 'err': ERR_EDU_FULL,
#                 'msg': ERR_EDU_FULL_MSG
#             }))
#
#         # 如果数据库异常导致增加教育经历失败(add_rlt['tag'] == ERR_ADD_EDU_DB)
#         else:
#             return HttpResponse(json_helper.dumps({
#                 'err': FAIL,
#                 'msg': FAIL_MSG
#             }))
#
#     # 如果请求的方法是GET
#     else:
#         return HttpResponse(json_helper.dumps({
#             'err': ERR_METHOD,
#             'msg': ERR_METHOD_MSG
#         }))
#
#
# @csrf_exempt
# def get_edu(request):
#     """
#     获取学生的教育经历
#     成功：返回{
#                 'err': SUCCEED,
#                 'grade': get_rlt['grade'],
#                 'major': get_rlt['major'],
#                 'edu_list': get_rlt['edu_list']
#             }
#             get_rlt['edu_list']: [{'edu_id': edu_rcd.id,
#                                   'major': edu_rcd.major,
#                                   'graduation_year': edu_rcd.graduation_year,
#                                   'edu_background': edu_rcd.background,
#                                   'school': edu_rcd.school}]
#     失败：返回相应的err和msg的JSON
#     """
#     if request.method == 'POST':
#         stu_id = request.POST.get('stu_id')
#         get_rlt = info.get_edu(stu_id)
#
#         # 如果获取成功
#         if get_rlt['tag'] == OK_GET_EDU:
#             return HttpResponse(json_helper.dumps({
#                 'err': SUCCEED,
#                 'grade': get_rlt['grade'],
#                 'edu_background': get_rlt['edu_background'],
#                 'edu_list': get_rlt['edu_list']
#             }))
#
#         # 如果该学生没有教育经历
#         elif get_rlt['tag'] == ERR_GET_NO_EDU:
#             return HttpResponse(json_helper.dumps({
#                 'err': NO_EDU,
#                 'msg': NO_EDU_MSG
#             }))
#
#         # get_rlt['tag'] == ERR_GET_EDU_DB
#         else:
#             return HttpResponse(json_helper.dumps({
#                 'err': FAIL,
#                 'msg': FAIL_MSG
#             }))
#
#     # 如果请求的方法是GET
#     else:
#         return HttpResponse(json_helper.dumps({
#             'err': ERR_METHOD,
#             'msg': ERR_METHOD_MSG
#         }))
#
#
# @csrf_exempt
# def update_edu(request):
#     """
#     更新教育经历
#     成功：返回{
#                 'err': SUCCEED,
#                 'edu_id': update_rlt['edu_id'],
#                 'grade': update_rlt['grade'],
#                 'edu_background': update_rlt['edu_background']
#             }
#     失败：返回相应的err和msg的JSON
#     """
#     if request.method == 'POST':
#         stu_id = request.POST.get('stu_id')
#         edu_id = request.POST.get('edu_id')
#         major = request.POST.get('major')
#         graduation_year = request.POST.get('graduation_year')
#         background = request.POST.get('edu_background')
#         school = request.POST.get('school')
#
#         update_rlt = info.update_edu(stu_id, edu_id, major, graduation_year, background, school)
#         # 如果更新教育经历成功
#         if update_rlt['tag'] == OK_UPDATE_EDU:
#             return HttpResponse(json_helper.dumps({
#                 'err': SUCCEED,
#                 'grade': update_rlt['grade'],
#                 'edu_background': update_rlt['edu_background']
#             }))
#
#         # 如果数据库异常导致更新教育经历失败(add_rlt['tag'] == ERR_UPDATE_EDU_DB)
#         else:
#             return HttpResponse(json_helper.dumps({
#                 'err': FAIL,
#                 'msg': FAIL_MSG
#             }))
#
#     # 如果请求的方法是GET
#     else:
#         return HttpResponse(json_helper.dumps({
#             'err': ERR_METHOD,
#             'msg': ERR_METHOD_MSG
#         }))
#
#
# @csrf_exempt
# def del_edu(request):
#     """
#     删除教育经历
#     成功:返回{
#                 'err': SUCCEED,
#                 'grade': del_rlt['grade'],
#                 'edu_background': del_rlt['edu_background']
#             }
#     失败：返回相应的err和msg的JSON
#     """
#     if request.method == 'POST':
#         stu_id = request.POST.get('stu_id')
#         edu_id = request.POST.get('edu_id')
#
#         del_rlt = info.del_edu(stu_id=stu_id, edu_id=edu_id)
#         # 如果删除成功
#         if del_rlt['tag'] == OK_DEL_EDU:
#             return HttpResponse(json_helper.dumps({
#                 'err': SUCCEED,
#                 'grade': del_rlt['grade'],
#                 'edu_background': del_rlt['edu_background']
#             }))
#
#         # 如果删除了最后一条教育经历
#         elif del_rlt['tag'] == OK_DEL_LAST_EDU:
#             return HttpResponse(json_helper.dumps({'err': OK_DEL_LAST}))
#
#         # 如果数据库异常导致删除教育经历失败(add_rlt['tag'] == ERR_DEL_EDU_DB)
#         else:
#             return HttpResponse(json_helper.dumps({
#                 'err': FAIL,
#                 'msg': FAIL_MSG
#             }))
#
#     # 如果请求的方法是GET
#     else:
#         return HttpResponse(json_helper.dumps({
#             'err': ERR_METHOD,
#             'msg': ERR_METHOD_MSG
#         }))
#
#
# @csrf_exempt
# def add_intern(request):
#     """
#     增加实习经历
#     成功：返回{
#                 'err': SUCCEED,
#                 'intern_id': add_rlt['intern_id']
#             }
#     失败：返回相应的err和msg的JSON
#     """
#     if request.method == 'POST':
#         stu_id = request.POST.get('stu_id')
#         company = request.POST.get('company')
#         position = request.POST.get('position')
#         begin_time = request.POST.get('begin_time')
#         end_time = request.POST.get('end_time')
#         description = request.POST.get('description')
#
#         add_rlt = info.add_intern(stu_id, company, position, begin_time, end_time, description)
#         # 如果增加实习经历成功
#         if add_rlt['tag'] == OK_ADD_INTERN:
#             return HttpResponse(json_helper.dumps({
#                 'err': SUCCEED,
#                 'intern_id': add_rlt['intern_id']
#             }))
#
#         # 如果实习经历已达上限
#         elif add_rlt['tag'] == ERR_ADD_INTERN_FULL:
#             return HttpResponse(json_helper.dumps({
#                 'err': ERR_INTERN_FULL,
#                 'msg': ERR_INTERN_FULL_MSG
#             }))
#
#         # 如果数据库异常导致增加实习经历失败(add_rlt['tag'] == ERR_ADD_INTERN_DB)
#         else:
#             return HttpResponse(json_helper.dumps({
#                 'err': FAIL,
#                 'msg': FAIL_MSG
#             }))
#
#     # 如果请求的方法是GET
#     else:
#         return HttpResponse(json_helper.dumps({
#             'err': ERR_METHOD,
#             'msg': ERR_METHOD_MSG
#         }))
#
#
# @csrf_exempt
# def get_intern(request):
#     """
#     获取实习经历
#     成功：返回{'err': SUCCEED, 'intern_list': get_rlt['intern_list']}
#     失败：返回相应的err和msg的JSON
#     """
#     if request.method == 'POST':
#         stu_id = request.POST.get('stu_id')
#         get_rlt = info.get_intern(stu_id)
#
#         # 如果获取成功
#         if get_rlt['tag'] == OK_GET_INTERN:
#             return HttpResponse(json_helper.dumps({
#                 'err': SUCCEED,
#                 'intern_list': get_rlt['intern_list']
#             }))
#
#         # 如果该学生没有实习经历
#         elif get_rlt['tag'] == ERR_GET_NO_INTERN:
#             return HttpResponse(json_helper.dumps({
#                 'err': NO_INTERN,
#                 'msg': NO_INTERN_MSG
#             }))
#
#         # get_rlt['tag'] == ERR_GET_INTERN_DB
#         else:
#             return HttpResponse(json_helper.dumps({
#                 'err': FAIL,
#                 'msg': FAIL_MSG
#             }))
#
#     # 如果请求的方法是GET
#     else:
#         return HttpResponse(json_helper.dumps({
#             'err': ERR_METHOD,
#             'msg': ERR_METHOD_MSG
#         }))
#
#
# @csrf_exempt
# def update_intern(request):
#     """
#     更新实习经历
#     成功：返回
#     失败：返回相应的err和msg的JSON
#     """
#     if request.method == 'POST':
#         stu_id = request.POST.get('stu_id')
#         intern_id = request.POST.get('intern_id')
#         company = request.POST.get('company')
#         position = request.POST.get('position')
#         begin_time = request.POST.get('begin_time')
#         end_time = request.POST.get('end_time')
#         description = request.POST.get('description')
#
#         update_rlt = info.update_intern(intern_id, stu_id, company, position, begin_time, end_time, description)
#         # 如果更新实习经历成功
#         if update_rlt['tag'] == OK_UPDATE_INTERN:
#             return HttpResponse(json_helper.dumps({'err': SUCCEED}))
#
#         # 如果数据库异常导致更新实习经历失败(add_rlt['tag'] == ERR_UPDATE_INTERN_DB)
#         else:
#             return HttpResponse(json_helper.dumps({
#                 'err': FAIL,
#                 'msg': FAIL_MSG
#             }))
#
#     # 如果请求的方法是GET
#     else:
#         return HttpResponse(json_helper.dumps({
#             'err': ERR_METHOD,
#             'msg': ERR_METHOD_MSG
#         }))
#
#
# @csrf_exempt
# def del_intern(request):
#     """
#     删除实习经历
#     成功：返回
#
#     """
#     if request.method == 'POST':
#         stu_id = request.POST.get('stu_id')
#         intern_id = request.POST.get('intern_id')
#
#         del_rlt = info.del_intern(stu_id=stu_id, intern_id=intern_id)
#         # 如果删除成功
#         if del_rlt['tag'] == OK_DEL_INTERN:
#             return HttpResponse(json_helper.dumps({'err': SUCCEED}))
#
#         # 如果数据库异常导致删除实习经历失败(add_rlt['tag'] == ERR_DEL_INTERN_DB)
#         else:
#             return HttpResponse(json_helper.dumps({
#                 'err': FAIL,
#                 'msg': FAIL_MSG
#             }))
#
#     # 如果请求的方法是GET
#     else:
#         return HttpResponse(json_helper.dumps({
#             'err': ERR_METHOD,
#             'msg': ERR_METHOD_MSG
#         }))
#
#
# @csrf_exempt
# def add_proj(request):
#     """
#     增加项目经历
#     成功：返回{
#                 'err': SUCCEED,
#                 'proj_id': add_rlt['proj_id']
#             }
#     失败：返回相应的err和msg的JSON
#     """
#     if request.method == 'POST':
#         stu_id = request.POST.get('stu_id')
#         name = request.POST.get('name')
#         duty = request.POST.get('duty')
#         year = request.POST.get('year')
#         description = request.POST.get('description')
#
#         add_rlt = info.add_proj(stu_id, name, duty, year, description)
#         # 如果增加项目经历成功
#         if add_rlt['tag'] == OK_ADD_PROJ:
#             return HttpResponse(json_helper.dumps({
#                 'err': SUCCEED,
#                 'proj_id': add_rlt['proj_id']
#             }))
#
#         # 如果项目经历已达上限
#         elif add_rlt['tag'] == ERR_ADD_PROJ_FULL:
#             return HttpResponse(json_helper.dumps({
#                 'err': ERR_PROJ_FULL,
#                 'msg': ERR_PROJ_FULL_MSG
#             }))
#
#         # 如果数据库异常导致增加项目经历失败(add_rlt['tag'] == ERR_ADD_PROJ_DB)
#         else:
#             return HttpResponse(json_helper.dumps({
#                 'err': FAIL,
#                 'msg': FAIL_MSG
#             }))
#
#     # 如果请求的方法是GET
#     else:
#         return HttpResponse(json_helper.dumps({
#             'err': ERR_METHOD,
#             'msg': ERR_METHOD_MSG
#         }))
#
#
# @csrf_exempt
# def get_proj(request):
#     """
#     获取项目经历
#     成功：返回{'err': SUCCEED, 'proj_list': get_rlt['proj_list']}
#                             "proj_list": [{
#             　　　　　　                      "proj_id": proj_id,
#             　　　　　　                      "name": name,
#             　　　　　　                      "duty": duty,
#             　　　　　　                      "year": year,
#             　　　　　　                      "description": description},
#             　　　                         ...]}
#     失败：返回相应的err和msg的JSON
#     """
#     if request.method == 'POST':
#         stu_id = request.POST.get('stu_id')
#         get_rlt = info.get_proj(stu_id)
#
#         # 如果获取成功
#         if get_rlt['tag'] == OK_GET_PROJ:
#             return HttpResponse(json_helper.dumps({
#                 'err': SUCCEED,
#                 'proj_list': get_rlt['proj_list']
#             }))
#
#         # 如果该学生没有项目经历
#         elif get_rlt['tag'] == ERR_GET_NO_PROJ:
#             return HttpResponse(json_helper.dumps({
#                 'err': NO_PROJ,
#                 'msg': NO_PROJ_MSG
#             }))
#
#         # get_rlt['tag'] == ERR_GET_PROJ_DB
#         else:
#             return HttpResponse(json_helper.dumps({
#                 'err': FAIL,
#                 'msg': FAIL_MSG
#             }))
#
#     # 如果请求的方法是GET
#     else:
#         return HttpResponse(json_helper.dumps({
#             'err': ERR_METHOD,
#             'msg': ERR_METHOD_MSG
#         }))
#
#
# @csrf_exempt
# def update_proj(request):
#     """
#     更新项目经历
#     成功：返回
#     失败：返回相应的err和msg的JSON
#     """
#     if request.method == 'POST':
#         stu_id = request.POST.get('stu_id')
#         proj_id = request.POST.get('proj_id')
#         name = request.POST.get('name')
#         duty = request.POST.get('duty')
#         year = request.POST.get('year')
#         description = request.POST.get('description')
#
#         update_rlt = info.update_proj(proj_id, stu_id, name, duty, year, description)
#         # 如果更新项目经历成功
#         if update_rlt['tag'] == OK_UPDATE_PROJ:
#             return HttpResponse(json_helper.dumps({'err': SUCCEED}))
#
#         # 如果数据库异常导致更新项目经历失败(add_rlt['tag'] == ERR_UPDATE_PROJ_DB)
#         else:
#             return HttpResponse(json_helper.dumps({
#                 'err': FAIL,
#                 'msg': FAIL_MSG
#             }))
#
#     # 如果请求的方法是GET
#     else:
#         return HttpResponse(json_helper.dumps({
#             'err': ERR_METHOD,
#             'msg': ERR_METHOD_MSG
#         }))
#
#
# @csrf_exempt
# def del_proj(request):
#     """
#     删除项目经历
#     成功：返回{'err': SUCCEED}
#     失败：返回相应的err和msg的JSON
#     """
#     if request.method == 'POST':
#         stu_id = request.POST.get('stu_id')
#         proj_id = request.POST.get('proj_id')
#
#         del_rlt = info.del_proj(stu_id=stu_id, proj_id=proj_id)
#         # 如果删除成功
#         if del_rlt['tag'] == OK_DEL_PROJ:
#             return HttpResponse(json_helper.dumps({'err': SUCCEED}))
#
#         # 如果数据库异常导致删除项目经历失败(add_rlt['tag'] == ERR_DEL_PROJ_DB)
#         else:
#             return HttpResponse(json_helper.dumps({
#                 'err': FAIL,
#                 'msg': FAIL_MSG
#             }))
#
#     # 如果请求的方法是GET
#     else:
#         return HttpResponse(json_helper.dumps({
#             'err': ERR_METHOD,
#             'msg': ERR_METHOD_MSG
#         }))


@csrf_exempt
def upload_works(request):
    """
    保存上传的作品集文件
    成功：返回err:SUCCEED, 作品集路径
    失败：返回相应的err和msg的JSON
    """
    if request.method == 'POST':
        stu_id = request.POST.get('stu_id')
        works_file = request.FILES.get('works')

        upload_rlt = works.upload(stu_id=stu_id, works_file=works_file)
        # 如果保存上传的作品集文件成功
        if upload_rlt['tag'] == OK_SAVE_WORKS:
            return HttpResponse(json_helper.dumps({
                'err': SUCCEED,
                'path': upload_rlt['path']
            }))

        # 如果简历文件不合法
        elif upload_rlt['tag'] == ERR_WORKS_FILE_INVALID:
            return HttpResponse(json_helper.dumps({
                'err': WORKS_INVALID,
                'msg': WORKS_INVALID_MSG
            }))

        # 如果保存失败 tag == ERR_SAVE_WORKS_FAIL
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
def add_skill(request):
    """
    增加技能评价
    成功：返回{
                'err': SUCCEED,
                'skill_id': add_rlt['skill_id']
            }
    失败：返回相应的err和msg的JSON
    """
    if request.method == 'POST':
        stu_id = request.POST.get('stu_id')
        name = request.POST.get('name')
        value = request.POST.get('value')

        add_rlt = skill.add(stu_id, name, value)
        # 如果增加技能评价成功
        if add_rlt['tag'] == OK_ADD_SKILL:
            return HttpResponse(json_helper.dumps({
                'err': SUCCEED,
                'skill_id': add_rlt['skill_id']
            }))

        # 如果数据库异常或数量已满导致增加技能评价失败
        # (add_rlt['tag'] == ERR_ADD_SKILL_DB 或add_rlt['tag'] == ERR_ADD_SKILL_FULL)
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
def get_skill(request):
    """
    获取技能评价
    成功：返回{'err': SUCCEED, 'skill_list': get_rlt['skill_list']}
                            "skill_list": [{
            　　　　　　                      "skill_id": skill_id,
            　　　　　　                      "name": name,
            　　　　　　                      "value": value},
            　　　                         ...]}
    失败：返回相应的err和msg的JSON
    """
    if request.method == 'POST':
        stu_id = request.POST.get('stu_id')
        get_rlt = skill.get(stu_id)

        # 如果获取成功
        if get_rlt['tag'] == OK_GET_SKILL:
            return HttpResponse(json_helper.dumps({
                'err': SUCCEED,
                'skill_list': get_rlt['skill_list']
            }))

        # 如果该学生没有技能评价
        elif get_rlt['tag'] == ERR_GET_NO_SKILL:
            return HttpResponse(json_helper.dumps({
                'err': NO_SKILL,
                'msg': NO_SKILL_MSG
            }))

        # get_rlt['tag'] == ERR_GET_SKILL_DB
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
def update_skill(request):
    """
    更新技能评价
    成功：返回
    失败：返回相应的err和msg的JSON
    """
    if request.method == 'POST':
        stu_id = request.POST.get('stu_id')
        skill_id = request.POST.get('skill_id')
        name = request.POST.get('name')
        value = request.POST.get('value')

        update_rlt = skill.update(skill_id, stu_id, name, value)
        # 如果更新技能评价成功
        if update_rlt['tag'] == OK_UPDATE_SKILL:
            return HttpResponse(json_helper.dumps({'err': SUCCEED}))

        # 如果数据库异常导致更新技能评价失败(add_rlt['tag'] == ERR_UPDATE_SKILL_DB)
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
def del_skill(request):
    """
    删除技能评价
    成功：返回{'err': SUCCEED}
    失败：返回相应的err和msg的JSON
    """
    if request.method == 'POST':
        stu_id = request.POST.get('stu_id')
        skill_id = request.POST.get('skill_id')

        del_rlt = skill.delete(stu_id=stu_id, skill_id=skill_id)
        # 如果删除成功
        if del_rlt['tag'] == OK_DEL_SKILL:
            return HttpResponse(json_helper.dumps({'err': SUCCEED}))

        # 如果数据库异常导致删除技能评价失败(add_rlt['tag'] == ERR_DEL_SKILL_DB)
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
def stu_get_apply(request):
    """
    学生获取投递列表
    成功：返回
    失败：返回相应的err和msg的JSON
    """
    if request.method == 'POST':
        stu_id = request.POST.get('stu_id')
        state = request.POST.get('state')
        print(stu_id)
        print(state)
        get_rlt = apply.stu_get_list(stu_id, state)

        # 如果获取成功
        if get_rlt['tag'] == OK_GET_APPLY:
            return HttpResponse(json_helper.dumps({
                'err': SUCCEED,
                'apply_list': get_rlt['apply_list']
            }))

        # 如果该学生没有投递记录
        elif get_rlt['tag'] == ERR_GET_NO_APPLY:
            return HttpResponse(json_helper.dumps({
                'err': NO_APPLY,
                'msg': NO_APPLY_MSG
            }))

        # get_rlt['tag'] == ERR_GET_APPLY_DB
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
def set_apply_read(request):
    """
    设置投递记录为已读（学生）
    成功：返回
    失败：返回相应的err和msg的JSON
    """
    if request.method == 'POST':
        apply_list = request.POST.getlist('apply_list[]')

        rlt = apply.set_read(apply_list)
        # 如果设置投递记录为已读
        if rlt['tag'] == OK_READ_APPLY:
            return HttpResponse(json_helper.dumps({'err': SUCCEED}))

        # 如果数据库异常导致设置投递记录为已读失败(add_rlt['tag'] == ERR_READ_APPLY_DB)
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
def team_get_apply(request):
    """
    团队获取投递列表
    成功：返回{
                'err': SUCCEED,
                'apply_list': get_rlt['apply_list']
            }
    失败：返回相应的err和msg的JSON
    """
    if request.method == 'POST':
        team_id = request.POST.get('team_id')
        state = request.POST.get('state')
        get_rlt = apply.team_get_list(team_id, state)

        # 如果获取成功
        if get_rlt['tag'] == OK_GET_APPLY:
            return HttpResponse(json_helper.dumps({
                'err': SUCCEED,
                'apply_list': get_rlt['apply_list'],
                'unread_num': get_rlt['unread_num']
            }))

        # 如果该团队没有投递记录
        elif get_rlt['tag'] == ERR_GET_NO_APPLY:
            return HttpResponse(json_helper.dumps({
                'err': NO_APPLY,
                'msg': NO_APPLY_MSG
            }))

        # get_rlt['tag'] == ERR_GET_APPLY_DB
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
def apply_info(request):
    """
    团队获取投递信息
    成功：返回{
                    'err': SUCCEED,
                    'stu_id': get_rlt['stu_id'],
                    'name': get_rlt['name'],
                    'avatar_path': get_rlt['avatar_path'],
                    'sex': get_rlt['sex'],
                    'age': get_rlt['age'],
                    'mail': get_rlt['mail'],
                    'tel': get_rlt['tel'],
                    'school': get_rlt['school'],
                    'major': get_rlt['major'],
                    'location': get_rlt['location'],
                    'resume_path': get_rlt['resume_path'],
                    'state': get_rlt['state']
                    }
    失败：返回相应的err和msg的JSON
    """
    if request.method == 'POST':
        apply_id = request.POST.get('apply_id')
        get_rlt = apply.team_get_info(apply_id)

        # 如果获取成功
        if get_rlt['tag'] == OK_APPLY_INFO:
            return HttpResponse(json_helper.dumps({
                    'err': SUCCEED,
                    'stu_id': get_rlt['stu_id'],
                    'name': get_rlt['name'],
                    'avatar_path': get_rlt['avatar_path'],
                    'sex': get_rlt['sex'],
                    'age': get_rlt['age'],
                    'mail': get_rlt['mail'],
                    'tel': get_rlt['tel'],
                    'school': get_rlt['school'],
                    'major': get_rlt['major'],
                    'location': get_rlt['location'],
                    'resume_path': get_rlt['resume_path'],
                    'state': get_rlt['state']
                    }))

        # get_rlt['tag'] == ERR_APPLY_INFO_DB
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
def apply_reply(request):
    """
    邮件回复投递（团队）
    成功：返回{'err': SUCCEED}
    失败：返回相应的err和msg的JSON
    """
    if request.method == 'POST':
        apply_id = request.POST.get('apply_id')
        text = request.POST.get('text')
        tag = apply.reply(apply_id, text)

        # 如果获取成功
        if tag == OK_REPLY:
            return HttpResponse(json_helper.dumps({'err': SUCCEED}))

        # tag == ERR_REPLY_DB
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
def team_apply_handle(request):
    """
    处理投递（团队）
    成功：返回{'err': SUCCEED}
    失败：返回相应的err和msg的JSON
    """
    if request.method == 'POST':
        apply_id = request.POST.get('apply_id')
        state = request.POST.get('state')
        tag = apply.handle(apply_id, state)

        # 如果处理成功
        if tag == OK_HANDLE:
            return HttpResponse(json_helper.dumps({'err': SUCCEED}))

        # tag == ERR_STATE或tag == ERR_HANDLE_DB
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
def get_about_me(request):
    """
    获取学生的“关于我”
    成功：返回{'err': SUCCEED, 'about_me_list': rlt['about_me_list']}
    失败：返回相应的err和msg的JSON
    """
    if request.method == 'POST':
        stu_id = request.POST.get('stu_id')
        rlt = about_me.get(stu_id)

        if rlt['tag'] == about_me.OK_GET_ABOUT_ME:
            return HttpResponse(json_helper.dumps({
                'err': SUCCEED,
                'about_me_list': rlt['about_me_list']
            }))

        # tag == ERR_GET_ABOUT_ME_DB
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
def update_about_me(request):
    """
    更新学生的“关于我”
    成功：返回{'err': SUCCEED}
    失败：返回相应的err和msg的JSON
    """
    if request.method == 'POST':
        stu_id = request.POST.get('stu_id')
        about_me_id = request.POST.get('about_me_id')
        title = request.POST.get('title')
        text = request.POST.get('text')
        rlt = about_me.update(about_me_id, title, text, stu_id)

        if rlt['tag'] == about_me.OK_UPDATE_ABOUT_ME:
            return HttpResponse(json_helper.dumps({'err': SUCCEED}))

        # tag == ERR_UPDATE_ABOUT_ME_DB
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
def add_about_me(request):
    """
    添加关于我
    成功：返回{
                'err': SUCCEED,
                'about_me_id': add_rlt['about_me_id']
            }
    失败：返回相应的err和msg的JSON
    """
    if request.method == 'POST':
        stu_id = request.POST.get('stu_id')
        title = request.POST.get('title')
        text = request.POST.get('text')

        add_rlt = about_me.add(title, text, stu_id)
        # 如果增加成功
        if add_rlt['tag'] == about_me.OK_ADD_ABOUT_ME:
            return HttpResponse(json_helper.dumps({
                'err': SUCCEED,
                'about_me_id': add_rlt['about_me_id']
            }))

        # 如果数据库异常导致增加作品集信息失败(add_rlt['tag'] == ERR_ADD_ABOUT_ME_DB)
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
def del_about_me(request):
    """
    删除关于我
    成功：返回{'err': SUCCEED}
    失败：返回相应的err和msg的JSON
    """
    if request.method == 'POST':
        about_me_id = request.POST.get('about_me_id')
        stu_id = request.POST.get('stu_id')

        del_rlt = about_me.delete(about_me_id, stu_id)
        # 如果增加成功
        if del_rlt['tag'] == about_me.OK_DEL_ABOUT_ME:
            return HttpResponse(json_helper.dumps({'err': SUCCEED}))

        # 如果数据库异常导致删除关于我失败(del_rlt['tag'] == ERR_DEL_ABOUT_ME_DB)
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
def get_works(request):
    """
    获取学生作品集
    成功：返回{
                'err': SUCCEED,
                'works_id': get_rlt['works_id'],
                'path': get_rlt['path'],
                'site': get_rlt['site']
            }
    失败：返回相应的err和msg的JSON
    """
    if request.method == 'POST':
        stu_id = request.POST.get('stu_id')
        get_rlt = works.get(stu_id)

        # 如果获取成功
        if get_rlt['tag'] == OK_GET_WORKS:
            return HttpResponse(json_helper.dumps({
                'err': SUCCEED,
                'works_list': get_rlt['works_list']
            }))

        # 如果该学生没有作品
        elif get_rlt['tag'] == ERR_GET_NO_WORKS:
            return HttpResponse(json_helper.dumps({
                'err': NO_WORKS,
                'msg': NO_WORKS_MSG
            }))

        # get_rlt['tag'] == ERR_GET_WORKS_DB
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
def update_works(request):
    """
    更新作品集信息
    成功：返回{'err': SUCCEED}
    失败：返回相应的err和msg的JSON
    """
    if request.method == 'POST':
        stu_id = request.POST.get('stu_id')
        works_id = request.POST.get('works_id')
        name = request.POST.get('name')
        duty = request.POST.get('duty')
        url = request.POST.get('url')
        description = request.POST.get('description')
        img = request.POST.get('img')
        audio = request.POST.get('audio')
        video = request.POST.get('video')

        update_rlt = works.update(works_id, stu_id, name, duty, url, description, img, audio, video)
        # 如果更新作品集信息成功
        if update_rlt['tag'] == OK_UPDATE_WORKS:
            return HttpResponse(json_helper.dumps({'err': SUCCEED}))

        # 如果不存在或数据库异常导致更新作品集信息失败
        # (add_rlt['tag'] == ERR_UPDATE_WORKS_DB)或(add_rlt['tag'] == ERR_UPDATE_NOTEXIST)
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
def add_works(request):
    """
    增加作品集信息
    成功：返回{
                'err': SUCCEED,
                'works_id': add_rlt['works_id']
            }
    失败：返回相应的err和msg的JSON
    """
    if request.method == 'POST':
        stu_id = request.POST.get('stu_id')
        name = request.POST.get('name')
        duty = request.POST.get('duty')
        url = request.POST.get('url')
        description = request.POST.get('description')
        img = request.POST.get('img')
        audio = request.POST.get('audio')
        video = request.POST.get('video')

        add_rlt = works.add(stu_id, name, duty, url, description, img, audio, video)
        # 如果增加作品集信息成功
        if add_rlt['tag'] == works.OK_ADD_WORKS:
            return HttpResponse(json_helper.dumps({
                'err': SUCCEED,
                'works_id': add_rlt['works_id']
            }))

        # 如果已有作品集信息
        elif add_rlt['tag'] == works.ERR_ADD_WORKS_FULL:
            return HttpResponse(json_helper.dumps({
                'err': WORKS_FULL,
                'msg': WORKS_FULL_MSG
            }))

        # 如果数据库异常导致增加作品集信息失败(add_rlt['tag'] == ERR_ADD_WORKS_DB)
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
def del_works(request):
    """
    删除作品集信息
    成功：返回{'err': SUCCEED}
    失败：返回相应的err和msg的JSON
    """
    if request.method == 'POST':
        stu_id = request.POST.get('stu_id')
        works_id = request.POST.get('works_id')

        del_rlt = works.delete(stu_id=stu_id, works_id=works_id)
        # 如果删除成功
        if del_rlt['tag'] == works.OK_DEL_works:
            return HttpResponse(json_helper.dumps({'err': SUCCEED}))

        # 如果数据库异常导致删除作品集信息失败(add_rlt['tag'] == ERR_DEL_WORKS_DB)
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
def top6(request):
    """
    获取人气最高的6个学生
    成功：返回{
                'err': SUCCEED,
                'top_list': get_rlt['top_list'],
            }
    失败：返回相应的err和msg的JSON
    """
    if request.method == 'GET':
        rlt = square.top6()

        # 如果获取成功
        if rlt['tag'] == square.OK_GET_TOP6:
            return HttpResponse(json_helper.dumps({
                'err': SUCCEED,
                'top_list': rlt['top_list']
            }))

        else:
            return HttpResponse(json_helper.dumps({
                'err': FAIL,
                'msg': FAIL_MSG
            }))

    # 如果请求的方法是POST
    else:
        return HttpResponse(json_helper.dumps({
            'err': ERR_METHOD,
            'msg': ERR_METHOD_MSG
        }))


@csrf_exempt
def top6_in_label(request):
    """
    获取人气最高的6个学生
    成功：返回{
                'err': SUCCEED,
                'top_list': get_rlt['top_list'],
            }
    失败：返回相应的err和msg的JSON
    """
    if request.method == 'POST':
        label = int(request.POST.get('label'))
        rlt = square.top6_in_label(label)

        # 如果获取成功
        if rlt['tag'] == square.OK_GET_TOP6:
            return HttpResponse(json_helper.dumps({
                'err': SUCCEED,
                'top_list': rlt['top_list']
            }))

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
