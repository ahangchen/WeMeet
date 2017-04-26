from django.views.decorators.csrf import csrf_exempt

from student.views import apply_reply, team_apply_handle, apply_info, team_get_apply


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
