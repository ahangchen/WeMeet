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

from student.models import StuInfo

from student.util.value_update import value, NO_INPUT
from student.util.logger import logger


def delete(stu_id):
    """
    删除
    成功返回OK_DELETE
    失败返回ERR_DELETE_DB
    """
    try:
        delete_stu = StuInfo.objects.all().get(id=stu_id)  # 抛出MultipleObjectsReturned或DoesNotExist
        delete_stu.delete()  # 不抛出异常
        return OK_DELETE

    except StuInfo.DoesNotExist:
        logger.error('尝试删除不存在的学生')
        return ERR_DELETE_DB

    except StuInfo.MultipleObjectsReturned:
        logger.info('数据库异常（存在重复记录）')
        StuInfo.objects.all().filter(id=stu_id).delete()  # 不抛异常
        return OK_DELETE

    # 数据库异常
    except:
        logger.error('数据库异常导致删除学生失败')
        return ERR_DELETE_DB


def update(stu_id, name=NO_INPUT, school=NO_INPUT, tel=NO_INPUT,
           mail=NO_INPUT, avatar_path=NO_INPUT, edu_background=NO_INPUT,
           grade=NO_INPUT, major=NO_INPUT, location=NO_INPUT):
    """
    成功：返回OK_UPDATE
    失败：返回ERR_UPDATE_NOTEXIST
          或ERR_UPDATE_DB
    """
    try:
        update_stu = StuInfo.objects.all().get(id=stu_id)

        update_stu.name = value(update_stu.name, name)
        update_stu.school = value(update_stu.school, school)
        update_stu.tel = value(update_stu.tel, tel)
        update_stu.mail = value(update_stu.mail, mail)
        update_stu.avatar_path = value(update_stu.avatar_path, avatar_path)
        update_stu.edu_background = value(update_stu.edu_background, edu_background)
        update_stu.grade = value(update_stu.grade, grade)
        update_stu.major = value(update_stu.major, major)
        update_stu.location = value(update_stu.location, location)

        update_stu.save()
        return OK_UPDATE
    except StuInfo.DoesNotExist:
        logger.error('尝试更新不存在的学生')
        return ERR_UPDATE_NOTEXIST
    except:
        logger.error('数据库异常导致更新学生失败')
        return ERR_UPDATE_DB


def select(stu_id):
    """
    成功：返回{'tag': OK_SELECT, 'stu': select_stu}
    失败：返回{'tag': ERR_SELECT_NOTEXIST}
           或{'tag': ERR_SELECT_DB}
    """
    try:
        select_stu = StuInfo.objects.all().get(id=stu_id)
        return {'tag': OK_SELECT,
                'stu': select_stu}
    except StuInfo.DoesNotExist:
        return {'tag': ERR_SELECT_NOTEXIST}
    except:
        logger.error('数据库异常导致查询学生失败')
        return {'tag': ERR_SELECT_DB}


def insert(name, school, tel, mail, avatar_path, edu_background, grade, major, location):
    """
    成功：返回插入的学生
    失败：返回ERROR_INSERT
    """
    try:
        new_stu = StuInfo(name=name,
                          school=school,
                          tel=tel,
                          mail=mail,
                          avatar_path=avatar_path,
                          edu_background=edu_background,
                          grade=grade,
                          major=major,
                          location=location)
        new_stu.save()  #  如果是手工设置的主键，会抛出 IntegrityError， save和create等价
        return new_stu
#        return GOOD_INSERT
    except:
        # TODO(hjf): log到日志
        return ERR_INSERT_DB







