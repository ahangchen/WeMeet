from student.models import StuInfo, StuAccount

from student.db import stu_info
from student.db.tag import ERR_INSERT_DB, OK_INSERT, ERR_DELETE_NOTEXIST, \
                            OK_UPDATE, ERR_UPDATE_DB, ERR_UPDATE_NOTEXIST,\
                            OK_SELECT, ERR_SELECT_DB, ERR_SELECT_NOTEXIST,\
                            OK_DELETE, ERR_DELETE_DB

from student.util.value_update import value, NO_INPUT
from student.util.date_helper import pre_date
from student.util.logger import logger

DEFAULT_CIPHERTEXT = '032164879231378144'


def insert(account, pwd, stu):
    """
    成功：返回插入的账号
    失败：返回ERR_INSERT
    """
    try:
        new_account = StuAccount(account=account,
                                 pwd=pwd,
                                 is_activated=False,
                                 ciphertext=DEFAULT_CIPHERTEXT,
                                 reset_date=pre_date(),
                                 stu=stu)
        new_account.save()
        return new_account

    # 如果插入账号发生异常
    except Exception as e:
        logger.error(e.__str__() + '数据库异常导致插入账号失败')
        return ERR_INSERT_DB


def update(account, pwd=NO_INPUT, is_activated=NO_INPUT, ciphertext=NO_INPUT, reset_date=NO_INPUT):
    try:
        update_account = StuAccount.objects.all().get(account=account)

        update_account.pwd = value(update_account.pwd, pwd)
        update_account.ciphertext = value(update_account.ciphertext, ciphertext)
        update_account.is_activated = value(update_account.is_activated, is_activated)
        update_account.reset_date = value(update_account.reset_date, reset_date)

        update_account.save()
        return OK_UPDATE
    except StuAccount.DoesNotExist:
        return ERR_UPDATE_NOTEXIST
    except Exception as e:
        logger.error(e.__str__() + '数据库异常导致账号更新失败')
        return ERR_UPDATE_DB


def stu_update(stu_id, account):
    try:
        update_account= StuAccount.objects.all().get(stu_id=stu_id)
        update_account.account = account
        update_account.save()
        return OK_UPDATE
    except StuAccount.DoesNotExist:
        return ERR_UPDATE_NOTEXIST
    except Exception as e:
        logger.error(e.__str__() + '数据库异常导致账号更新失败')
        return ERR_UPDATE_DB


def acnt_select(account):
    """
    用账号id查找账号
    成功：返回{'tag': OK_SELECT, 'acnt': select_acnt}
    失败：返回{'tag': ERR_SELECT_NOTEXIST}
           或{'tag': ERR_SELECT_DB}
    """
    try:
        select_acnt = StuAccount.objects.all().get(account=account)
        return {'tag': OK_SELECT,
                'acnt': select_acnt}

    except StuAccount.DoesNotExist:
        return {'tag': ERR_SELECT_NOTEXIST}
    except Exception as e:
        logger.error(e.__str__() + '数据库异常导致账号查询失败')
        return {'tag': ERR_SELECT_DB}


def ciphertext_select(ciphertext):
    """
    用密文查找账号
    成功：返回{'tag': OK_SELECT, 'acnt': select_acnt}
    失败：返回{'tag': ERR_SELECT_NOTEXIST}
           或{'tag': ERR_SELECT_DB}
    """
    try:
        select_acnt = StuAccount.objects.all().get(ciphertext=ciphertext)
        return {'tag': OK_SELECT,
                'acnt': select_acnt}
    except StuAccount.DoesNotExist:
        return {'tag': ERR_SELECT_NOTEXIST}
    except Exception as e:
        logger.error(e.__str__() + '数据库异常导致账号查询失败')
        return {'tag': ERR_SELECT_DB}


def stu_select(stu_id):
    """
    用学生id查找账号
    成功：返回{'tag': OK_SELECT, 'acnt': select_acnt}
    失败：返回{'tag': ERR_SELECT_NOTEXIST}
           或{'tag': ERR_SELECT_DB}
    """
    try:
        select_acnt = StuAccount.objects.all().get(stu_id=stu_id)
        return {'tag': OK_SELECT,
                'acnt': select_acnt}
    except StuAccount.DoesNotExist:
        return {'tag': ERR_SELECT_NOTEXIST}
    except Exception as e:
        logger.error(e.__str__() + '数据库异常导致账号查询失败')
        return {'tag': ERR_SELECT_DB}


def delete(account):
    try:
        delete_acnt = StuInfo.objects.all().get(account=account)  # 抛出MultipleObjectsReturned或DoesNotExist
        delete_acnt.delete()  # 不抛出异常
        return OK_DELETE

    except StuAccount.DoesNotExist:
        logger.error('尝试删除不存在的账号')
        return ERR_DELETE_DB

    except StuInfo.MultipleObjectsReturned:
        logger.info('数据库异常（存在重复记录）')
        StuInfo.objects.all().filter(account=account).delete()  # 不抛异常
        return OK_DELETE

    # 数据库异常
    except Exception as e:
        logger.error(e.__str__() + '数据库异常导致删除账号失败')
        return ERR_DELETE_DB








