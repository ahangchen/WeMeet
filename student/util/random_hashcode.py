import random
import string
import hashlib


def get_hashcode(length=8):
    """
    获取随机字符串的hash值（md5)
    @length: 随机字符串的长度
    返回: 随机字符串的hash值（md5)
    """
    a = list(string.ascii_letters)
    random.shuffle(a)
    random_string = ''.join(a[:length]).encode('utf-8')
    return hashlib.md5(random_string).hexdigest()
