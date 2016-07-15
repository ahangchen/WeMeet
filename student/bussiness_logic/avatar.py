from django.core.files.storage import default_storage
from django.core.files.base import ContentFile

from student.utility.logger import logger


DEFAULT_AVATAR = 'student/avatar/default.jpg'
AVATAR_PATH_ROOT = 'student/avatar'


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


