# coding=utf8
import json
import operator
from functools import reduce

from django.db.models import Q
from django.db.models import Sum
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from haystack.query import SearchQuerySet

from student.util import json_helper
from team.ctrl import team
from team.ctrl import topic
from team.ctrl.err_code_msg import *
from team.models import Team, Product, Job
from team.util.request import check_post


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
@check_post
def search(request):
    """
    搜索职位、团队、项目信息
    成功： 职位、团队、项目相关信息
    失败：返回相应的err和msg的JSON
    """
    import logging

    models = {'job': Job, 'team': Team, 'product': Product}
    res = {'err': ERROR_METHOD, 'message': MSG_METHOD_ERR}

    # logging.debug(model)
    if not request.POST.get('model'):
        model = [Job, Team, Product]
    else:
        model = [models[request.POST.get('model')]]
    search_type = request.POST.get('type')
    content = request.POST.get('keys')
    keys = content.split(' ')
    condition = reduce(operator.and_, (Q(content__contains=x) for x in keys))
    logging.debug(condition)

    if search_type:
        res = SearchQuerySet().filter(typy=int(search_type)).filter(condition).models(*model)
    else:
        res = SearchQuerySet().filter(condition).models(*model)

    res_list = []
    if res.count():
        for obj in res:
            obj_dict = {}
            res_name = (obj.__dict__)['_additional_fields']
            res_name.append('pk')
            for k in res_name:
                obj_dict[k] = (obj.__dict__)[k]
            obj_dict['model'] = obj.__dict__['model_name']
            res_list.append(obj_dict)
        # res_name = (res[0].__dict__)['_additional_fields']
        # res_name.append('pk')
        # res_list = [{k: (obj.__dict__)[k] for k in res_name} for obj in res]
    res = {'err': SUCCEED, 'message': res_list}

    res = json.dumps(res, ensure_ascii=False)
    return HttpResponse(res)


@csrf_exempt
def newest(request):
    return HttpResponse(json_helper.dumps_err(SUCCEED, team.new_team_project_job()))


def newest_teams(request):
    team_type = request.GET['b_type']
    return HttpResponse(json_helper.dumps_err(SUCCEED, team.newest_teams(team_type)))


def newest_topic(request):
    return HttpResponse(json_helper.dumps_err(SUCCEED, topic.newest()))
