from django.core.files.storage import default_storage
from django.core.files.base import ContentFile

from student.bussiness_logic.tag import ERR_AVATAR_FILE_INVALID
from student.bussiness_logic.tag import ERR_SAVE_AVATAR_FAIL
from student.bussiness_logic.tag import OK_SAVE_AVATAR

from student.data_access import stu_info
from student.data_access.tag import ERR_SELECT_NOTEXIST
from student.data_access.tag import ERR_SELECT_DB

from student.utility.logger import logger
from student.utility.file_helper import get_file_type


DEFAULT_AVATAR = 'student/avatar/default.jpg'
AVATAR_PATH_ROOT = 'student/avatar'


def save(stu_id, avatar):
    """
    保存头像
    @stu_id:学生id
    @avatar:头像文件
    成功：返回{'tag': OK_SAVE_AVATAR, 'path': avatar_path}
    失败：返回{'tag': ERR_SAVE_AVATAR_FAIL}
          或{'tag': ERR_AVATAR_FILE_INVALID}
    """

    def check_avatar_file(file):  # TODO(hjf): Check avatar file
        """return true if avatar file is valid"""
        return True

    def get_avatar_path(file_name, file_type):
        return '%s/%s.%s' % (AVATAR_PATH_ROOT, file_name, file_type)

    def save_avatar(avatar, path):
        if default_storage.exists(path):
            try:
                default_storage.delete(path)
            # 如果目标文件系统不支持删除文件操作
            except NotImplementedError as err:
                logger.error('目标文件系统不支持删除文件操作')
                return False
        default_storage.save(path, ContentFile(avatar.read()))
        return True

    # 确认学生是否存在
    select_tag = stu_info.select(stu_id=stu_id)
    # 如果账号不存在
    if select_tag == ERR_SELECT_NOTEXIST:
        logger.warning('尝试为不存在的学生上传头像')
        return {'tag': ERR_SAVE_AVATAR_FAIL}
    # 如果数据库异常导致查询学生是否存在失败
    elif select_tag == ERR_SELECT_DB:
        logger.error('数据库异常导致无法确定学生是否存在，上传头像失败')
        return {'tag': ERR_SAVE_AVATAR_FAIL}

    # 学生存在，如果头像合法
    if check_avatar_file(avatar):
        avatar_path = get_avatar_path(file_name=stu_id,
                                      file_type=get_file_type(avatar.name))  # use stu_id as avatar file name

        # 如果头像保存成功
        if save_avatar(avatar, avatar_path):
            return {'tag': OK_SAVE_AVATAR,
                    'path': avatar_path}
        # 如果头像保存失败
        else:
            return {'tag': ERR_SAVE_AVATAR_FAIL}

    # 如果头像不合法
    else:
        return {'tag': ERR_AVATAR_FILE_INVALID}


