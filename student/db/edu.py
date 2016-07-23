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

from student.models import StuEdu

from student.util.value_update import value, NO_INPUT
from student.util.logger import logger


def stu_filter(stu):
    """
    用学生查询教育经历记录
    返回QuerySet
    """
    return StuEdu.objects.filter(stu=stu)


def update(edu_id, major=NO_INPUT, graduation_year=NO_INPUT, background=NO_INPUT, school=NO_INPUT):
    """
    用edu_id更新教育经历
    成功：返回OK_UPDATE
    失败：返回ERR_UPDATE_NOTEXIST
            或ERR_UPDATE_DB
    @edu_id: 教育经历记录
    @major: 专业
    @graduation_year: 毕业年份
    @background: 学历
    @school: 学校
    """
    try:
        update_edu = StuEdu.objects.all().get(edu_id=edu_id)

        update_edu.name = value(update_edu.major, major)
        update_edu.graduation_year = value(update_edu.graduation_year, graduation_year)
        update_edu.name = value(update_edu.background, background)
        update_edu.name = value(update_edu.school, school)

        update_edu.save()
        return OK_UPDATE

    except StuEdu.DoesNotExist:
        logger.error('尝试更新不存在的教育经历记录')
        return ERR_UPDATE_NOTEXIST
    except:
        logger.error('数据库异常导致更新教育经历失败')
        return ERR_UPDATE_DB


def insert(major, graduation_year, background, school, stu):
    """
    插入教育经历
    成功：返回{'tag': OK_INSERT, 'edu': new_edu}
    失败：返回{'tag': ERR_INSERT_DB}
    """
    try:
        new_edu = StuEdu(major=major,
                         graduation_year=graduation_year,
                         background=background,
                         school=school,
                         stu=stu)

        new_edu.save()
        return {'tag': OK_INSERT,
                'edu': new_edu}
    except:
        logger.error('数据库异常导致插入教育经历记录失败')
        return {'tag': ERR_INSERT_DB}

