# from student.utility.tag import NO_INPUT

from student.db import stu_info, account, edu
from student.db.tag import OK_SELECT
from student.db.tag import ERR_SELECT_NOTEXIST
from student.db.tag import ERR_SELECT_DB
from student.db.tag import OK_UPDATE
from student.db.tag import ERR_UPDATE_DB
from student.db.tag import ERR_UPDATE_NOTEXIST
from student.db.tag import OK_INSERT

from student.ctrl.tag import ERR_GET_INFO_NOTEXIST
from student.ctrl.tag import ERR_GET_INFO_DB
from student.ctrl.tag import OK_UPDATE_STU_INFO
from student.ctrl.tag import ERR_UPDATE_STU_INFO_DB
from student.ctrl.tag import OK_ADD_EDU
from student.ctrl.tag import ERR_ADD_EDU_FULL
from student.ctrl.tag import ERR_ADD_EDU_DB
from student.ctrl.tag import OK_GET_EDU
from student.ctrl.tag import ERR_GET_EDU_NO_EDU
from student.ctrl.tag import ERR_GET_EDU_DB

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


def add_edu(stu_id, major, graduation_year, background, school):
    """
    增加教育经历
    成功：返回{'tag': OK_ADD_EDU, 'edu_id': insert_rlt['edu'].id}
    失败：返回{'tag': ERR_ADD_EDU_FULL}
           或{'tag': ERR_ADD_EDU_DB}
    @stu_id: 学生id
    @major: 专业
    @graduation_year: 毕业年份
    @background: 学历
    @school: 学校
    """
    select_rlt = stu_info.select(stu_id=stu_id)
    # 如果学生存在
    if select_rlt['tag'] == OK_SELECT:
        # 如果教育经历未达五条
        if edu.stu_filter(stu=select_rlt['stu']).count() < 5:
            insert_rlt = edu.insert(major=major, graduation_year=graduation_year,
                                    background=background, school=school, stu=select_rlt['stu'])
            # 如果插入成功：
            if insert_rlt['tag'] == OK_INSERT:
                return {'tag': OK_ADD_EDU,
                        'edu_id': insert_rlt['edu'].id}
            # 如果插入失败（insert_rlt['tag'] == ERR_INSERT_DB）
            else:
                return {'tag': ERR_ADD_EDU_DB}

        # 如果教育经历已有五条或更多
        else:
            return {'tag': ERR_ADD_EDU_FULL}

    # 如果学生记录不存在
    elif select_rlt['tag'] == ERR_SELECT_NOTEXIST:
        logger.warning('尝试为不存在的学生增加教育经历')
        return {'tag': ERR_ADD_EDU_DB}
    # 如果数据库异常导致获取学生信息失败(select_rlt['tag'] == ERR_SELECT_DB)
    else:
        logger.error('数据库异常导致无法确认学生是否存在，增加教育经历失败')
        return {'tag': ERR_ADD_EDU_DB}


def get_edu(stu_id):
    """
    获取学生的教育经历
    成功：返回{'tag': OK_GET_EDU, 'grade': latest_year, 'major': major, 'edu_list': edu_list}
                     edu_list: [{'edu_id': edu_rcd.id,
                                 'major': edu_rcd.major,
                                 'graduation_year': edu_rcd.graduation_year,
                                 'edu_background': edu_rcd.background,
                                 'school': edu_rcd.school}]
    失败：返回{'tag': ERR_GET_EDU_NO_EDU}
          或{'tag': ERR_GET_EDU_DB}
    """
    select_rlt = stu_info.select(stu_id=stu_id)
    # 如果学生存在
    if select_rlt['tag'] == OK_SELECT:
        filter_set = edu.stu_filter(stu=select_rlt['stu'])

        # 如果该学生有合法的教育经历数量
        if filter_set.count() in range(1, 6):
            edu_list = []
            latest_year = -1
            major = ''
            for edu_rcd in filter_set:
                if edu_rcd.graduation_year >= latest_year:
                    latest_year = edu_rcd.graduation_year
                    major = edu_rcd.major
                edu_list.append({'edu_id': edu_rcd.id,
                                 'major': edu_rcd.major,
                                 'graduation_year': edu_rcd.graduation_year,
                                 'edu_background': edu_rcd.background,
                                 'school': edu_rcd.school})
            return {'tag': OK_GET_EDU,
                    'grade': latest_year,
                    'major': major,
                    'edu_list': edu_list}

        # 如果该学生无教育经历
        elif filter_set.count() == 0:
            return {'tag': ERR_GET_EDU_NO_EDU}
        # 如果该学生的教育经历数量不合法
        else:
            logger.error('学生id为%s的学生拥有不合法的教育经历数量，导致获取教育经历失败' % stu_id)
            return {'tag': ERR_GET_EDU_DB}

    # 如果学生不存在
    elif select_rlt['tag'] == ERR_SELECT_NOTEXIST:
        logger.warning('尝试获取不存在的学生的教育经历')
        return {'tag': ERR_GET_EDU_DB}
    # 如果数据库异常导致无法确认学生是否存在(select_rlt['tag'] == ERR_SELECT_DB)
    else:
        logger.error('数据库异常导致无法确认学生是否存在，查询教育经历失败')
        return {'tag': ERR_GET_EDU_DB}




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






