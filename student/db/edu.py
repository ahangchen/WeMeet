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


def select(id):
    """
    用id查询教育经历记录
    成功： 返回{'tag': OK_SELECT, 'edu': select_edu}
    失败： 返回{'tag': ERR_SELECT_NOTEXIST}
            或{'tag': ERR_SELECT_DB}
    """
    try:
        select_edu = StuEdu.objects.get(id=id)
        return {'tag': OK_SELECT,
                'edu': select_edu}
    except StuEdu.DoesNotExist:
        return {'tag': ERR_SELECT_NOTEXIST}
    except:
        logger.error('数据库异常导致查询教育经历记录失败')
        return {'tag': ERR_SELECT_DB}


def id_stu_update(edu_id, stu, major=NO_INPUT, graduation_year=NO_INPUT, background=NO_INPUT, school=NO_INPUT):
    """
    用学生和edu_id更新教育经历
    @edu_id: 教育经历记录
    @stu: 关联的学生
    @major: 专业
    @graduation_year: 毕业年份
    @background: 学历
    @school: 学校
    成功：返回OK_UPDATE
    失败：返回ERR_UPDATE_DB
    """
    try:
        update_edu = StuEdu.objects.all().get(id=edu_id, stu=stu)

        update_edu.major = value(update_edu.major, major)
        update_edu.graduation_year = value(update_edu.graduation_year, graduation_year)
        update_edu.background = value(update_edu.background, background)
        update_edu.school = value(update_edu.school, school)

        update_edu.save()
        return OK_UPDATE

    except StuEdu.DoesNotExist:
        logger.warning("尝试更新学生id和教育经历id不匹配的教育经历")
        return ERR_UPDATE_DB
    except:
        logger.error('数据库异常导致更新教育经历失败')
        return ERR_UPDATE_DB


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
        update_edu = StuEdu.objects.all().get(id=edu_id)

        update_edu.major = value(update_edu.major, major)
        update_edu.graduation_year = value(update_edu.graduation_year, graduation_year)
        update_edu.background = value(update_edu.background, background)
        update_edu.school = value(update_edu.school, school)

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


def id_insert(edu_id, major, graduation_year, background, school, stu):
    """
    包含id的插入教育经历
    成功：返回{'tag': OK_INSERT, 'edu': new_edu}
    失败：返回{'tag': ERR_INSERT_DB}
    """
    try:
        new_edu = StuEdu(id=id,
                         major=major,
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


def delete(edu_id):
    """
    删除
    成功返回OK_DELETE
    失败返回ERR_DELETE_DB
    """
    try:
        delete_edu = StuEdu.objects.all().get(id=edu_id)  # 抛出MultipleObjectsReturned或DoesNotExist
        delete_edu.delete()  # 不抛出异常
        return OK_DELETE

    except StuEdu.DoesNotExist:
        logger.error('尝试删除不存在的教育经历')
        return ERR_DELETE_DB

    except StuEdu.MultipleObjectsReturned:
        logger.info('数据库异常（存在重复记录）')
        StuEdu.objects.all().filter(id=edu_id).delete()  # 不抛异常
        return OK_DELETE

    # 数据库异常
    except:
        logger.error('数据库异常导致删除教育经历失败')
        return ERR_DELETE_DB


def id_stu_delete(edu_id, stu):
    """
    用id和stu删除教育经历
    成功：返回OK_DELETE
    失败：返回ERR_DELETE_DB
    """
    try:
        delete_edu = StuEdu.objects.all().get(id=edu_id, stu=stu)  # 抛出MultipleObjectsReturned或DoesNotExist
        delete_edu.delete()  # 不抛出异常
        return OK_DELETE

    except StuEdu.DoesNotExist:
        logger.error('尝试删除学生id和教育经历id不匹配的教育经历')
        return ERR_DELETE_DB

    except StuEdu.MultipleObjectsReturned:
        logger.info('数据库异常（存在重复记录）')
        StuEdu.objects.all().filter(id=edu_id).delete()  # 不抛异常
        return OK_DELETE

    # 数据库异常
    except:
        logger.error('数据库异常导致删除教育经历失败')
        return ERR_DELETE_DB



