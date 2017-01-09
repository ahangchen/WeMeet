# -- coding: utf-8 --
from student.db.tag import OK_UPDATE
from student.db.tag import ERR_INSERT_DB
from student.db.tag import ERR_UPDATE_NOTEXIST
from student.db.tag import ERR_SELECT_NOTEXIST
from student.db.tag import ERR_SELECT_DB
from student.db.tag import ERR_DELETE_DB
from student.db.tag import ERR_UPDATE_DB

from student.ctrl.avatar import DEFAULT_AVATAR

from student.ctrl.tag import OK_REG
from student.ctrl.tag import REG_FAIL_DB
from student.ctrl.tag import REG_FAIL_EXIST
from student.ctrl.tag import OK_ACTIVATE
from student.ctrl.tag import ERR_ACTIVATE_DB
from student.ctrl.tag import ERR_ACTIVATE_NOTEXIST
from student.ctrl.tag import OK_LOGIN
from student.ctrl.tag import ERR_LOGIN_NOTEXIST
from student.ctrl.tag import ERR_LOGIN_DB
from student.ctrl.tag import ERR_LOGIN_NONACTIVATED
from student.ctrl.tag import ERR_LOGIN_WRONG_PWD
from student.ctrl.tag import OK_CHANGE_PWD
from student.ctrl.tag import ERR_CHANGE_PWD_DB
from student.ctrl.tag import ERR_CHANGE_PWD_NOTEXIST
from student.ctrl.tag import ERR_CHANGE_PWD_WRONG_CREDENTIAL
from student.ctrl.tag import ERR_RESET_DB
from student.ctrl.tag import ERR_RESET_NOTEXIST
from student.ctrl.tag import ERR_RESET_OUT_DATE
from student.ctrl.tag import OK_RESET_MAIL
from student.ctrl.tag import ERR_RESET_MAIL_NOTEXIST
from student.ctrl.tag import ERR_RESET_MAIL_DB


from student.ctrl import verify_mail
from student.ctrl import reset_mail

from student.db.stu_info import insert
from student.db.stu_info import update
from student.db import account
from student.db import stu_info

from student.util.encrypt_decrypt import decrypt, encrypt
from student.util.mail_helper import send_163_mail
from student.util.random_hashcode import get_hashcode
from student.util.logger import logger
from student.util import date_helper


from django.core.mail import send_mail

from team.util.data import random6


def invite(acnt):
    pwd = str(random6())
    exist = account.acnt_select(account=acnt)

    # 如果数据库异常导致无法查询账号是否存在
    if exist['tag'] == ERR_SELECT_DB:
        logger.error('数据库异常导致无法查询账号是否存在，导致注册失败')
        return REG_FAIL_DB, -1

    # 如果账号已存在
    elif exist['tag'] != ERR_SELECT_NOTEXIST:
        return REG_FAIL_EXIST, -1

    # 如果账号尚未被注册
    stu_tag = stu_info.insert(name='', title='', personal_signature='', sex=0, school='',  grade=-1,
                              avatar_path=DEFAULT_AVATAR, label=-1)

    # 如果插入学生失败
    if stu_tag == ERR_INSERT_DB:
        logger.error('数据库异常导致插入学生失败，注册失败')
        return REG_FAIL_DB, -1

    # 如果插入学生成功
    else:
        acnt_tag = account.insert(account=acnt, pwd=pwd, stu=stu_tag)
        # 如果插入账号失败
        if acnt_tag == ERR_INSERT_DB:
            logger.error('数据库异常导致插入账号失败，注册失败')
            delete_tag = stu_info.delete(stu_tag.id)

            if delete_tag == ERR_DELETE_DB:
                logger.error('注册失败，数据库异常导致无法回滚状态（无法删除已插入的学生）')
            return REG_FAIL_DB, -1

        # 如果插入账号成功
        else:
            # 记录账号密文
            ciphertext = encrypt(acnt)
            update_tag = account.update(account=acnt, ciphertext=ciphertext)
            # 如果记录密文失败
            if update_tag != OK_UPDATE:
                logger.error('记录账号密文失败，注册失败')

                # 记录密文失败，回滚，删除已插入的账号
                delete_acnt_tag = account.delete(account=acnt)
                if delete_acnt_tag == ERR_DELETE_DB:
                    logger.error('注册失败，数据库异常导致无法回滚状态（无法删除已插入的账号）')

                # 删除已插入的学生
                delete_stu_tag = stu_info.delete(stu_tag.id)
                if delete_stu_tag == ERR_DELETE_DB:
                    logger.error('注册失败，数据库异常导致无法回滚状态（无法删除已插入的学生）')

                return ERR_UPDATE_DB, -1

            # 记录账号密文成功
            else:
                send_163_mail('13660106752', 'xuegongban118', '13660106752@163.com', acnt, 'WeMeet注册验证邮件',
                              verify_mail.get_content(ciphertext) + "\npwd: " + pwd)
                # send_mail('WeMeet注册验证邮件', verify_mail.get_content(ciphertext) + "\npwd: " + pwd,
                #           'm18826076291@sina.com', [acnt])
                return OK_REG, acnt_tag.stu_id


