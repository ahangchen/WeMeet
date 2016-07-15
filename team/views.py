# coding=utf8
from django.shortcuts import render

# Create your views here.
from team.ctrl.register import validate
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from team.models import Team, Product, Job
from django.core import serializers
from haystack.query import SearchQuerySet
from django.db.models import Q
from functools import reduce
from team.ctrl.err_code_msg import *

import json
import operator


def test(request):
    return render(request, 'team/test.html', {})


def valid_code(request):
    return validate(request)

@csrf_exempt
def search(request):
    """
    搜索职位、团队、项目信息
    成功： 职位、团队、项目相关信息
    失败：返回相应的err和msg的JSON
    """

    import logging
    # logging.debug(type())

    models = {'job':Job,'team':Team,'product':Product}
    res = {'err':ERROR_METHOD,'message':ERROR_METHOD_MSG}

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
            res_list = [ {k:(obj.__dict__)[k] for k in res_name } for obj in res]
        res = {'err':0,'message':res_list}
    elif request.method == 'POST':
        res['message'] = ERROR_SEARCHMODEL_MSG

    res = json.dumps(res, ensure_ascii=False)
    return HttpResponse(res)
