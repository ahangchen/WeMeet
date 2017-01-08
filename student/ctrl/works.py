from student.ctrl.tag import OK_GET_WORKS, ERR_GET_NO_WORKS, ERR_GET_WORKS_DB, \
                             OK_UPDATE_WORKS, ERR_UPDATE_WORKS_DB, \
                             OK_ADD_WORKS, ERR_ADD_WORKS_DB, \
                             OK_DEL_works, ERR_DEL_works_DB, ERR_ADD_WORKS_FULL, \
                             OK_SAVE_WORKS, ERR_SAVE_WORKS_FAIL, ERR_WORKS_FILE_INVALID

from student.util.logger import logger
from student.util import file_helper
from student.db import stu_info, works
import time


WORKS_PATH_ROOT = 'student/works'


def get(stu_id):
    """
    获取学生的作品集
    """
    select_rlt = stu_info.select(stu_id=stu_id)
    # 如果学生存在
    if select_rlt['tag'] == stu_info.OK_SELECT:
        filter_set = works.stu_filter(stu=select_rlt['stu'])

        # 如果该学生有合法的作品数量数量
        if filter_set.count() in range(1, 6):
            return {'tag': OK_GET_WORKS,
                    'works_list': list(filter_set.values())}

        # 如果该学生无作品
        elif filter_set.count() == 0:
            return {'tag': ERR_GET_NO_WORKS}
        # 如果该学生的作品数量不合法
        else:
            logger.error('学生id为%s的学生拥有不合法的作品数量，导致获取作品失败' % stu_id)
            return {'tag': ERR_GET_WORKS_DB}

    # 如果学生不存在
    elif select_rlt['tag'] == stu_info.ERR_SELECT_NOTEXIST:
        logger.warning('尝试获取不存在的学生的作品')
        return {'tag': ERR_GET_WORKS_DB}
    # 如果数据库异常导致无法确认学生是否存在(select_rlt['tag'] == ERR_SELECT_DB)
    else:
        logger.error('数据库异常导致无法确认学生是否存在，查询作品失败')
        return {'tag': ERR_GET_WORKS_DB}


def update(works_id, stu_id, name, duty, url, description, img, audio, video):
    """
    修改作品集信息
    成功：返回{'tag': OK_UPDATE_WORKS}
    失败：返回{'tag': ERR_UPDATE_WORKS_DB}
    """
    select_rlt = stu_info.select(stu_id=stu_id)
    # 如果学生存在
    if select_rlt['tag'] == stu_info.OK_SELECT:
        return {'tag': OK_UPDATE_WORKS} \
            if works.update(
                works_id, select_rlt['stu'], name, duty, url, description, img, audio, video
            ) == works.OK_UPDATE \
            else {'tag': ERR_UPDATE_WORKS_DB}

    # 如果学生不存在
    elif select_rlt['tag'] == stu_info.ERR_SELECT_NOTEXIST:
        logger.warning('尝试更新不存在的学生的作品集信息')
        return {'tag': ERR_UPDATE_WORKS_DB}
    # 如果数据库异常导致无法确认学生是否存在(select_rlt['tag'] == ERR_SELECT_DB)
    else:
        logger.error('数据库异常导致无法确认学生是否存在，修改作品集信息失败')
        return {'tag': ERR_UPDATE_WORKS_DB}