def register(acnt, pwd):
    """
    注册
    成功：返回OK_REG
    失败：返回REG_FAIL_EXIST(账号已存在）
            或REG_FAIL_DB
    """
    exist = account.acnt_select(account=acnt)

    # 如果数据库异常导致无法查询账号是否存在
    if exist['tag'] == ERR_SELECT_DB:
        logger.error('数据库异常导致无法查询账号是否存在，导致注册失败')
        return REG_FAIL_DB

    # 如果账号已存在
    elif exist['tag'] != ERR_SELECT_NOTEXIST:
        return REG_FAIL_EXIST

    # 如果账号尚未被注册
    stu_tag = stu_info.insert(name='', title='', personal_signature='',
                              sex=-1, school='',
                              grade=-1, avatar_path=DEFAULT_AVATAR, label=-1)

    # 如果插入学生失败
    if stu_tag == ERR_INSERT_DB:
        logger.error('数据库异常导致插入学生失败，注册失败')
        return REG_FAIL_DB

    # 如果插入学生成功
    else:
        acnt_tag = account.insert(account=acnt, pwd=pwd, stu=stu_tag)
        # 如果插入账号失败
        if acnt_tag == ERR_INSERT_DB:
            logger.error('数据库异常导致插入账号失败，注册失败')
            delete_tag = stu_info.delete(stu_tag.id)

            if delete_tag == ERR_DELETE_DB:
                logger.error('注册失败，数据库异常导致无法回滚状态（无法删除已插入的学生）')
            return REG_FAIL_DB

        # 如果插入账号成功
        else:
            # 记录账号密文
            ciphertext = encrypt(acnt)
            update_tag = account.update(account=acnt, ciphertext=ciphertext)
            # 如果记录密文失败
            if update_tag != OK_UPDATE:
                logger.error('记录账号密文失败，注册失败')

                # 记录密文失败，回滚，删除已插入的账号
                delete_acnt_tag = account.delete(account=acnt)
                if delete_acnt_tag == ERR_DELETE_DB:
                    logger.error('注册失败，数据库异常导致无法回滚状态（无法删除已插入的账号）')

                # 删除已插入的学生
                delete_stu_tag = stu_info.delete(stu_tag.id)
                if delete_stu_tag == ERR_DELETE_DB:
                    logger.error('注册失败，数据库异常导致无法回滚状态（无法删除已插入的学生）')

                return ERR_UPDATE_DB

            # 记录账号密文成功
            else:
                send_163_mail('13660106752', 'xuegongban118', '13660106752@163.com', acnt, 'WeMeet注册验证邮件',
                              verify_mail.get_content(ciphertext))
                return OK_REG


