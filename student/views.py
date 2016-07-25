# coding=utf8
from django.http import HttpResponse
from django.shortcuts import render  # for test method
from django.views.decorators.csrf import csrf_exempt

from student.ctrl import info
from student.ctrl import account
from student.ctrl import avatar
from student.ctrl import resume
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
                                      ERR_EDU_FULL, ERR_EDU_FULL_MSG, \
                                      ERR_OUT_DATE, ERR_OUT_DATE_MSG, \
                                      ERR_METHOD, ERR_METHOD_MSG, \
                                      NO_INTERN, NO_INTERN_MSG, \
                                      NO_RESUME, NO_RESUME_MSG, \
                                      NO_WORKS, NO_WORKS_MSG, \
                                      NO_SKILL, NO_SKILL_MSG, \
                                      NO_PROJ, NO_PROJ_MSG, \
                                      NO_EDU, NO_EDU_MSG, \
                                      FAIL, FAIL_MSG, \
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
from student.ctrl.tag import OK_ADD_INTERN
from student.ctrl.tag import ERR_ADD_INTERN_FULL
from student.ctrl.tag import ERR_ADD_INTERN_DB
from student.ctrl.tag import OK_UPDATE_INTERN
from student.ctrl.tag import ERR_UPDATE_INTERN_DB
from student.ctrl.tag import OK_DEL_INTERN
from student.ctrl.tag import ERR_DEL_INTERN_DB


# from student.util.tag import NO_INPUT
from student.util import json_helper


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


def fetch(request):
    """
    渲染前端重置密码的页面
    method: GET
    成功：返回渲染页面
    失败：返回相应的err和msg的JSON
    """
    return render(request, 'team/fetch.html', {'hash_tid': request.GET['reset_key'], 'mail': request.GET['mail']})


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
    成功： 返回err: SUCCEED，头像路径，姓名，学校, 性别，出生年份，出生月份，年龄，专业，所在地，联系方式（tel），邮箱, 简历地址
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
                'school': get_rlt['stu'].school,
                'sex': get_rlt['stu'].sex,
                'year': get_rlt['stu'].year,
                'month': get_rlt['stu'].month,
                'major': get_rlt['stu'].major,
                'location': get_rlt['stu'].location,
                'tel': get_rlt['stu'].tel,
                'mail': get_rlt['stu'].mail,
                'resume_path': get_rlt['stu'].resume_path,
                'age': get_rlt['age']
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
        stu_id = request.POST.get('id')
        avatar_path = request.POST.get('path')
        name = request.POST.get('name')
        school = request.POST.get('school')
        major = request.POST.get('major')
        location = request.POST.get('location')
        sex = request.POST.get('sex')
        year = request.POST.get('year')
        month = request.POST.get('month')
        mail = request.POST.get('mail')
        tel = request.POST.get('tel')

        tag = info.update(stu_id=stu_id, avatar_path=avatar_path, name=name, school=school,
                          major=major, location=location, sex=sex, year=year,
                          month=month, mail=mail, tel=tel)

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


