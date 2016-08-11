from team.models import Job, Team
from team.db.tag import SUCCEED,ERR_JOB_NOT_EXIT,MSG_JOB_NOT_EXIT,ERR_PROD_TABLE,MSG_PROD_TABLE

DB_OK = 0
DB_ACC_NOT_FOUND = 1


def id_job(job_id):
    job = Job.objects.filter(id=job_id).first()
    if job is None:
        return None
    else:
        return job


def select(job_id):
    """
        查询product,如果存在,返回项目信息,否则,返回错误信息
        成功：返回{'tag': PRODUCT_SUCCEED, 'msg': product}
        失败：返回{'tag': ERR_PROD_NOT_EXIT/ERR_PROD_TABLE,
                'msg': 错误信息}
    """
    try:
        job = Job.objects.all().get(id=job_id)
        return {'err': SUCCEED,
                'msg': job}
    except Job.DoesNotExist:
        return {'err': ERR_JOB_NOT_EXIT,
                'msg': MSG_JOB_NOT_EXIT}
    except:
        return {'err': ERR_PROD_TABLE,
                'msg': MSG_PROD_TABLE}


def newest():
    jobs = Job.objects.all().order_by('-id')[: 3]
    jobs_ret = [
        {'jid': job.id,
         'tid': job.team_id,
         'team_logo': job.team.logo_path,
         'j_name': job.name,
         't_name': job.team.name
         } for job in jobs
        ]
    return {'jobs': jobs_ret}