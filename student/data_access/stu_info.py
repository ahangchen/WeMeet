from student.data_access.tag import ERR_DELETE_MULT
from student.data_access.tag import ERR_DELETE_NOTEXIST
from student.data_access.tag import ERR_DELETE_DB
from student.data_access.tag import ERR_UPDATE_NOTEXIST
from student.data_access.tag import ERR_INSERT_DB
from student.data_access.tag import ERR_SELECT_NOTEXIST
from student.data_access.tag import OK_DELETE
from student.data_access.tag import OK_INSERT
from student.data_access.tag import OK_UPDATE

from student.models import StuInfo

from student.utility.value_update import value, NO_INPUT


def delete(stu_id):  # TODO(HJF): 改成只返回ERR_DELEET
    try:
        delete_stu = StuInfo.objects.all().get(id=stu_id)  # 抛出MultipleObjectsReturned或DoesNotExist
        delete_stu.delete()  # 不抛出异常
        return OK_DELETE

    except StuInfo.DoesNotExist:
        # TODO(hjf): log到日志
        return ERR_DELETE_NOTEXIST

    except StuInfo.MultipleObjectsReturned:
        # TODO(hjf): log到日志
        StuInfo.objects.all().filter(id=stu_id).delete()  # 不抛异常
        return ERR_DELETE_MULT

    # 数据库异常
    except:
        # TODO(hjf): log到日志，修改返回内容
        return ERR_DELETE_DB


def update(stu_id, name=NO_INPUT, school=NO_INPUT, tel=NO_INPUT,
           mail=NO_INPUT, avatar_path=NO_INPUT, edu_background=NO_INPUT,
           grade=NO_INPUT, major=NO_INPUT, location=NO_INPUT):
    """
    成功：返回GOOD_UPDATE
    失败：返回ERROR_UPDATE_DOESNOTEXIST
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
        # TODO(hjf): log到日志
        return ERR_UPDATE_NOTEXIST
    except:
        # TODO(hjf): log到日志，修改返回内容（读写发生竞争条件）
        return ERR_UPDATE_NOTEXIST


def select(stu_id):
    """
    成功：返回select_stu
    失败：返回ERROR_SELECT_DOESNOTEXIST
    """
    try:
        select_stu = StuInfo.objects.all().get(id=stu_id)
        return select_stu
    except StuInfo.DoesNotExist:
        # TODO(hjf): log到日志
        return ERR_SELECT_NOTEXIST
    except:
        # TODO(hjf): log到日志, 修改返回内容
        return ERR_SELECT_NOTEXIST


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







