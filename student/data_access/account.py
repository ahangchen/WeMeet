from student.models import StuInfo, StuAccount

from student.data_access import stu_info
from student.data_access.tag import ERR_INSERT_DB, OK_INSERT, ERR_DELETE_NOTEXIST, \
                                        OK_UPDATE, ERR_UPDATE_DB, ERR_UPDATE_NOTEXIST,\
                                        ERR_SELECT_DB, ERR_SELECT_NOTEXIST,\
                                        OK_DELETE, ERR_DELETE_DB

from student.utility.value_update import value, NO_INPUT
from student.utility.date_helper import pre_date
from student.utility.logger import logger

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
    except:
        logger.error('数据库异常导致插入账号失败')
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
    except:
        logger.error('数据库异常导致账号更新失败')
        return ERR_UPDATE_DB


def select(account=NO_INPUT, ciphertext=NO_INPUT):
    """
    成功：返回查询的账号
    失败：返回ERR_SELECT_NOTEXIST
           或ERR_SELECT
    """
    try:
        if account != NO_INPUT and ciphertext == NO_INPUT:
            select_acnt = StuAccount.objects.all().get(account=account)
            return select_acnt

        elif account == NO_INPUT and ciphertext != NO_INPUT:
            select_acnt = StuAccount.objects.all().get(ciphertext=ciphertext)
            return select_acnt

        elif account != NO_INPUT and ciphertext != NO_INPUT:
            select_acnt = StuAccount.objects.all().get(account=account, ciphertext=ciphertext)
            return select_acnt

        return

    except StuAccount.DoesNotExist:
        return ERR_SELECT_NOTEXIST
    except:
        logger.error('数据库异常导致账号查询失败')
        return ERR_SELECT_DB


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
    except:
        logger.error('数据库异常导致删除账号失败')
        return ERR_DELETE_DB








