from student.models import StuInfo
from student.Utility.DAL_utility import value
from student.Utility.tag import *


def delete(stu_id):
    try:
        delete_stu = StuInfo.objects.all().get(stu_id=stu_id)
        delete_stu.delete()
        return GOOD_DELETE
    except StuInfo.DoesNotExist:
        return ERROR_DELETE_DOESNOTEXIST


def update(stu_id, psw=NO_INPUT, stu_name=NO_INPUT, stu_school=NO_INPUT,
           stu_tel=NO_INPUT, stu_mail=NO_INPUT):
    try:
        update_stu = StuInfo.objects.all().get(stu_id=stu_id)

        update_stu.stu_psw = value(update_stu.psw, psw)
        update_stu.stu_name = value(update_stu.stu_name, stu_name)
        update_stu.stu_school = value(update_stu.stu_school, stu_school)
        update_stu.stu_tel = value(update_stu.stu_tel, stu_tel)
        update_stu.stu_mail = value(update_stu.stu_mail, stu_mail)

        update_stu.save()
        return GOOD_UPDATE
    except StuInfo.DoesNotExist:
        return ERROR_UPDATE_DOESNOTEXIST


def select(stu_id):
    try:
        select_stu = StuInfo.objects.all().get(stu_id=stu_id)
        return select_stu
    except StuInfo.DoesNotExist:
        return ERROR_SELECT_DOESNOTEXIST


def insert(stu_id, psw, stu_name, stu_school, stu_tel, stu_mail):
    tag = select(stu_id)
    if tag == ERROR_SELECT_DOESNOTEXIST:
        new_stu = StuInfo(stu_id=stu_id,
                          psw=psw,
                          stu_name=stu_name,
                          stu_school=stu_school,
                          stu_tel=stu_tel,
                          stu_mail=stu_mail)
        new_stu.save()
        return GOOD_INSERT
    return ERROR_INSERT







