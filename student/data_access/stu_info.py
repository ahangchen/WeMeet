from student.data_access.tag import ERROR_DELETE_DOESNOTEXIST
from student.data_access.tag import ERROR_UPDATE_DOESNOTEXIST
from student.data_access.tag import ERROR_INSERT
from student.data_access.tag import ERROR_SELECT_DOESNOTEXIST
from student.data_access.tag import GOOD_DELETE
from student.data_access.tag import GOOD_INSERT
from student.data_access.tag import GOOD_UPDATE

from student.models import StuInfo

from student.utility.value_update import value
from student.utility.tag import NO_INPUT


def delete(stu_id):
    try:
        delete_stu = StuInfo.objects.all().get(id=stu_id)
        delete_stu.delete()
        return GOOD_DELETE
    except StuInfo.DoesNotExist:
        return ERROR_DELETE_DOESNOTEXIST


def update(stu_id, pwd=NO_INPUT, name=NO_INPUT, school=NO_INPUT, tel=NO_INPUT,
           mail=NO_INPUT, avatar_path=NO_INPUT, is_activated=NO_INPUT,
           edu_background=NO_INPUT, grade=NO_INPUT, major=NO_INPUT, location=NO_INPUT):
    """
    成功：返回GOOD_UPDATE
    失败：返回ERROR_UPDATE_DOESNOTEXIST
    """
    try:
        update_stu = StuInfo.objects.all().get(id=stu_id)

        update_stu.pwd = value(update_stu.pwd, pwd)
        update_stu.name = value(update_stu.name, name)
        update_stu.school = value(update_stu.school, school)
        update_stu.tel = value(update_stu.tel, tel)
        update_stu.mail = value(update_stu.mail, mail)
        update_stu.avatar_path = value(update_stu.avatar_path, avatar_path)
        update_stu.is_activated = value(update_stu.is_activated, is_activated)
        update_stu.edu_background = value(update_stu.edu_background, edu_background)
        update_stu.grade = value(update_stu.grade, grade)
        update_stu.major = value(update_stu.major, major)
        update_stu.location = value(update_stu.location, location)

        update_stu.save()
        return GOOD_UPDATE
    except StuInfo.DoesNotExist:
        return ERROR_UPDATE_DOESNOTEXIST


def select(stu_id):
    """
    成功：返回select_stu
    失败：返回ERROR_SELECT_DOESNOTEXIST
    """
    try:
        select_stu = StuInfo.objects.all().get(id=stu_id)
        return select_stu
    except StuInfo.DoesNotExist:
        return ERROR_SELECT_DOESNOTEXIST


def insert(stu_id, pwd, name, school, tel, mail, avatar_path, edu_background, grade, major, location):
    """
    成功：返回GOOD_INSERT
    失败：返回ERROR_INSERT
    """
    tag = select(stu_id)
    if tag == ERROR_SELECT_DOESNOTEXIST:
        new_stu = StuInfo(id=stu_id,
                          pwd=pwd,
                          name=name,
                          school=school,
                          tel=tel,
                          mail=mail,
                          avatar_path=avatar_path,
                          is_activated=False,
                          edu_background=edu_background,
                          grade=grade,
                          major=major,
                          location=location)
        new_stu.save()
        return GOOD_INSERT
    return ERROR_INSERT







