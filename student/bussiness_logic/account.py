from student.data_access.tag import GOOD_INSERT
from student.data_access.tag import GOOD_UPDATE
from student.data_access.tag import ERROR_UPDATE_DOESNOTEXIST
from student.data_access.tag import ERROR_SELECT_DOESNOTEXIST

from student.bussiness_logic.avatar import DEFAULT_AVATAR

from student.bussiness_logic.tag import GOOD_REGISTER
from student.bussiness_logic.tag import ERROR_REGISTER
from student.bussiness_logic.tag import GOOD_ACTIVATE
from student.bussiness_logic.tag import ERROR_ACTIVATE_DOESNOTEXIST
from student.bussiness_logic.tag import GOOD_LOGIN
from student.bussiness_logic.tag import ERROR_LOGIN_DOESNOTEXIST
from student.bussiness_logic.tag import ERROR_LOGIN_NONACTIVATED
from student.bussiness_logic.tag import ERROR_LOGIN_WRONG_PWD
from student.bussiness_logic.tag import GOOD_CHANGE_PWD
from student.bussiness_logic.tag import ERROR_CHANGE_PWD_DOESNOTEXIST
from student.bussiness_logic.tag import ERROR_CHANGE_PWD_WRONG_CREDENTIAL
from student.bussiness_logic.tag import ERROR_RESET_DOESNOTEXIST
from student.bussiness_logic.tag import GOOD_RESET_MAIL
from student.bussiness_logic.tag import ERROR_RESET_MAIL_DOESNOTEXIST


from student.bussiness_logic import verify_mail
from student.bussiness_logic import reset_mail

from student.data_access.stu_info import insert
from student.data_access.stu_info import update
from student.data_access.stu_info import select

from student.utility.encrypt_decrypt import decrypt
from student.utility.random_hashcode import get_hashcode

from django.core.mail import send_mail


def register(account, pwd):
    """
    注册
    成功：返回GOOD_REGISTER
    失败：返回ERROR_REGISTER
    """
    tag = insert(stu_id=account, pwd=pwd, name='', school='',
                 tel='', mail='', avatar_path=DEFAULT_AVATAR)
    if tag == GOOD_INSERT:
        send_mail('WeMeet注册验证邮件', verify_mail.get_content(stu_id=account),  # TODO(hjf): 修改邮件内容、收发邮箱
                  'm18826076291@sina.com', ['961437466@qq.com'])
        return GOOD_REGISTER
    # 当tag是ERROR_INSERT的时候
    return ERROR_REGISTER


def activate(account_cipher):
    """
    激活账号
    成功：返回GOOD_ACTIVATE
    失败：返回ERROR_ACTIVATE_DOESNOTEXIST
    @account_cipher:  加密后的account
    """
    account = decrypt(account_cipher)
    # 如果账号不存在
    if select(stu_id=account) == ERROR_SELECT_DOESNOTEXIST:
        return ERROR_ACTIVATE_DOESNOTEXIST
    tag = update(stu_id=account, is_activated=True)
    # 如果更新激活状态失败（账号不存在）
    if tag == ERROR_UPDATE_DOESNOTEXIST:
        return ERROR_ACTIVATE_DOESNOTEXIST
    # 如果更新激活状态成功
    return GOOD_ACTIVATE


def login(account, pwd):
    """
    登陆
    成功：返回GOOD_LOGIN
    失败：返回ERROR_LOGIN_DOESNOTEXIST或ERROR_LOGIN_WRONG_PWD
    @account: 账号（邮箱）
    @pwd: 密码
    """
    obj = select(stu_id=account)
    # 如果账号不存在
    if obj == ERROR_SELECT_DOESNOTEXIST:
        return ERROR_LOGIN_DOESNOTEXIST
    elif not obj.is_activated:
        return ERROR_LOGIN_NONACTIVATED
    # 账号（stu_id）存在, 如果密码错误
    elif obj.pwd != pwd:
        return ERROR_LOGIN_WRONG_PWD
    # 登陆成功
    else:
        return GOOD_LOGIN


def send_reset_mail(account):
    """
    发送密码重置邮件
    成功：发送重置邮件并返回GOOD_RESTE_MAIL
    失败：返回ERROR_RESET_MAIL_DOESNOTEXIST
    @account: 账号（邮箱）
    """
    # 如果账号不存在
    if select(stu_id=account) == ERROR_SELECT_DOESNOTEXIST:
        return ERROR_RESET_MAIL_DOESNOTEXIST
    # 如果账号存在，发送邮件
    send_mail('WeMeet重置密码邮件', reset_mail.get_content(stu_id=account),  # TODO(hjf): 修改邮件内容、收发邮箱
              'm18826076291@sina.com', ['961437466@qq.com'])
    return GOOD_RESET_MAIL


def reset(account_cipher):
    """
    重置账号，修改账号状态为未激活，修改密码为随机字符串的哈希值
    @account_cipher: 由后端加密的account，只能通过邮件获得
    成功：返回{'credential': credential, 'account': stu_id}
    失败：返回ERROR_RESET_DOESNOTEXIST
    """
    account = decrypt(account_cipher)
    # 如果账号不存在
    obj = select(stu_id=account)
    if obj == ERROR_SELECT_DOESNOTEXIST:
        return ERROR_RESET_DOESNOTEXIST
    # 如果账号存在，重置状态和密码
    credential = get_hashcode()
    update(stu_id=account, is_activated=False, pwd=credential)
    return {'credential': credential, 'account': account}  # 防止credential(哈希值）和ERROR_RESET_DOESNOTEXIST冲突


def change_pwd(account, credential, pwd):
    """
    验证凭据激活账号修改密码
    成功：激活账号，修改密码， 返回GOOD_CHANGE_PWD
    失败：返回ERROR_CHANGE_PWD_DOESNOTEXIST
          或ERROR_CHANGE_PWD_WRONG_CREDENTIAL
    """
    obj = select(stu_id=account)
    # 如果账号不存在
    if obj == ERROR_SELECT_DOESNOTEXIST:
        return ERROR_CHANGE_PWD_DOESNOTEXIST
    # 账号存在，如果凭据错误
    elif obj.pwd != credential:
        return ERROR_CHANGE_PWD_WRONG_CREDENTIAL
    # 如果账号存在，凭据正确，激活账号，并修改密码
    else:
        tag = update(stu_id=account, is_activated=True, pwd=pwd)
        # 如果账号不存在
        if tag == ERROR_UPDATE_DOESNOTEXIST:
            return ERROR_CHANGE_PWD_DOESNOTEXIST
        # 如果更新成功(tag == GOOD_UPDATE)
        else:
            return GOOD_CHANGE_PWD



