from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from student.util import json_helper
from team.ctrl import topic
from team.ctrl.err_code_msg import SUCCEED


@csrf_exempt
def new(request):
    tid = request.POST['tid']
    title = request.POST['title']
    content = request.POST['content']
    return HttpResponse(json_helper.dumps_err(SUCCEED, topic.new(tid, title, content)))


@csrf_exempt
def update(request):
    tpid = request.POST['topic']
    title = request.POST['title']
    content = request.POST['content']
    topic.update(tpid, title, content)
    return HttpResponse(json_helper.dumps_err(SUCCEED, '修改成功'))


@csrf_exempt
def remove(request):
    tpid = request.POST['topic']
    topic.remove(tpid)
    return HttpResponse(json_helper.dumps_err(SUCCEED, '删除成功'))


@csrf_exempt
def info(request):
    tpid = request.GET['topic']
    return HttpResponse(json_helper.dumps_err(SUCCEED, topic.get(tpid)))


@csrf_exempt
def list(request):
    tid = request.GET['tid']
    return HttpResponse(json_helper.dump_err_msg(SUCCEED, topic.list(tid)))