@csrf_exempt
def add_edu(request):
    """
    增加教育经历
    成功：返回：{
                'err': SUCCEED,
                'edu_id': add_rlt['edu_id'],
                'grade': add_rlt['grade'],
                'edu_background': add_rlt['edu_background']
            }
    失败：返回相应的err和msg的JSON
    """
    if request.method == 'POST':
        stu_id = request.POST.get('stu_id')
        major = request.POST.get('major')
        graduation_year = request.POST.get('graduation_year')
        background = request.POST.get('edu_background')
        school = request.POST.get('school')

        add_rlt = info.add_edu(stu_id, major, graduation_year, background, school)
        # 如果增加教育经历成功
        if add_rlt['tag'] == OK_ADD_EDU:
            return HttpResponse(json_helper.dumps({
                'err': SUCCEED,
                'edu_id': add_rlt['edu_id'],
                'grade': add_rlt['grade'],
                'edu_background': add_rlt['edu_background']
            }))

        # 如果教育经历已达上限
        elif add_rlt['tag'] == ERR_ADD_EDU_FULL:
            return HttpResponse(json_helper.dumps({
                'err': ERR_EDU_FULL,
                'msg': ERR_EDU_FULL_MSG
            }))

        # 如果数据库异常导致增加教育经历失败(add_rlt['tag'] == ERR_ADD_EDU_DB)
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
def get_edu(request):
    """
    获取学生的教育经历
    成功：返回{
                'err': SUCCEED,
                'grade': get_rlt['grade'],
                'major': get_rlt['major'],
                'edu_list': get_rlt['edu_list']
            }
            get_rlt['edu_list']: [{'edu_id': edu_rcd.id,
                                  'major': edu_rcd.major,
                                  'graduation_year': edu_rcd.graduation_year,
                                  'edu_background': edu_rcd.background,
                                  'school': edu_rcd.school}]
    失败：返回相应的err和msg的JSON
    """
    if request.method == 'POST':
        stu_id = request.POST.get('stu_id')
        get_rlt = info.get_edu(stu_id)

        # 如果获取成功
        if get_rlt['tag'] == OK_GET_EDU:
            return HttpResponse(json_helper.dumps({
                'err': SUCCEED,
                'grade': get_rlt['grade'],
                'edu_background': get_rlt['edu_background'],
                'edu_list': get_rlt['edu_list']
            }))

        # 如果该学生没有教育经历
        elif get_rlt['tag'] == ERR_GET_NO_EDU:
            return HttpResponse(json_helper.dumps({
                'err': NO_EDU,
                'msg': NO_EDU_MSG
            }))

        # get_rlt['tag'] == ERR_GET_EDU_DB
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
def update_edu(request):
    """
    更新教育经历
    成功：返回{
                'err': SUCCEED,
                'edu_id': update_rlt['edu_id'],
                'grade': update_rlt['grade'],
                'edu_background': update_rlt['edu_background']
            }
    失败：返回相应的err和msg的JSON
    """
    if request.method == 'POST':
        stu_id = request.POST.get('stu_id')
        edu_id = request.POST.get('edu_id')
        major = request.POST.get('major')
        graduation_year = request.POST.get('graduation_year')
        background = request.POST.get('edu_background')
        school = request.POST.get('school')

        update_rlt = info.update_edu(stu_id, edu_id, major, graduation_year, background, school)
        # 如果更新教育经历成功
        if update_rlt['tag'] == OK_UPDATE_EDU:
            return HttpResponse(json_helper.dumps({
                'err': SUCCEED,
                'grade': update_rlt['grade'],
                'edu_background': update_rlt['edu_background']
            }))

        # 如果数据库异常导致更新教育经历失败(add_rlt['tag'] == ERR_UPDATE_EDU_DB)
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
def del_edu(request):
    """
    删除教育经历
    成功:返回{
                'err': SUCCEED,
                'grade': del_rlt['grade'],
                'edu_background': del_rlt['edu_background']
            }
    失败：返回相应的err和msg的JSON
    """
    if request.method == 'POST':
        stu_id = request.POST.get('stu_id')
        edu_id = request.POST.get('edu_id')

        del_rlt = info.del_edu(stu_id=stu_id, edu_id=edu_id)
        # 如果删除成功
        if del_rlt['tag'] == OK_DEL_EDU:
            return HttpResponse(json_helper.dumps({
                'err': SUCCEED,
                'grade': del_rlt['grade'],
                'edu_background': del_rlt['edu_background']
            }))
        # 如果数据库异常导致删除教育经历失败(add_rlt['tag'] == ERR_DEL_EDU_DB)
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
def add_intern(request):
    """
    增加实习经历
    成功：返回{'err': SUCCEED}
    失败：返回相应的err和msg的JSON
    """
    if request.method == 'POST':
        stu_id = request.POST.get('stu_id')
        company = request.POST.get('company')
        position = request.POST.get('position')
        begin_time = request.POST.get('begin_time')
        end_time = request.POST.get('end_time')
        description = request.POST.get('description')

        add_rlt = info.add_intern(stu_id, company, position, begin_time, end_time, description)
        # 如果增加实习经历成功
        if add_rlt['tag'] == OK_ADD_INTERN:
            return HttpResponse(json_helper.dumps({'err': SUCCEED}))

        # 如果实习经历已达上限
        elif add_rlt['tag'] == ERR_ADD_INTERN_FULL:
            return HttpResponse(json_helper.dumps({
                'err': ERR_INTERN_FULL,
                'msg': ERR_INTERN_FULL_MSG
            }))

        # 如果数据库异常导致增加实习经历失败(add_rlt['tag'] == ERR_ADD_INTERN_DB)
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
def update_intern(request):
    """
    更新实习经历
    成功：返回
    失败：返回相应的err和msg的JSON
    """
    if request.method == 'POST':
        stu_id = request.POST.get('stu_id')
        intern_id = request.POST.get('intern_id')
        company = request.POST.get('company')
        position = request.POST.get('position')
        begin_time = request.POST.get('begin_time')
        end_time = request.POST.get('end_time')
        description = request.POST.get('description')

        update_rlt = info.update_intern(intern_id, stu_id, company, position, begin_time, end_time, description)
        # 如果更新实习经历成功
        if update_rlt['tag'] == OK_UPDATE_INTERN:
            return HttpResponse(json_helper.dumps({'err': SUCCEED}))

        # 如果数据库异常导致更新实习经历失败(add_rlt['tag'] == ERR_UPDATE_INTERN_DB)
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
def del_intern(request):
    """
    删除实习经历
    成功：返回

    """
    if request.method == 'POST':
        stu_id = request.POST.get('stu_id')
        intern_id = request.POST.get('intern_id')

        del_rlt = info.del_intern(stu_id=stu_id, intern_id=intern_id)
        # 如果删除成功
        if del_rlt['tag'] == OK_DEL_INTERN:
            return HttpResponse(json_helper.dumps({'err': SUCCEED}))

        # 如果数据库异常导致删除教育经历失败(add_rlt['tag'] == ERR_DEL_INTERN_DB)
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
def get_intern(request):
    """
    获取实习经历
    成功：返回{'err': SUCCEED, 'intern_list': get_rlt['intern_list']}
    失败：返回相应的err和msg的JSON
    """
    if request.method == 'POST':
        stu_id = request.POST.get('stu_id')
        get_rlt = info.get_intern(stu_id)

        # 如果获取成功
        if get_rlt['tag'] == OK_GET_INTERN:
            return HttpResponse(json_helper.dumps({
                'err': SUCCEED,
                'intern_list': get_rlt['intern_list']
            }))

        # 如果该学生没有实习经历
        elif get_rlt['tag'] == ERR_GET_NO_INTERN:
            return HttpResponse(json_helper.dumps({
                'err': NO_INTERN,
                'msg': NO_INTERN_MSG
            }))

        # get_rlt['tag'] == ERR_GET_INTERN_DB
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
def get_proj(request):
    """
    获取项目经历
    成功：返回{'err': SUCCEED, 'proj_list': get_rlt['proj_list']}
                            "proj_list": [{
            　　　　　　                      "proj_id": proj_id,
            　　　　　　                      "name": name,
            　　　　　　                      "duty": duty,
            　　　　　　                      "year": year,
            　　　　　　                      "description": description},
            　　　                         ...]}
    失败：返回相应的err和msg的JSON
    """
    if request.method == 'POST':
        stu_id = request.POST.get('stu_id')
        get_rlt = info.get_proj(stu_id)

        # 如果获取成功
        if get_rlt['tag'] == OK_GET_PROJ:
            return HttpResponse(json_helper.dumps({
                'err': SUCCEED,
                'proj_list': get_rlt['proj_list']
            }))

        # 如果该学生没有项目经历
        elif get_rlt['tag'] == ERR_GET_NO_PROJ:
            return HttpResponse(json_helper.dumps({
                'err': NO_PROJ,
                'msg': NO_PROJ_MSG
            }))

        # get_rlt['tag'] == ERR_GET_PROJ_DB
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
        get_rlt = info.get_works(stu_id)

        # 如果获取成功
        if get_rlt['tag'] == OK_GET_WORKS:
            return HttpResponse(json_helper.dumps({
                'err': SUCCEED,
                'works_id': get_rlt['works_id'],
                'path': get_rlt['path'],
                'site': get_rlt['site']
            }))

        # 如果该学生没有作品集
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
        get_rlt = info.get_skill(stu_id)

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