def add(stu_id, name, duty, url, description, img, audio, video):
    """
    增加作品集信息
    成功：返回{'tag': OK_ADD_WORKS, 'works_id': insert_rlt['works'].works_id}
    失败：返回{'tag': ERR_ADD_WORKS_DB}或{'tag': ERR_ADD_WORKS_FULL}
    """
    select_rlt = stu_info.select(stu_id=stu_id)
    # 如果学生存在
    if select_rlt['tag'] == stu_info.OK_SELECT:
        filter_set = works.stu_filter(stu=select_rlt['stu'])

        # 如果该学生有合法的作品数量数量
        if filter_set.count() < 6:
            insert_rlt = works.insert(name, duty, url, description, select_rlt['stu'], img, audio, video)
            if insert_rlt['tag'] == works.OK_INSERT:
                return {'tag': OK_ADD_WORKS, 'works_id': insert_rlt['works'].works_id}
            else:
                return {'tag': ERR_ADD_WORKS_FULL}

    # 如果学生记录不存在
    elif select_rlt['tag'] == stu_info.ERR_SELECT_NOTEXIST:
        logger.warning('尝试为不存在的学生增加作品集信息')
        return {'tag': ERR_ADD_WORKS_DB}
    # 如果数据库异常导致获取学生信息失败(select_rlt['tag'] == ERR_SELECT_DB)
    else:
        logger.error('数据库异常导致无法确认学生是否存在，增加作品集信息失败')
        return {'tag': ERR_ADD_WORKS_DB}


def delete(stu_id, works_id):
    """
    删除作品
    成功：返回{'tag': OK_DEL_WORKS}
    失败：返回{'tag': ERR_DEL_WORKS_DB}
    """
    select_rlt = stu_info.select(stu_id=stu_id)
    # 如果学生存在
    if select_rlt['tag'] == stu_info.OK_SELECT:
        delete_tag = works.delete(works_id, select_rlt['stu'])
        if delete_tag == works.OK_DELETE:
            return {'tag': OK_DEL_works}

        # delete_tag == ERR_DELETE_DB
        else:
            return {'tag': ERR_DEL_works_DB}

    # 如果学生不存在
    elif select_rlt['tag'] == stu_info.ERR_SELECT_NOTEXIST:
        logger.warning('尝试删除不存在的学生的技能评价')
        return {'tag': ERR_DEL_works_DB}

    # 如果数据库异常导致无法确认学生是否存在(select_rlt['tag'] == ERR_SELECT_DB)
    else:
        logger.error('数据库异常导致无法确认学生是否存在，删除技能评价失败')
        return {'tag': ERR_DEL_works_DB}


def upload(stu_id, works_file):
    """
    上传作品集文件
    @stu_id 学生id
    @works: 作品集文件
    成功：返回{'tag': OK_SAVE_WORKS, 'path': ref_path}
    失败：返回{'tag': ERR_SAVE_WORKS_FAIL}
    """

    def check_resume_file(file):  # TODO(hjf): Check works file
        """return true if works file is valid"""
        return True

    def get_works_path(folder, file_name, file_type):
        return '%s/%s/%s.%s' % (WORKS_PATH_ROOT, folder, file_name, file_type)

    # 确认学生是否存在
    select_rlt = stu_info.select(stu_id=stu_id)
    # 如果学生存在
    if select_rlt['tag'] == stu_info.OK_SELECT:
        # 如果作品集文件合法
        if check_resume_file(works_file):
            works_path = get_works_path(folder=stu_id,
                                        file_name=int(time.time()),
                                        file_type=file_helper.get_file_type(works_file.name))  # 用time作简历文件名称
            # ref_path = '/media/' + works_path
            ref_path = works_path

            # 如果作品集文件上传成功
            if file_helper.save(works_file, works_path):
                return {'tag': OK_SAVE_WORKS,
                        'path': ref_path}
            # 如果作品集文件上传失败，
            else:
                return {'tag': ERR_SAVE_WORKS_FAIL}

        # 如果作品集文件不合法
        else:
            return {'tag': ERR_WORKS_FILE_INVALID}

    # 如果学生不存在
    elif select_rlt['tag'] == stu_info.ERR_SELECT_NOTEXIST:
        logger.warning('尝试为不存在的学生上传作品集')
        return {'tag': ERR_SAVE_WORKS_FAIL}
    # 如果数据库异常导致查询学生是否存在失败(select_rlt['tag'] == ERR_SELECT_DB)
    else:
        logger.error('数据库异常导致无法确定学生是否存在，上传作品集失败')
        return {'tag': ERR_SAVE_WORKS_FAIL}
