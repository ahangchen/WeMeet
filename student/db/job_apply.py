from student.db.tag import ERR_DELETE_NOTEXIST
from student.db.tag import ERR_DELETE_DB
from student.db.tag import ERR_UPDATE_NOTEXIST
from student.db.tag import ERR_UPDATE_DB
from student.db.tag import ERR_INSERT_DB
from student.db.tag import ERR_SELECT_NOTEXIST
from student.db.tag import ERR_SELECT_DB
from student.db.tag import OK_DELETE
from student.db.tag import OK_INSERT
from student.db.tag import OK_UPDATE
from student.db.tag import OK_SELECT

from student.models import JobApply

from student.util.logger import logger


def insert(stu, job, state, team, resume_path, change_time, stu_read, team_read):
    """
    插入一条投递简历的记录
    成功：{'tag': OK_INSERT, 'apply': new_apply}
    失败：返回{'tag': ERR_INSERT_DB}
    """
    try:
        new_apply = JobApply(stu=stu,
                             job=job,
                             state=state,
                             team=team,
                             resume_path=resume_path,
                             change_time=change_time,
                             stu_read=stu_read,
                             team_read=team_read)
        new_apply.save()
        return {'tag': OK_INSERT,
                'apply': new_apply}

    # 如果插入投递记录发生异常
    except:
        logger.error('数据库异常导致插入投递简历记录失败')
        return {'tag': ERR_INSERT_DB}


def stu_job_select(stu, job):
    """
    用学生id和职位id查询投递记录
    成功： 返回{'tag': OK_SELECT, 'apply': select_apply}
    失败： 返回{'tag': ERR_SELECT_NOTEXIST}
            或{'tag': ERR_SELECT_DB}
    """
    try:
        select_apply = JobApply.objects.get(stu=stu, job=job)
        return {'tag': OK_SELECT,
                'apply': select_apply}
    except JobApply.DoesNotExist:
        return {'tag': ERR_SELECT_NOTEXIST}
    except:
        logger.error('数据库异常导致查询投递记录失败')
        return {'tag': ERR_SELECT_DB}


def stu_state_filter(stu, state):
    """
    用学生和投递状态查询投递记录
    返回QuerySet
    """
    return JobApply.objects.filter(stu=stu, state=state)




