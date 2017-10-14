import random
import hashlib

from student.models import WMToken


def login_token(uid, u_type):
    if u_type == 0:
        type_key = 's'
    else:
        type_key = 't'
    key = str(uid)
    for i in range(10):
        key += str(random.randint(0, 10))
    return type_key + hashlib.md5(key.encode()).hexdigest()


def has_login(uid, u_type, token):
    login_rst = WMToken.objects.filter(uid=uid, u_type=u_type, token=token).count()
    return login_rst > 0


def gen_token(uid, u_type):
    token = login_token(uid, u_type)
    WMToken.objects.update_or_create(uid=uid, u_type=u_type, token=token)
    return token


if __name__ == '__main__':
    print(login_token(1, 0))