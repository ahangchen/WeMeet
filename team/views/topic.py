from django.http import HttpResponse
from student.util import json_helper
from team.ctrl import topic
from team.ctrl.err_code_msg import SUCCEED


def new(request):
    tid = request.POST['tid']
    title = request.POST['title']
    content = request.POST['content']
    return HttpResponse(json_helper.dumps_err(SUCCEED, topic.new(tid, title, content)))


def update(request):
    tpid = request.POST['topic']
    title = request.POST['title']
    content = request.POST['content']
    topic.update(tpid, title, content)
    return HttpResponse(json_helper.dumps_err(SUCCEED, '修改成功'))


def remove(request):
    tpid = request.POST['topic']
    topic.remove(tpid)
    return HttpResponse(json_helper.dumps_err(SUCCEED, '删除成功'))


def info(request):
    tpid = request.POST['topic']
    return HttpResponse(json_helper.dumps_err(SUCCEED, topic.get(tpid)))