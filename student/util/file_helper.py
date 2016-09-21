from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from student.util.logger import logger
import re


def get_file_type(file_name):
    file_type = re.split('\.', file_name)[-1]
    return file_type


def save(file, path):
    if default_storage.exists(path):
        try:
            default_storage.delete(path)
        # 如果目标文件系统不支持删除文件操作
        except NotImplementedError as err:
            logger.error('目标文件系统不支持删除文件操作')
            return False
    default_storage.save(path, ContentFile(file.read()))
    return True


def delete(path):
    if default_storage.exists(path) and path != '':
        try:
            default_storage.delete(path)
        # 如果目标文件系统不支持删除文件操作
        except NotImplementedError as err:
            logger.error('目标文件系统不支持删除文件操作')
            return False
    return True