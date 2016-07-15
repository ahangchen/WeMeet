# from student.utility.tag import NO_INPUT

# from student.data_access.tag import GOOD_UPDATE
# from student.data_access.tag import ERROR_SELECT_DOESNOTEXIST

# from student.bussiness_logic.avatar import check_avatar_file
# from student.bussiness_logic.avatar import get_avatar_path
# from student.bussiness_logic.avatar import save_avatar

# from student.bussiness_logic.tag import ERROR_AVATAR_FILE_INVALID
# from student.bussiness_logic.tag import ERROR_AVATAR_SAVE_FAILED
# from student.bussiness_logic.tag import GOOD_UPDATE_INFO
# from student.bussiness_logic.tag import ERROR_UPDATE_INFO
from student.bussiness_logic.tag import ERR_GET_INFO_NOTEXIST

# from student.data_access.stu_info import update
from student.data_access.stu_info import select

# from student.utility.file_helper import get_file_type

#
# def get(account):
#     """
#     获取学生信息
#      成功：返回学生
#      失败:返回ERROR_GET_INFO_DOESNOTEXIST
#     """
#     result = select(stu_id=account)
#     # 如果学生不存在
#     if result == ERROR_SELECT_DOESNOTEXIST:
#         return ERR_GET_INFO_NOTEXIST
#     # 如果获取学生信息成功
#     return result








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






