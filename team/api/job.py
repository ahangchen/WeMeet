import json

from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from team.ctrl import job
from team.ctrl.err_code_msg import ERR_POST_TYPE, MSG_POST_TYPE, SUCCEED, MSG_SUCC, ERR_JOB_TYPE, ERR_JOB_NONE, \
    MSG_JOB_NONE, MSG_JOB_TYPE, ERR_JOB_NOT_FOUND, MSG_JOB_NOT_FOUND
from team.ctrl.job import JOB_NOT_FOUND
from team.db.form import JobForm
from team.db.tag import PRODUCT_SUCCEED
from team.models import JobType, Job
from team.util.request import is_post, resp_method_err
from team.db import job as db_job
from student.util import json_helper


@csrf_exempt
def update_job(request):
    """
        修改职位信息
        成功: 返回相应的err和message的JSON
        失败：返回相应的err和message的JSON
    """
    if not is_post(request):
        return resp_method_err()

    if request.META.get('CONTENT_TYPE', request.META.get('CONTENT_TYPE', 'application/json')) == 'application/json':
        req_data = json.loads(request.body.decode('utf-8'))
        id = req_data['id']
    else:
        id = request.POST['id']
        req_data = request.POST
        if not id.isdigit():
            return HttpResponse(json.dumps({'err': ERR_JOB_TYPE, 'message': MSG_JOB_TYPE}, ensure_ascii=False))

    if not Job.objects.filter(id=id):
        return HttpResponse(json.dumps({'err': ERR_JOB_NONE, 'message': MSG_JOB_NONE}, ensure_ascii=False))

    job = Job.objects.get(id=id)
    job_form = JobForm(req_data, request.FILES)
    if job_form.is_valid():
        for (key, value) in job_form.cleaned_data.items():
            if value:
                job.__dict__[key] = value
            job.save()
        return HttpResponse(json.dumps({'err': SUCCEED, 'message': MSG_SUCC}, ensure_ascii=False))
    return HttpResponse(json.dumps({'err': ERR_JOB_TYPE, 'message': dict(job_form._errors)}, ensure_ascii=False))


@csrf_exempt
def add_job(request):
    """
        添加职位信息
        成功: 返回职位ID
        失败：返回相应的err和message的JSON
    """
    if not is_post(request):
        return resp_method_err()

    if request.META.get('CONTENT_TYPE', request.META.get('CONTENT_TYPE', 'application/json')) == 'application/json':
        req_data = json.loads(request.body.decode('utf-8'))
    else:
        req_data = request.POST
    print(req_data)
    job_form = JobForm(req_data, request.FILES)
    if job_form.is_valid():
        job = Job(**job_form.cleaned_data)
        job.save()
        return HttpResponse(json.dumps({'err': SUCCEED, 'message': MSG_SUCC, 'msg': job.id}, ensure_ascii=False))
    return HttpResponse(json.dumps({'err': ERR_JOB_TYPE, 'message': dict(job_form._errors)}, ensure_ascii=False))


@csrf_exempt
def delete_job(request):
    """
        删除职位信息
        成功: 返回相应的err和msg的JSON
        失败：返回相应的err和msg的JSON
    """
    if not is_post(request):
        return resp_method_err()

    job_id = request.POST.get('jobId')
    res = db_job.select(job_id)

    if res['err'] != PRODUCT_SUCCEED:
        return HttpResponse(json.dumps(res, ensure_ascii=False))

    job = res['msg']
    job.delete()

    return HttpResponse(json.dumps({'err': SUCCEED, 'msg': MSG_SUCC}, ensure_ascii=False))


@csrf_exempt
def job_type(request):
    """
        查找职位类型
        成功: 职位类型ID和name
    """

    jobType = JobType.objects.values()
    return HttpResponse(json.dumps({'err': SUCCEED, 'msg': list(jobType)}, ensure_ascii=False))


@csrf_exempt
def search_job(request):
    """
        根据职位信息搜索职位信息
        成功: 返回职位信息
        失败：返回相应的err和message的JSON
    """
    if not is_post(request):
        return resp_method_err()

    team_id = job_type = request.POST.get('teamId')
    job_tags = request.POST.getlist('jobTags[]')
    job_type = list()
    for job_tag in job_tags:
        if job_tag != '':
            job_type.append(job_tag)
    print(job_type)

    if False:  # ToDo(wang) check param # not job_type[0].isdigit():
        return HttpResponse(json.dumps({'err': ERR_POST_TYPE, 'message': MSG_POST_TYPE}, ensure_ascii=False))

    res_list = Job.objects.filter(j_type__in=job_type, team_id=team_id).extra(
        select={'jobId': 'id', 'minSaraly': 'min_salary', 'maxSaraly': 'max_salary', 'exp': 'exp_cmd',
                'job_state': 'pub_state'}).values('jobId', 'name', 'address', 'minSaraly', 'maxSaraly', 'city', 'town',
                                                  'exp', 'job_state')

    res = json.dumps({'err': SUCCEED, 'message': list(res_list)}, ensure_ascii=False)
    return HttpResponse(res)


@csrf_exempt
def job_info(request):
    """
    获取职位信息
    成功: 返回职位信息
    失败：返回相应的err和msg的JSON
    """
    if not is_post(request):
        return resp_method_err()
    job_id = request.POST.get('id')
    rlt = job.info(job_id)
    if rlt != JOB_NOT_FOUND:
        return HttpResponse(json_helper.dumps({
            'err': SUCCEED,
            'team_id': rlt.team.id,
            'job_name': rlt.name,
            'min_salary': rlt.min_salary,
            'max_salary': rlt.max_salary,
            'prince': rlt.prince,
            'city': rlt.city,
            'town': rlt.town,
            'address': rlt.address,
            'edu_cmd': rlt.edu_cmd,
            'exp_cmd': rlt.exp_cmd,
            'job_type': rlt.j_type,
            'work_type': rlt.w_type,
            'summary': rlt.summary,
            'pub_date': rlt.pub_date,
            'pub_state': rlt.pub_state,
            'job_cmd': rlt.job_cmd,
            'work_cmd': rlt.work_cmd,
        }))
    else:
        return HttpResponse(json_helper.dump_err_msg(ERR_JOB_NOT_FOUND, MSG_JOB_NOT_FOUND))
