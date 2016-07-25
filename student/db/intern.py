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

from student.models import StuIntern
from student.util.logger import logger

def stu_filter(stu):
    """
    用学生查询实习经历记录
    返回QuerySet
    """
    return StuIntern.objects.filter(stu=stu)


def insert(company, position, begin_time, end_time, description, stu):
    """
    插入实习经历
    成功：返回{'tag': OK_INSERT, 'intern': new_intern}
    失败：返回{'tag': ERR_INSERT_DB}
    """
    try:
        new_intern = StuIntern(company=company,
                               position=position,
                               begin_time=begin_time,
                               end_time=end_time,
                               description=description,
                               stu=stu)

        new_intern.save()
        return {'tag': OK_INSERT,
                'edu': new_intern}
    except:
        logger.error('数据库异常导致插入实习经历记录失败')
        return {'tag': ERR_INSERT_DB}
