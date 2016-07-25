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

from student.models import StuProj
from student.util.logger import logger


def stu_filter(stu):
    """
    用学生查询项目记录
    返回QuerySet
    """
    return StuProj.objects.filter(stu=stu)


def insert(name, duty, year, description, stu):
    """
    插入项目经历
    成功：返回{'tag': OK_INSERT, 'new_proj': new_proj}
    失败：返回{'tag': ERR_INSERT_DB}
    """
    try:
        new_proj = StuProj(name=name,
                           duty=duty,
                           year=year,
                           description=description,
                           stu=stu)

        new_proj.save()
        return {'tag': OK_INSERT,
                'proj': new_proj}
    except:
        logger.error('数据库异常导致插入项目经历记录失败')
        return {'tag': ERR_INSERT_DB}