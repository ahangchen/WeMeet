from django.core.files.storage import default_storage
from django.core.files.base import ContentFile

from student.ctrl.tag import ERR_AVATAR_FILE_INVALID
from student.ctrl.tag import ERR_SAVE_AVATAR_FAIL
from student.ctrl.tag import OK_SAVE_AVATAR

from student.db import stu_info
from student.db.tag import ERR_SELECT_NOTEXIST
from student.db.tag import ERR_SELECT_DB
from student.db.tag import OK_UPDATE
from student.db.tag import ERR_UPDATE_NOTEXIST
from student.db.tag import ERR_UPDATE_DB

from student.util.logger import logger
from student.util import file_helper
import time


DEFAULT_AVATAR = 'student/avatar/default.jpg'
AVATAR_PATH_ROOT = 'student/avatar'


def save(stu_id, avatar):
    """
    保存头像
    @stu_id:学生id
    @avatar:头像文件
    成功：返回{'tag': OK_SAVE_AVATAR, 'path': ref_path}
    失败：返回{'tag': ERR_SAVE_AVATAR_FAIL}
          或{'tag': ERR_AVATAR_FILE_INVALID}
    """

    def check_avatar_file(file):  # TODO(hjf): Check avatar file
        """return true if avatar file is valid"""
        return True

    def get_avatar_path(folder, file_name, file_type):
        return '%s/%s/%s.%s' % (AVATAR_PATH_ROOT, folder, file_name, file_type)

    # 确认学生是否存在
    select_rlt = stu_info.select(stu_id=stu_id)
    # 如果账号不存在
    if select_rlt['tag'] == ERR_SELECT_NOTEXIST:
        logger.warning('尝试为不存在的学生上传头像')
        return {'tag': ERR_SAVE_AVATAR_FAIL}
    # 如果数据库异常导致查询学生是否存在失败
    elif select_rlt['tag'] == ERR_SELECT_DB:
        logger.error('数据库异常导致无法确定学生是否存在，上传头像失败')
        return {'tag': ERR_SAVE_AVATAR_FAIL}

    # 学生存在，如果头像合法
    pre_ref_path = select_rlt['stu'].avatar_path
    if check_avatar_file(avatar):
        # 写入文件的路径
        avatar_path = get_avatar_path(folder=stu_id,
                                      file_name=int(time.time()),
                                      file_type=file_helper.get_file_type(avatar.name))  # use time as avatar file name

        # 引用头像的路径
        ref_path = '/media/' + avatar_path
        # 更新学生头像路径
        update_tag = stu_info.update(stu_id=stu_id, avatar_path=ref_path)
        # 如果更新头像路径成功
        if update_tag == OK_UPDATE:
            # 如果头像保存成功
            if file_helper.save(avatar, avatar_path):
                return {'tag': OK_SAVE_AVATAR,
                        'path': ref_path}
            # 如果头像保存失败， 回滚
            else:
                roll_tag = stu_info.update(stu_id=stu_id, avatar_path=pre_ref_path)
                # 如果回滚失败
                if roll_tag != OK_UPDATE:
                    logger.error('头像保存失败，但数据库异常导致无法将已更新的头像路径恢复')
                return {'tag': ERR_SAVE_AVATAR_FAIL}

        # 如果写入路径失败
        else:
            return {'tag': ERR_SAVE_AVATAR_FAIL}
    # 如果头像不合法
    else:
        return {'tag': ERR_AVATAR_FILE_INVALID}