def activate(account_cipher):
    """
    激活账号
    成功：返回OK_ACTIVATE
    失败：返回ERR_ACTIVATE_NOTEXIST
          或ERR_ACTIVATE_DB
    @account_cipher:  加密后的account
    """
    select_rlt = account.ciphertext_select(ciphertext=account_cipher)
    if select_rlt['tag'] == ERR_SELECT_NOTEXIST:
        logger.warning('尝试激活不存在的账号')
        return ERR_ACTIVATE_NOTEXIST
    elif select_rlt['tag'] == ERR_SELECT_DB:
        logger.error('数据库异常导致无法激活账号')
        return ERR_ACTIVATE_DB

    tag = account.update(account=select_rlt['acnt'].account, is_activated=True)

    # 如果更新激活状态失败（账号不存在）
    if tag == ERR_UPDATE_NOTEXIST:
        logger.error('在激活账号过程中，账号记录丢失，激活失败')
        return ERR_ACTIVATE_DB

    # 如果更新激活状态失败（数据库异常）
    elif tag == ERR_UPDATE_DB:
        logger.error('数据库异常导致无法激活账号')
        return ERR_ACTIVATE_DB

    # 如果更新激活状态成功
    return OK_ACTIVATE


def login(acnt, pwd):
    """
    登陆
    成功：返回OK_LOGIN和学生id
    失败：返回ERR_LOGIN_NOTEXIST
            或ERR_LOGIN_DB
            或ERR_LOGIN_WRONG_PWD
            或ERR_LOGIN_NONACTIVATED

    @account: 账号（邮箱）
    @pwd: 密码
    """
    rlt = account.acnt_select(account=acnt)

    # 如果账号不存在
    if rlt['tag'] == ERR_SELECT_NOTEXIST:
        return {'tag': ERR_LOGIN_NOTEXIST}

    # 如果数据库异常
    elif rlt['tag'] == ERR_SELECT_DB:
        logger.error('数据库异常导致登陆失败')
        return {'tag': ERR_LOGIN_DB}

    # 如果账号未激活
    elif not rlt['acnt'].is_activated:
        return {'tag': ERR_LOGIN_NONACTIVATED}

    # 如果密码错误
    elif rlt['acnt'].pwd != pwd:
        return {'tag': ERR_LOGIN_WRONG_PWD}

    # 登陆成功
    else:
        return {'tag': OK_LOGIN,
                'stu_id': rlt['acnt'].stu.id}


def send_reset_mail(acnt):
    """
    发送密码重置邮件，记录链接发送的时间
    成功：发送重置邮件并返回OK_RESTE_MAIL
    失败：返回ERR_RESET_MAIL_NOTEXIST
    　　　　或ERR_RESET_MAIL_DB
    @account: 账号（邮箱）
    """

    select_rlt = account.acnt_select(account=acnt)
    # 如果账号不存在
    if select_rlt['tag'] == ERR_SELECT_NOTEXIST:
        logger.warning('尝试发送重置邮件到不存在的账号')
        return ERR_RESET_MAIL_NOTEXIST
    # 如果数据异常无法查询
    elif select_rlt['tag'] == ERR_SELECT_DB:
        logger.error('数据库异常导致无法发送重置邮件')
        return ERR_RESET_MAIL_DB

    # 账号密文
    ciphertext = encrypt(acnt)
    # 如果账号存在，记录邮件发送的日期和账号密文，并发送邮件
    update_tag = account.update(account=acnt, reset_date=date_helper.now(), ciphertext=ciphertext)

    # 如果记录日期时，账号记录丢失
    if update_tag == ERR_UPDATE_NOTEXIST:
        logger.error('记录重置邮件发送日期时，账号记录丢失')
        return ERR_RESET_MAIL_NOTEXIST

    # 如果数据库异常无法记录邮件发送日期
    elif update_tag == ERR_UPDATE_DB:
        logger.error('数据库异常导致无法发送重置邮件')
        return ERR_RESET_MAIL_DB

    # 如果日期记录成功，发送邮件
    send_163_mail('13660106752', 'xuegongban118', '13660106752@163.com', acnt, 'WeMeet重置密码邮件',
                  reset_mail.get_content(ciphertext, acnt))
    return OK_RESET_MAIL


