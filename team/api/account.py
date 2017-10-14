from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from student.util import json_helper

from team.ctrl import acc_mng
from team.ctrl.acc_mng import ACC_MNG_OK, ACC_UNABLE, LOGIN_FAIL_NO_MATCH
from team.ctrl.err_code_msg import SUCCEED, ERR_UNKNOWN, MSG_FAIL, ERR_STH_NO_MATCH, MSG_SUCC, MSG_RESET_KEY_ERR, \
    ERR_ACC_UNABLE, MSG_ACC_UNABLE, MSG_ACC_PWD_NO_MATCH, MSG_ACC_INV_NO_MATCH, MSG_ACC_NOT_FOUND
from team.ctrl.sess import gen_token
from team.ctrl.team import ACC_NO_FOUND
from team.util.request import is_post, resp_method_err, resp_valid_err, is_valid_ok


@csrf_exempt
def register(request):
    if not is_post(request):
        return resp_method_err()
    # 如果验证码错误 todo: 上线后启动验证码校验机制
    if not is_valid_ok(request):
        return resp_valid_err()
    # 如果验证码正确
    mail = request.POST.get('mail')
    pwd = request.POST.get('pwd')
    inv_code = request.POST.get('inv_code')
    ret = acc_mng.register(mail, pwd, inv_code)
    # 如果注册成功
    if ret == ACC_MNG_OK:
        return HttpResponse(json_helper.dump_err_msg(SUCCEED, MSG_SUCC))
    # 如果数据库异常导致注册失败
    else:
        return HttpResponse(json_helper.dump_err_msg(ERR_STH_NO_MATCH, MSG_ACC_INV_NO_MATCH))


@csrf_exempt
def login(request):
    """
    登陆
    成功：返回 {'err': SUCCEED }
    失败：返回相应的err和msg的JSON
    """
    if not is_post(request):
        return resp_method_err()
    # if not is_valid_ok(request):
    #     return resp_valid_err()
    acnt = request.POST.get('mail')
    pwd = request.POST.get('pwd')
    ret, tid, token = acc_mng.login(acnt, pwd)
    # 如果登陆成功
    if ret == ACC_MNG_OK:
        return HttpResponse(json_helper.dumps({'err': 0, 'res': tid, 'token': token}))
    # 如果不匹配
    elif ret == LOGIN_FAIL_NO_MATCH:
        return HttpResponse(json_helper.dump_err_msg(ERR_STH_NO_MATCH, MSG_ACC_PWD_NO_MATCH))
    # 如果账号未激活
    elif ret == ACC_UNABLE:
        return HttpResponse(json_helper.dump_err_msg(ERR_ACC_UNABLE, MSG_ACC_UNABLE))
    # 未知错误
    else:
        return HttpResponse(json_helper.dump_err_msg(ERR_UNKNOWN, MSG_FAIL))


@csrf_exempt
def reset(request):
    """
    发送账号重置邮件
    reset: send reset mail
    成功: 返回 {err: SUCCEED}
    失败：返回相应的err和msg的JSON
    """
    if not is_post(request):
        return resp_method_err()
    tid = request.POST.get('mail')
    ret = acc_mng.send_reset_mail(tid)
    if ret == ACC_MNG_OK:
        return HttpResponse(json_helper.dump_err_msg(SUCCEED, MSG_SUCC))
    elif ret == ACC_NO_FOUND:
        return HttpResponse(json_helper.dump_err_msg(ERR_STH_NO_MATCH, MSG_ACC_NOT_FOUND))


@csrf_exempt
def fetch(request):
    """
    重置密码，修改账号状态为未激活
    成功：返回{'err': SUCCEED, 'key': key, 'account': acnt}
                              key: 用户修改密码的凭据; account: 未加密的账号
    失败：返回相应的err和msg
    """
    return render(request, 'team/fetch.html', {'hash_tid': request.GET['reset_key'], 'mail': request.GET['mail']})


@csrf_exempt
def update_pwd(request):
    """
    修改密码
    成功: 返回 {err: SUCCEED}
    失败：返回相应的err和msg的JSON
    """
    if not is_post(request):
        return resp_method_err()
    mail = request.POST['mail']
    hash_tid = request.POST['key']
    pwd = request.POST['pwd']
    if ACC_MNG_OK == acc_mng.update_pwd(mail, hash_tid, pwd):
        return HttpResponse(json_helper.dump_err_msg(SUCCEED, MSG_SUCC))
    else:
        return HttpResponse(json_helper.dump_err_msg(ERR_STH_NO_MATCH, MSG_RESET_KEY_ERR))


@csrf_exempt
def invite(request):
    if not is_post(request):
        return resp_method_err()
    name = request.POST['name']
    leader = request.POST['leader']
    tel = request.POST['tel']
    mail = request.POST['mail']
    inv_code = acc_mng.invite(name, leader, tel, mail)
    if inv_code is not None:
        return HttpResponse(json_helper.dump_err_msg(SUCCEED, inv_code))
    else:
        return HttpResponse(json_helper.dump_err_msg(ERR_UNKNOWN, MSG_FAIL))

