import re


def get_file_type(file_name):
    file_type = re.split('\.', file_name)[-1]
    return file_type
