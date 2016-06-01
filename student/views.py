# coding=utf8
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from student.BLL import stu_info_op
from student.Utility.tag import *
import json

# for test...
from django.shortcuts import render
def post(request):
    return render(request, 'POST.html')


@csrf_exempt
def register_stu(request):
    if request.method == "POST":
        stu_id = request.POST.get('stu_id')
        psw = request.POST.get('psw')

        tag = stu_info_op.register(stu_id=stu_id, psw=psw)
        if tag == GOOD_REGISTER:
            err = '0'
            msg = 'register succeed'
        else:
            err = '-1'
            msg = 'stu_id exists'

        json_ctx = {'err': err, 'msg': msg}
        return HttpResponse(json.dumps(json_ctx, ensure_ascii=False))
    json_ctx = {'err': '-2', 'msg': "wrong method"}
    return HttpResponse(json.dumps(json_ctx, ensure_ascii=False))


@csrf_exempt
def update_stu_info(request):
    if request.method == "POST":
        stu_id = request.POST.get('stu_id', NO_INPUT)
        # check if stu_id is posted
        if stu_id == NO_INPUT:
            json_ctx = {'err': '-3', 'msg': 'post does not contain stu_id'}
            return HttpResponse(json.dumps(json_ctx, ensure_ascii=False))

        # if stu_id is posted
        stu_name = request.POST.get('stu_name', NO_INPUT)
        stu_school = request.POST.get('stu_school', NO_INPUT)
        stu_tel = request.POST.get('stu_tel', NO_INPUT)
        stu_mail = request.POST.get('mail', NO_INPUT)

        tag = stu_info_op.update_info(stu_id=stu_id,
                                      stu_name=stu_name,
                                      stu_school=stu_school,
                                      stu_tel=stu_tel,
                                      stu_mail=stu_mail)

        if tag == GOOD_UPDATE_INFO:
            err = '0'
            msg = 'update_stu_info succeed'
        else:
            err = '-1'
            msg = 'stu_id does not exist'

        json_ctx = {'err': err, 'msg': msg}
        return HttpResponse(json.dumps(json_ctx, ensure_ascii=False))

    # if request method is get
    json_ctx = {'err': '-2', 'msg': 'wrong method'}
    return HttpResponse(json.dumps(json_ctx, ensure_ascii=False))


@csrf_exempt
def get_stu_info(request):
    if request.method == "POST":
        stu_id = request.POST.get('stu_id', NO_INPUT)
        # check if stu_id is posted
        if stu_id == NO_INPUT:
            json_ctx = {'err': '-3', 'msg': 'post does not contain stu_id'}
            return HttpResponse(json.dumps(json_ctx, ensure_ascii=False))

        # if stu_id is posted
        temp = stu_info_op.get_info(stu_id)
        # if stu_id exists and return a Stuinfo
        if temp != ERROR_GET_INFO:
            err = '0'
            msg = 'get_stu_info succeed'
            json_ctx = {'err': err,
                        'msg': msg,
                        'stu_id': temp.stu_id,
                        'stu_name': temp.stu_name,
                        'stu_school': temp.stu_school,
                        'stu_tel': temp.stu_tel,
                        'stu_mail': temp.stu_mail}
            return HttpResponse(json.dumps(json_ctx, ensure_ascii=False))

        # if stu_id does not exist
        json_ctx = {'err': '-1', 'msg': 'stu_id does not exist'}
        return HttpResponse(json.dumps(json_ctx, ensure_ascii=False))

    # if post method is get
    json_ctx = {'err': '-2', 'msg': 'wrong method'}
    return HttpResponse(json.dumps(json_ctx, ensure_ascii=False))


















