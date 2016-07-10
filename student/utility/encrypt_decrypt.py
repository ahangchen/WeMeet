# 依赖PyCrypto2.6.1
from Crypto.Cipher import AES
from binascii import b2a_hex, a2b_hex
import base64


key = "This is a key123"  # 键
IV = "This is an IV456"  # 偏移量


def encrypt(msg):
    length = len(msg)
    num = length % 16
    msg = msg.ljust(length + 16 - num)  # 补充至16字节
    obj = AES.new(key, AES.MODE_CBC, IV)  # 新建AES加密器
    msg = b2a_hex(obj.encrypt(msg))  # 因为AES加密时候得到的字符串不一定是ascii字符集的，输出到终端或者保存时候可能存在问题
                                     # 所以这里统一转化为16进制
    msg = msg.decode()  # bytes转化为str
    return msg


def decrypt(msg):
    msg = a2b_hex(msg)  # 转化为16进制的逆过程
    obj = AES.new(key, AES.MODE_CBC, IV)  # 新建AES解密器
    msg = obj.decrypt(msg)  # 解密
    msg = msg.decode()  # bytes转化为str
    return msg
