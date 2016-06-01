from student.Utility.tag import *
from student.DAL.stu_CURD import *


def register(stu_id, psw):
    tag = insert(stu_id=stu_id, psw=psw, stu_name='', stu_school='', stu_tel='', stu_mail='')
    if tag == GOOD_INSERT:
        return GOOD_REGISTER
    return ERROR_REGISTER


def change_psw(stu_id, psw):
    tag = update(stu_id=stu_id, psw=psw)
    if tag == GOOD_UPDATE:
        return GOOD_CHANGE_PSW
    return ERROR_CHANGE_PSW


def update_info(stu_id, stu_name=NO_INPUT, stu_school=NO_INPUT,
                stu_tel=NO_INPUT, stu_mail=NO_INPUT):
    tag = update(stu_id=stu_id,
                 stu_name=stu_name,
                 stu_school=stu_school,
                 stu_tel=stu_tel,
                 stu_mail=stu_mail)
    if tag == GOOD_UPDATE:
        return GOOD_UPDATE_INFO
    return ERROR_UPDATE_INFO


def get_info(stu_id):
    temp = select(stu_id=stu_id)
    if temp == ERROR_SELECT_DOESNOTEXIST:
        return ERROR_GET_INFO
    return temp





