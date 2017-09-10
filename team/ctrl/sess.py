import random
import hashlib


def login_token(uid, type):
    if type == 0:
        type_key = 's'
    else:
        type_key = 't'
    key = str(uid)
    for i in range(10):
        key += str(random.randint(0, 10))
    return type_key + hashlib.md5(key.encode()).hexdigest()


if __name__ == '__main__':
    print(login_token(1, 0))