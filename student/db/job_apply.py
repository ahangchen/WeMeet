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


def insert(stu, job, team, resume_path):
    """
    插入一条投递简历的记录
    成功：{'tag': OK_INSERT, 'apply': new_apply}
    失败：返回{'tag': ERR_INSERT_DB}
    """
    try:
        new_apply = JobApply(stu=stu,
                             job=job,
                             state=0,
                             team=team,
                             resume_path=resume_path)
        new_apply.save()
        return {'tag': OK_INSERT,
                'apply': new_apply}

    # 如果插入投递记录发生异常
    except:
        logger.error('数据库异常导致插入投递简历记录失败')
        return {'tag': ERR_INSERT_DB}



