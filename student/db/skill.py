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

from student.models import StuSkill
from student.util.logger import logger
from student.util.value_update import value, NO_INPUT


def stu_filter(stu):
    """
    用学生查询技能评价
    返回QuerySet
    """
    return StuSkill.objects.filter(stu=stu)


def insert(name, value, stu):
    """
    插入技能评价
    成功：返回{'tag': OK_INSERT, 'skill': new_skill}
    失败：返回{'tag': ERR_INSERT_DB}
    """
    try:
        new_skill = StuSkill(name=name,
                             value=value,
                             stu=stu)

        new_skill.save()
        return {'tag': OK_INSERT,
                'skill': new_skill}
    except:
        logger.error('数据库异常导致插入技能评价记录失败')
        return {'tag': ERR_INSERT_DB}
