# from student.utility.tag import NO_INPUT

from student.db import stu_info, account
from student.db.tag import OK_SELECT
from student.db.tag import ERR_SELECT_NOTEXIST
from student.db.tag import ERR_SELECT_DB
from student.db.tag import OK_UPDATE
from student.db.tag import ERR_UPDATE_DB
from student.db.tag import ERR_UPDATE_NOTEXIST

# from student.ctrl.avatar import check_avatar_file
# from student.ctrl.avatar import get_avatar_path
# from student.ctrl.avatar import save_avatar

# from student.ctrl.tag import ERROR_AVATAR_FILE_INVALID
# from student.ctrl.tag import ERROR_AVATAR_SAVE_FAILED
# from student.ctrl.tag import GOOD_UPDATE_INFO
# from student.ctrl.tag import ERROR_UPDATE_INFO
from student.ctrl.tag import ERR_GET_INFO_NOTEXIST
from student.ctrl.tag import ERR_GET_INFO_DB
from student.ctrl.tag import OK_UPDATE_STU_INFO
from student.ctrl.tag import ERR_UPDATE_STU_INFO_DB

# from student.db.stu_info import update

from student.util.file_helper import get_file_type
from student.util.logger import logger


def get(stu_id):
    """
    获取学生信息
     成功：返回学生
     失败:返回ERR_GET_INFO_NOTEXIST
           或ERR_GET_INFO_DB
    """
    select_rlt = stu_info.select(stu_id=stu_id)
    # 如果学生存在
    if select_rlt['tag'] == OK_SELECT:
        return select_rlt['stu']
    # 如果学生记录不存在
    elif select_rlt['tag'] == ERR_SELECT_NOTEXIST:
        logger.error('学生不存在，获取学生信息失败')
        return ERR_GET_INFO_NOTEXIST
    # 如果数据库异常导致获取学生信息失败(select_rlt['tag'] == ERR_SELECT_DB)
    else:
        logger.error('数据库异常导致获取学生信息失败')
        return ERR_GET_INFO_DB


def update(stu_id, avatar_path, name, school, major, location, edu_background, grade, mail, tel):
    """
    更新学生信息
    成功：返回OK_UPDATE_INFO
    失败：返回ERR_UPDATE_DB
    @stu_id: 学生id
    @avatar_path: 头像路径
    @name: 姓名
    @school: 学校
    @major: 专业
    @location: 所在地
    @edu_background: 学历
    @grade: 年级
    @mail: 邮箱
    @tel: 联系方式
    """

    stu_update_tag = stu_info.update(stu_id=stu_id,
                                     avatar_path=avatar_path,
                                     name=name,
                                     school=school,
                                     major=major,
                                     location=location,
                                     edu_background=edu_background,
                                     grade=grade,
                                     mail=mail,
                                     tel=tel)

    # 如果学生信息更新成功
    if stu_update_tag == OK_UPDATE:

        # *******************************************************************************
        # 更改邮箱会更改账号 # TODO(hjf):完善更改邮箱会更改账号
        # acnt_update_tag = account.stu_update(stu_id=stu_id, account=mail)
        # if acnt_update_tag == ERR_UPDATE_NOTEXIST:
        #     logger.error('学生存在，但账号不存在，已更新学生信息，但账号信息无法更新，不做回滚')
        #     return ERR_UPDATE_DB
        # elif acnt_update_tag == ERR_UPDATE_DB:
        #     logger.error('更新学生邮箱时，数据库异常导致无法更新账号信息')
        #     return ERR_UPDATE_DB
        # *******************************************************************************

        return OK_UPDATE_STU_INFO
    elif stu_update_tag == ERR_UPDATE_NOTEXIST:
        logger.error('学生不存在，无法更新学生信息')
        return ERR_UPDATE_STU_INFO_DB
    # 如果stu_update_tag == ERR_UPDATE_DB
    else:
        logger.error('数据库异常导致更新学生信息失败')
        return ERR_UPDATE_DB







# def update_info(stu_id, name=NO_INPUT, school=NO_INPUT, tel=NO_INPUT, mail=NO_INPUT, avatar=NO_INPUT):
#     if get(stu_id) != ERROR_SELECT_DOESNOTEXIST:
#         if avatar != NO_INPUT:
#             if check_avatar_file(avatar):
#                 avatar_path = get_avatar_path(file_name=stu_id,
#                                               file_type=get_file_type(avatar.name))  # use stu_id as avatar file name
#
#                 if not save_avatar(avatar, avatar_path):  # if failed to save avatar
#                     return ERROR_AVATAR_SAVE_FAILED
#
#             else:  # if avatar file is invalid
#                 return ERROR_AVATAR_FILE_INVALID
#
#     # if avatar == NO_INPUT or stu_id exists
#     avatar_path = NO_INPUT
#
#     tag = update(stu_id=stu_id,
#                  name=name,
#                  school=school,
#                  tel=tel,
#                  mail=mail,
#                  avatar_path=avatar_path,)
#     if tag == GOOD_UPDATE:
#         return GOOD_UPDATE_INFO
#     return ERROR_UPDATE_INFO






