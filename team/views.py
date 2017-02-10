# coding=utf8
import json
import operator
from functools import reduce

from django.db.models import Q
from django.db.models import Sum
from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from haystack.query import SearchQuerySet

from student.ctrl import account
from student.ctrl.err_code_msg import ERR_REG_IDEXIST, ERR_REG_IDEXIST_MSG
from student.ctrl.tag import OK_REG
from student.util import json_helper
from student.views import team_get_apply, apply_info, apply_reply, team_apply_handle
from team.ctrl import acc_mng
from team.ctrl import job
from team.ctrl import team
from team.ctrl.acc_mng import ACC_MNG_OK, LOGIN_FAIL_NO_MATCH, ACC_UNABLE, ACC_NO_FOUND
from team.ctrl.err_code_msg import *
from team.ctrl.job import JOB_NOT_FOUND
from team.ctrl.register import validate
from team.ctrl.team import bus_names
from team.models import Team, Product, Job
from team.util.request import is_post, resp_method_err, is_valid_ok, resp_valid_err


def test(request):
    return render(request, 'team/test.html', {})


@csrf_exempt
def valid_code(request):
    return validate(request)



@csrf_exempt
def hot_product(request):
    """
        搜索热门项目信息
        成功： 项目的名称、简介、logo、ID
        失败：返回相应的err和msg的JSON
    """
    res_list = Product.objects.extra(select={'visit_cnt': 'last_visit_cnt + '
                                                          'week_visit_cnt'}).order_by('-visit_cnt').values('name',
                                                                                                           'img_path',
                                                                                                           'content',
                                                                                                           'id')
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
                                     last_visit_cnt=Sum('product__last_visit_cnt')).order_by('-week_visit_cnt',
                                                                                             '-last_visit_cnt') \
        .values('name', 'about', 'logo_path', 'id')
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
    ret, tid = acc_mng.login(acnt, pwd)
    # 如果登陆成功
    if ret == ACC_MNG_OK:
        return HttpResponse(json_helper.dump_err_msg(SUCCEED, str(tid)))
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
def info(request):
    """获取团队信息"""
    tid = request.GET['tid']
    team_dict = team.info(tid)
    if team_dict is not None:
        return HttpResponse(json_helper.dumps_err(0, team_dict))
    else:
        return HttpResponse(json_helper.dump_err_msg(ERR_STH_NO_MATCH, MSG_ACC_NOT_FOUND))


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



@csrf_exempt
def update_team_contact(request):
    if not is_post(request):
        return resp_method_err()
    tid = request.POST['tid']
    tel = request.POST['tel']
    mail = request.POST['mail']
    ret = team.update_contact(tid, tel, mail)
    if ret == team.ACC_NO_FOUND:
        return HttpResponse(json_helper.dump_err_msg(ERR_STH_NO_MATCH, MSG_ACC_NOT_FOUND))
    else:
        return HttpResponse(json_helper.dump_err_msg(SUCCEED, MSG_SUCC))


@csrf_exempt
def rm_team_photo(request):
    if not is_post(request):
        return resp_method_err()
    tid = request.POST['tid']
    img_id = request.POST['img_id']
    ret = team.rm_photo(tid, img_id)
    if ret == team.ACC_NO_FOUND:
        return HttpResponse(json_helper.dump_err_msg(ERR_STH_NO_MATCH, MSG_ACC_NOT_FOUND))
    else:
        return HttpResponse(json_helper.dump_err_msg(SUCCEED, MSG_SUCC))


@csrf_exempt
def add_team_photo(request):
    if not is_post(request):
        return resp_method_err()
    tid = request.POST['tid']
    img = request.FILES['photo']
    name = str(img)
    ret, path = team.save_photo(tid, name, img)
    if ret == team.ACC_NO_FOUND:
        return HttpResponse(json_helper.dump_err_msg(ERR_STH_NO_MATCH, MSG_ACC_NOT_FOUND))
    else:
        photo_ret = {'img_id': ret, 'path': path}
        return HttpResponse(json_helper.dump_err_msg(SUCCEED, photo_ret))


@csrf_exempt
def add_team_stu(request):
    if not is_post(request):
        return resp_method_err()
    tid = request.POST['tid']
    sid = request.POST['sid']
    ret = team.add_stu(tid, sid)
    if ret == team.ACC_NO_FOUND:
        return HttpResponse(json_helper.dump_err_msg(ERR_STH_NO_MATCH, MSG_ACC_NOT_FOUND))
    elif ret == team.STU_NO_FOUND:
        return HttpResponse(json_helper.dump_err_msg(ERR_STU_NOT_FOUND, MSG_STU_NOT_FOUND))
    else:
        return HttpResponse(json_helper.dump_err_msg(SUCCEED, MSG_SUCC))