def reset(account_cipher):
    """
    重置账号，修改账号状态为未激活，修改密码为随机字符串的哈希值
    @account_cipher: 由后端加密的account，只能通过邮件获得
    成功：返回{'credential': credential, 'account': account}
    失败：返回ERR_RESET_NOTEXIST
           或ERR_SELECT_DB
    """
    obj = account.ciphertext_select(ciphertext=account_cipher)

    # 如果账号不存在
    if obj['tag'] == ERR_SELECT_NOTEXIST:
        logger.warning('尝试重置不存在的账号')
        return ERR_RESET_NOTEXIST

    # 如果数据库异常无法查询
    elif obj['tag'] == ERR_SELECT_DB:
        logger.error('数据库异常导致无法验证账号是否存在，无法重置账号')
        return ERR_RESET_DB

    # 如果账号存在，但重置账号的请求已过期
    elif date_helper.pass_days(obj['acnt'].reset_date) > date_helper.OUT_DATE_DAYS:
        return ERR_RESET_OUT_DATE

    # 如果账号存在，请求未过期，重置状态和密码
    credential = get_hashcode()
    tag = account.update(account=obj['acnt'].account, is_activated=False, pwd=credential)

    # 如果更新账号时，账号不存在
    if tag == ERR_UPDATE_NOTEXIST:
        logger.error('重置账号时，账号记录丢失')
        return ERR_RESET_NOTEXIST

    # 如果数据库异常导致无法重置账号
    elif tag == ERR_UPDATE_DB:
        logger.error('数据库异常导致无法重置账号账号')

    # 如果重置账号成功
    return {'credential': credential, 'account': obj['acnt'].account}  # 防止credential(哈希值）和ERROR_RESET_DOESNOTEXIST冲突


def change_pwd(acnt, credential, pwd):
    """
    验证凭据激活账号修改密码
    成功：激活账号，修改密码， 返回OK_CHANGE_PWD
    失败：返回ERR_CHANGE_PWD_NOTEXIST
          或ERR_CHANGE_PWD_WRONG_CREDENTIAL
          或ERR_CHANGE_PWD_DB
    """
    obj = account.acnt_select(account=acnt)
    # 如果账号不存在
    if obj['tag'] == ERR_SELECT_NOTEXIST:
        logger.warning('尝试修改不存在账号的密码')
        return ERR_CHANGE_PWD_NOTEXIST

    # 如果数据异常导致无法验证账号是否存在
    elif obj['tag'] == ERR_SELECT_DB:
        logger.error('数据库异常导致无法修改密码（无法验证账号是否存在）')
        return ERR_CHANGE_PWD_DB

    # 账号存在，如果凭据错误
    elif obj['acnt'].pwd != credential:
        logger.info('以错误的凭据修改密码')
        return ERR_CHANGE_PWD_WRONG_CREDENTIAL

    # 如果账号存在，凭据正确，激活账号，并修改密码
    else:
        tag = account.update(account=acnt, is_activated=True, pwd=pwd)
        # 如果数据库异常导致无法修改密码
        if tag == ERR_UPDATE_DB:
            logger.error('数据库异常导致无法修改密码')
            return ERR_CHANGE_PWD_DB
        # 如果修改密码时，账号不存在
        elif tag == ERR_UPDATE_NOTEXIST:
            logger.error('修改密码时，账号记录丢失')
            return ERR_CHANGE_PWD_NOTEXIST
        # 如果更新成功(tag == GOOD_UPDATE)
        else:
            return OK_CHANGE_PWD
