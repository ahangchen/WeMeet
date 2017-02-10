from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from student.ctrl.err_code_msg import ERR_REG_IDEXIST, ERR_REG_IDEXIST_MSG
from student.ctrl.tag import OK_REG
from team.api import account
from team.ctrl import team
from team.ctrl.err_code_msg import SUCCEED, MSG_ACC_NOT_FOUND, ERR_STH_NO_MATCH, ERR_UNKNOWN, MSG_FAIL, MSG_SUCC, \
    ERR_STU_NOT_FOUND, MSG_STU_NOT_FOUND
from team.ctrl.team import bus_names
from team.util.request import is_post, resp_method_err
from student.util import json_helper


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
def upload_logo(request):
    if not is_post(request):
        return resp_method_err()
    img = request.FILES['photo']
    name = str(img)
    path = team.save_logo(name, img)
    return HttpResponse(json_helper.dump_err_msg(SUCCEED, path))
