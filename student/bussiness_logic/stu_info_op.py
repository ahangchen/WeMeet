from student.utility.tag import NO_INPUT

from student.data_access.tag import GOOD_INSERT
from student.data_access.tag import GOOD_UPDATE
from student.data_access.tag import ERROR_SELECT_DOESNOTEXIST

from student.bussiness_logic.avatar import check_avatar_file
from student.bussiness_logic.avatar import DEFAULT_AVATAR
from student.bussiness_logic.avatar import get_avatar_path
from student.bussiness_logic.avatar import save_avatar

from student.bussiness_logic.tag import ERROR_AVATAR_FILE_INVALID
from student.bussiness_logic.tag import ERROR_AVATAR_SAVE_FAILED
from student.bussiness_logic.tag import GOOD_REGISTER
from student.bussiness_logic.tag import ERROR_REGISTER
from student.bussiness_logic.tag import GOOD_CHANGE_PWD
from student.bussiness_logic.tag import ERROR_CHANGE_PWD
from student.bussiness_logic.tag import GOOD_UPDATE_INFO
from student.bussiness_logic.tag import ERROR_UPDATE_INFO
from student.bussiness_logic.tag import ERROR_GET_INFO

from student.data_access.stu_info import insert
from student.data_access.stu_info import update
from student.data_access.stu_info import select

from student.utility.bussiness_logic import get_file_type


def register(stu_id, pwd):
    tag = insert(stu_id=stu_id, pwd=pwd, name='', school='', tel='', mail='', avatar_path=DEFAULT_AVATAR)
    if tag == GOOD_INSERT:
        return GOOD_REGISTER
    return ERROR_REGISTER


def change_pwd(stu_id, pwd):
    tag = update(stu_id=stu_id, pwd=pwd)
    if tag == GOOD_UPDATE:
        return GOOD_CHANGE_PWD
    return ERROR_CHANGE_PWD


def update_info(stu_id, name=NO_INPUT, school=NO_INPUT, tel=NO_INPUT, mail=NO_INPUT, avatar=NO_INPUT):
    if get_info(stu_id) != ERROR_SELECT_DOESNOTEXIST:
        if avatar != NO_INPUT:
            if check_avatar_file(avatar):
                avatar_path = get_avatar_path(file_name=stu_id,
                                              file_type=get_file_type(avatar.name))  # use stu_id as avatar file name

                if not save_avatar(avatar, avatar_path):  # if failed to save avatar
                    return ERROR_AVATAR_SAVE_FAILED

            else:  # if avatar file is invalid
                return ERROR_AVATAR_FILE_INVALID

    # if avatar == NO_INPUT or stu_id exists
    avatar_path = NO_INPUT

    tag = update(stu_id=stu_id,
                 name=name,
                 school=school,
                 tel=tel,
                 mail=mail,
                 avatar_path=avatar_path)
    if tag == GOOD_UPDATE:
        return GOOD_UPDATE_INFO
    return ERROR_UPDATE_INFO


def get_info(stu_id):
    result = select(stu_id=stu_id)
    if result == ERROR_SELECT_DOESNOTEXIST:
        return ERROR_GET_INFO
    return result  # succeed select





