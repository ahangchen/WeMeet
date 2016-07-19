from team.db import job

from enum import Enum

# PUB_STATE = Enum('待发布', '已发布', '已下架')
JOB_NOT_FOUND = -1


def info(job_id):
    obj = job.id_job(job_id)
    if obj is not None:
        return obj
    else:
        return JOB_NOT_FOUND
