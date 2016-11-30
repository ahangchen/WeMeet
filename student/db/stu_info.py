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
from student.db.tag import NO_RESUME

from student.models import StuInfo

from student.util.value_update import value, NO_INPUT
from student.util.logger import logger


# def delete(stu_id):
#     """
#     删除
#     成功返回OK_DELETE
#     失败返回ERR_DELETE_DB
#     """
#     try:
#         delete_stu = StuInfo.objects.all().get(id=stu_id)  # 抛出MultipleObjectsReturned或DoesNotExist
#         delete_stu.delete()  # 不抛出异常
#         return OK_DELETE
#
#     except StuInfo.DoesNotExist:
#         logger.error('尝试删除不存在的学生')
#         return ERR_DELETE_DB
#
#     except StuInfo.MultipleObjectsReturned:
#         logger.info('数据库异常（存在重复记录）')
#         StuInfo.objects.all().filter(id=stu_id).delete()  # 不抛异常
#         return OK_DELETE
#
#     # 数据库异常
#     except Exception as e:
#         logger.error(e.__str__() + '数据库异常导致删除学生失败')
#         return ERR_DELETE_DB
#
#
def update(stu_id, name=NO_INPUT, title=NO_INPUT, personal_signature=NO_INPUT, sex=NO_INPUT, school=NO_INPUT, grade=NO_INPUT, avatar_path=NO_INPUT,
           resume_path=NO_INPUT, label1=NO_INPUT, likes=NO_INPUT):
    """
    成功：返回OK_UPDATE
    失败：返回ERR_UPDATE_NOTEXIST
          或ERR_UPDATE_DB
    """
    try:
        update_stu = StuInfo.objects.all().get(id=stu_id)

        update_stu.name = value(update_stu.name, name)
        update_stu.sex = value(update_stu.sex, sex)
        update_stu.title = value(update_stu.title, title)
        update_stu.personal_signature = value(update_stu.personal_signature, personal_signature)
        update_stu.grade = value(update_stu.grade, grade)
        update_stu.school = value(update_stu.school, school)
        update_stu.label1 = value(update_stu.label1, label1)
        update_stu.likes = value(update_stu.likes, likes)
        update_stu.avatar_path = value(update_stu.avatar_path, avatar_path)
        update_stu.resume_path = value(update_stu.resume_path, resume_path)

        update_stu.save()
        return OK_UPDATE
    except StuInfo.DoesNotExist:
        logger.error('尝试更新不存在的学生')
        return ERR_UPDATE_NOTEXIST
    except Exception as e:
        logger.error(e.__str__() + '数据库异常导致更新学生失败')
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
    except Exception as e:
        logger.error(e.__str__() + '数据库异常导致查询学生失败')
        return {'tag': ERR_SELECT_DB}


def insert(name, title, personal_signature, sex, school, grade, avatar_path, label1):
    """
    成功：返回插入的学生
    失败：返回ERROR_INSERT
    """
    try:
        new_stu = StuInfo(name=name,
                          title=title,
                          personal_signature=personal_signature,
                          sex=sex,
                          school=school,
                          grade=grade,
                          avatar_path=avatar_path,
                          label1=label1,
                          likes=0,
                          resume_path=NO_RESUME)
        new_stu.save()  # 如果是手工设置的主键，会抛出 IntegrityError
        return new_stu
#        return GOOD_INSERT
    except Exception as e:
        logger.error(e.__str__() + '数据库异常导致插入学生失败')
        return ERR_INSERT_DB


def query(stu_id):
    return StuInfo.objects.filter(id=stu_id)