@csrf_exempt
def rm_team_stu(request):
    if not is_post(request):
        return resp_method_err()
    tid = request.POST['tid']
    sid = request.POST['sid']
    ret = team.rm_stu(tid, sid)
    if ret == team.ACC_NO_FOUND:
        return HttpResponse(json_helper.dump_err_msg(ERR_STH_NO_MATCH, MSG_ACC_NOT_FOUND))
    elif ret == team.NO_MATCH:
        return HttpResponse(json_helper.dump_err_msg(ERR_STU_NOT_FOUND, MSG_STU_NOT_FOUND))
    else:
        return HttpResponse(json_helper.dump_err_msg(SUCCEED, MSG_SUCC))


@csrf_exempt
def add_team_label(request):
    if not is_post(request):
        return resp_method_err()
    tid = request.POST['tid']
    name = request.POST['name']
    ret = team.add_label(tid, name)
    if ret == team.ACC_NO_FOUND:
        return HttpResponse(json_helper.dump_err_msg(ERR_STH_NO_MATCH, MSG_ACC_NOT_FOUND))
    else:
        return HttpResponse(json_helper.dump_err_msg(SUCCEED, ret))


@csrf_exempt
def rm_team_label(request):
    if not is_post(request):
        return resp_method_err()
    tid = request.POST['tid']
    name = request.POST['name']
    ret = team.rm_label(tid, name)
    if ret == team.ACC_NO_FOUND:
        return HttpResponse(json_helper.dump_err_msg(ERR_STH_NO_MATCH, MSG_ACC_NOT_FOUND))
    else:
        return HttpResponse(json_helper.dump_err_msg(SUCCEED, MSG_SUCC))


@csrf_exempt
def update_team_info(request):
    if not is_post(request):
        return resp_method_err()
    tid = request.POST['tid']
    name = request.POST['name']
    logo_path = request.POST['logo_path']
    slogan = request.POST['slogan']
    btype = request.POST['btype']
    about = request.POST['about']
    history = request.POST['history']
    ret = team.update_info(tid, name, logo_path, slogan, about, history, btype)
    if ret == team.ACC_NO_FOUND:
        return HttpResponse(json_helper.dump_err_msg(ERR_STH_NO_MATCH, MSG_ACC_NOT_FOUND))
    else:
        return HttpResponse(json_helper.dump_err_msg(SUCCEED, MSG_SUCC))


@csrf_exempt
def business(request):
    name = bus_names()
    if name is not None:
        return HttpResponse(json_helper.dump_err_msg(SUCCEED, name))
    else:
        return HttpResponse(json_helper.dump_err_msg(ERR_UNKNOWN, MSG_FAIL))


@csrf_exempt
def name2mail(request):
    name = request.GET['name']
    mails = team.name2mail(name)
    return HttpResponse(json_helper.dumps_err(SUCCEED, mails))


@csrf_exempt
def invite_stu(request):
    """团队邀请成员"""
    if not is_post(request):
        return resp_method_err()
    mail = request.POST['mail']
    tid = request.POST['tid']
    ret, sid = account.invite(mail)
    add_ret = team.add_stu(tid, sid)
    if ret != OK_REG:
        return HttpResponse(json_helper.dump_err_msg(ERR_REG_IDEXIST, ERR_REG_IDEXIST_MSG))
    if add_ret == team.ACC_NO_FOUND:
        return HttpResponse(json_helper.dump_err_msg(ERR_STH_NO_MATCH, MSG_ACC_NOT_FOUND))
    else:
        return HttpResponse(json_helper.dump_err_msg(SUCCEED, sid))


@csrf_exempt
def get_apply_list(request):
    """
    团队获取投递列表
    """
    return team_get_apply(request)


@csrf_exempt
def get_apply_info(request):
    """
    团队获取投递信息
    """
    return apply_info(request)


@csrf_exempt
def apply_mail(request):
    """
    团队邮件回复投递
    """
    return apply_reply(request)


@csrf_exempt
def apply_handle(request):
    """
    团队邮件回复投递
    """
    return team_apply_handle(request)


@csrf_exempt
def upload_logo(request):
    if not is_post(request):
        return resp_method_err()
    img = request.FILES['photo']
    name = str(img)
    path = team.save_logo(name, img)
    return HttpResponse(json_helper.dump_err_msg(SUCCEED, path))


@csrf_exempt
def newest(request):
    return HttpResponse(json_helper.dumps_err(SUCCEED, team.new_team_project_job()))


def newest_teams(request):
    return HttpResponse(json_helper.dumps_err(SUCCEED, team.newest_teams()))
