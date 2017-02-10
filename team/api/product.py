import json

from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from team.ctrl import product
from team.ctrl.err_code_msg import SUCCEED
from team.ctrl.product import check_param
from team.db.tag import PRODUCT_SUCCEED
from team.util.request import is_post, resp_method_err, check_post
from team.db import product as db_product


@csrf_exempt
@check_post
def search_product(request):
    """
        根据团队ID搜索项目信息
        成功: 返回项目信息
        失败：返回相应的err和msg的JSON
    """
    team_id = request.POST.get('teamId')

    if False:  # ToDo(wang) check param # not job_type[0].isdigit():
        return HttpResponse(json.dumps({'err': ERR_POST_TYPE, 'msg': MSG_POST_TYPE}, ensure_ascii=False))

    res_list = Product.objects.filter(team_id=team_id).values('name', 'img_path', 'content', 'reward', 'id',
                                                              'last_visit_cnt', 'week_visit_cnt')

    res = json.dumps({'err': SUCCEED, 'msg': list(res_list)}, ensure_ascii=False)
    return HttpResponse(res)


@csrf_exempt
def info_product(request):
    """
        查询项目信息
        成功: 返回项目信息
        失败：返回相应的err和message的JSON
    """
    prod_list = ['name', 'img_path', 'content', 'reward', 'team_id',
                 'last_visit_cnt', 'week_visit_cnt']

    if not is_post(request):
        return resp_method_err()
    prod_id = request.POST.get('productId')
    if prod_id is None:
        prod_id = request.GET.get('productId')
    print(prod_id)
    res = db_product.select(prod_id)

    if res['err'] == PRODUCT_SUCCEED:
        prod_dict = {key: res['msg'].__dict__[key] for key in prod_list}
        res = {'err': SUCCEED,
               'msg': prod_dict}

    return HttpResponse(json.dumps(res, ensure_ascii=False))


@csrf_exempt
def delete_product(request):
    """
        删除项目信息
        成功: 返回相应的err和msg的JSON
        失败：返回相应的err和msg的JSON
    """
    if not is_post(request):
        return resp_method_err()

    prod_id = request.POST.get('productId')
    res = db_product.select(prod_id)

    if res['err'] != PRODUCT_SUCCEED:
        return HttpResponse(json.dumps(res, ensure_ascii=False))

    prod = res['msg']
    product.delete_img(prod_id=prod.id)
    prod.delete()

    return HttpResponse(json.dumps({'err': SUCCEED, 'msg': MSG_SUCC}, ensure_ascii=False))


@csrf_exempt
@check_param
def add_product(request):
    """
        添加项目信息
        成功: 返回项目ID
        失败：返回相应的err和msg的JSON
    """
    if not is_post(request):
        return resp_method_err()

    # 判断是否插入
    res = db_product.insert(**request.POST.DATA)
    if res['err'] != PRODUCT_SUCCEED:
        return HttpResponse(json.dumps(res, ensure_ascii=False))

    prod_img = request.FILES.get('prod_img')
    if prod_img:
        res_img = product.save_img(prod_id=res['msg'].id, prod_img=prod_img)
        if res_img['err'] != PRODUCT_SUCCEED:
            return HttpResponse(json.dumps(res_img, ensure_ascii=False))
    return HttpResponse(json.dumps({'err': SUCCEED, 'message': MSG_SUCC, 'msg': res['msg'].id}, ensure_ascii=False))


@csrf_exempt
@check_param
def update_product(request):
    """
        编辑项目信息
        成功: 返回项目ID
        失败：返回相应的err和msg的JSON
    """
    if not is_post(request):
        return resp_method_err()

    # # 判断POST请求类型
    # if request.META.get('CONTENT_TYPE', request.META.get('CONTENT_TYPE', 'application/json')) == 'application/json':
    #     req_data = json.loads(request.body.decode('utf-8'))
    #     id = req_data['id']
    # else:
    #     req_data = request.POST
    #     id = request.POST['id']
    #     if not id.isdigit():
    #         return HttpResponse(json.dumps({'err': ERR_PROD_TYPE, 'message': MSG_PROD_TYPE}, ensure_ascii=False))
    #
    # # 判断参数类型
    # prod_form = ProductForm(req_data, request.FILES)
    # if not prod_form.is_valid():
    #     return HttpResponse(json.dumps({'err': ERR_PROD_TYPE, 'message': dict(prod_form._errors)}, ensure_ascii=False))

    res = db_product.select(prod_id=request.POST.DATA['id'])
    if res['err'] != PRODUCT_SUCCEED:
        return HttpResponse(json.dumps(res, ensure_ascii=False))

    # 判断是否插入
    res = db_product.update(**request.POST.DATA)
    if res['err'] != PRODUCT_SUCCEED:
        return HttpResponse(json.dumps(res, ensure_ascii=False))

    prod_img = request.FILES.get('prod_img')
    if prod_img:
        res_img = product.save_img(prod_id=res['msg'].id, prod_img=prod_img)
        if res_img['err'] != PRODUCT_SUCCEED:
            return HttpResponse(json.dumps(res_img, ensure_ascii=False))
    return HttpResponse(json.dumps({'err': SUCCEED, 'message': MSG_SUCC, 'msg': res['msg'].id}, ensure_ascii=False))


@csrf_exempt
def save_prod_img(request):
    """
    保存上传的项目照片文件，和更新项目照片
    成功：返回{'err': PRODUCT_SUCCEED, 'msg': img_path}
    失败：返回{'err': ERR_PROD_TABLE/ERR_PROD_NOT_EXIT/ERR_PROD_SAVE_IMG/ERR_PROD_CHECK_IMG,
             'msg': 错误信息}
    """
    if not is_post(request):
        return resp_method_err()

    prod_id = request.POST.get('id')
    prod_img = request.FILES.get('prod_img')
    res = product.save_img(prod_id=prod_id, prod_img=prod_img)

    return HttpResponse(json.dumps({'err': res['err'],
                                    'msg': res['msg']}))
