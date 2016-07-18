# coding=utf8
from django.shortcuts import render

# Create your views here.
from team.ctrl import acc_mng
from team.ctrl.acc_mng import ACC_MNG_OK, LOGIN_FAIL_NO_MATCH, ACC_UNABLE, ACC_NO_FOUND
from team.ctrl.register import validate
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from team.models import Team, Product, Job
from django.db.models import  Sum
from haystack.query import SearchQuerySet
from django.db.models import Q
from functools import reduce
from team.ctrl.err_code_msg import *
from student.utility import json_helper

import json
import operator

from team.util.request import is_post, resp_method_err


def test(request):
    return render(request, 'team/test.html', {})


def valid_code(request):
    return validate(request)

@csrf_exempt
def hot_product(request):
    """
        搜索热门项目信息
        成功： 项目的名称、简介、logo、ID
        失败：返回相应的err和msg的JSON
    """
    res_list = Product.objects.extra(select={'visit_cnt':'last_visit_cnt + '
            'week_visit_cnt'}).order_by('-visit_cnt').values('name','img_path','content','id')
    res = {'err': SUCCEED, 'message': list(res_list)}

    res = json.dumps(res, ensure_ascii=False)
    return HttpResponse(res)

@csrf_exempt
def hot_team(request):
    """
        搜索热门团队信息
        成功： 团队的名称、简介、logo、ID
        失败：返回相应的err和msg的JSON
    """
    res_list = Team.objects.annotate(week_visit_cnt=Sum('product__week_visit_cnt'),
                    last_visit_cnt=Sum('product__last_visit_cnt')).order_by('-week_visit_cnt','-last_visit_cnt')\
                    .values('name','about','logo_path','id')
    res = {'err': SUCCEED, 'message': list(res_list)}

    res = json.dumps(res, ensure_ascii=False)
    return HttpResponse(res)

@csrf_exempt
def search(request):
    """
    搜索职位、团队、项目信息
    成功： 职位、团队、项目相关信息
    失败：返回相应的err和msg的JSON
    """
    import logging

    models = {'job': Job, 'team': Team, 'product': Product}
    res = {'err': ERROR_METHOD, 'message': MSG_METHOD_ERR}

    if request.method == 'POST' and request.POST.get('model') in models.keys():
        model = models[request.POST.get('model')]
        search_type = request.POST.get('type')
        content = request.POST.get('keys')
        keys = content.split(' ')
        condition = reduce(operator.and_, (Q(text__contains=x) for x in keys))
        logging.debug(condition)

        if search_type:
            res = SearchQuerySet().filter(typy=int(search_type)).filter(condition).models(model)
        else:
            res = SearchQuerySet().filter(condition).models(model)

        res_list = []
        if res.count():
            res_name = (res[0].__dict__)['_additional_fields']
            res_name.append('pk')
            res_list = [{k: (obj.__dict__)[k] for k in res_name} for obj in res]
        res = {'err': SUCCEED, 'message': res_list}
    elif request.method == 'POST':
        res['message'] = MSG_ERR_SEARCH_TYPE

    res = json.dumps(res, ensure_ascii=False)
    return HttpResponse(res)


@csrf_exempt
def register(request):
    if not is_post(request):
        return resp_method_err()
    # 如果验证码错误 todo: 上线后启动验证码校验机制
    # if request.session['code'] != request.POST.get('code'):
    if False:
        return HttpResponse(json_helper.dump_err_msg(ERR_VALID_CODE, MSG_VALID_CODE_ERR))
    # 如果验证码正确
    acc = request.POST.get('account')
    pwd = request.POST.get('pwd')
    inv_code = request.POST.get('inv_code')
    ret = acc_mng.register(acc, pwd, inv_code)
    # 如果注册成功
    if ret == ACC_MNG_OK:
        return HttpResponse(json_helper.dump_err_msg(SUCCEED, MSG_SUCC))
    # 如果数据库异常导致注册失败
    else:
        return HttpResponse(json_helper.dump_err_msg(ERR_ACCOUNT_NO_MATCH, MSG_ACC_INV_NO_MATCH))


@csrf_exempt
def login(request):
    """
    登陆
    成功：返回 {'err': SUCCEED }
    失败：返回相应的err和msg的JSON
    """
    if not is_post(request):
        return resp_method_err()
    acnt = request.POST.get('account')
    pwd = request.POST.get('pwd')
    ret = acc_mng.login(acnt, pwd)
    # 如果登陆成功
    if ret == ACC_MNG_OK:
        return HttpResponse(json_helper.dump_err_msg(MSG_SUCC, MSG_SUCC))
    # 如果不匹配
    elif ret == LOGIN_FAIL_NO_MATCH:
        return HttpResponse(json_helper.dump_err_msg(ERR_ACCOUNT_NO_MATCH, MSG_ACC_PWD_NO_MATCH))
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
    send_rsmail: send reset mail
    成功: 返回 {err: SUCCEED}
    失败：返回相应的err和msg的JSON
    """
    if not is_post(request):
        return resp_method_err()
    tid = request.POST.get('account')
    ret = acc_mng.send_reset_mail(tid)
    if ret == ACC_MNG_OK:
        return HttpResponse(json_helper.dump_err_msg(MSG_SUCC, MSG_SUCC))
    elif ret == ACC_NO_FOUND:
        return HttpResponse(json_helper.dump_err_msg(ERR_ACCOUNT_NO_MATCH, MSG_ACC_NOT_FOUND))


@csrf_exempt
def fetch(request):
    """
    重置密码，修改账号状态为未激活
    成功：返回{'err': SUCCEED, 'key': key, 'account': acnt}
                              key: 用户修改密码的凭据; account: 未加密的账号
    失败：返回相应的err和msg
    """
    return render(request, 'team/fetch.html', {'reset_key': request.GET['reset_key']})


@csrf_exempt
def update_pwd(request):
    """
    修改密码
    成功: 返回 {err: SUCCEED}
    失败：返回相应的err和msg的JSON
    """
    if not is_post(request):
        return resp_method_err()
    if ACC_MNG_OK:
        return HttpResponse(json_helper.dump_err_msg(MSG_SUCC, MSG_SUCC))
    else:
        return HttpResponse(json_helper.dump_err_msg(ERR_ACCOUNT_NO_MATCH, MSG_RESET_KEY_ERR))

