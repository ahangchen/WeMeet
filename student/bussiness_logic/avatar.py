from django.core.files.storage import default_storage
from django.core.files.base import ContentFile

DEFAULT_AVATAR = 'student/avatar/default.jpg'
AVATAR_PATH_ROOT = 'student/avatar'


def check_avatar_file(file):  # TODO(hjf): Check avatar file
    """return true if avatar file is valid"""
    return True


def get_avatar_path(file_name, file_type):
    return '%s/%s.%s' % (AVATAR_PATH_ROOT, file_name, file_type)


def save_avatar(avatar, path):
    try:
        if default_storage.exists(path):
            default_storage.delete(path)
        default_storage.save(path, ContentFile(avatar.read()))
        return True
    except:
        return False


