# coding=utf8

from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from team.ctrl.register import validate


def test(request):
    return render(request, 'team/test.html', {})


@csrf_exempt
def valid_code(request):
    return validate(request)
