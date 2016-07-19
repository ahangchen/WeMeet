from student.util.encrypt_decrypt import encrypt

from team.db import team
from team.db.team import DB_ACC_NOT_FOUND, DB_OK, is_mail_valid, mail_team
from team.models import Pwd
from team.util.smtp_mail import send_163_mail

ACC_MNG_OK = 0
REG_FAIL_INV_ACC = 1
LOGIN_FAIL_NO_MATCH = 2
ACC_UNABLE = 3
ACC_NO_FOUND = 4


def register(mail, pwd, invite):
    """
    注册
    成功：返回 ACC_MNG_OK
    失败：返回 REG_FAIL_INV_ACC
    """
    # 检查是否存在acnt + invite
    if team.is_team_inv_match(mail, invite):
        # 如果存在则更新pwd
        team.update_team_pwd(mail, pwd)
        return ACC_MNG_OK
    else:
        # 如果不存在提示账号不存在或邀请码错误
        return REG_FAIL_INV_ACC


def login(mail, pwd):
    """
    登陆
    成功：返回OK_LOGIN
    失败：返回ERR_LOGIN_NOTEXIST
            或ERR_LOGIN_DB
            或ERR_LOGIN_WRONG_PWD
            或ERR_LOGIN_NONACTIVATED

    @account: 账号（邮箱）
    @pwd: 密码
    """
    tid, state = team.team_of_mail_pwd(mail, pwd)
    # 如果账号不存在
    if tid is None:
        return LOGIN_FAIL_NO_MATCH, -1
    # 如果账号不可用
    elif state != 0:
        return ACC_UNABLE, -1
    # 登陆成功
    else:
        return ACC_MNG_OK, tid


def reset_mail_content(reset_key, mail):
    return '<h1>点此重置密码</h1><p>http://110.64.69.66/team/fetch?reset_key=%s&mail=%s</p>' % (reset_key, mail)


def send_reset_mail(mail):
    """
    发送密码重置邮件，记录链接发送的时间
    成功：发送重置邮件并返回OK_RESTE_MAIL
    失败：返回ERR_RESET_MAIL_NOTEXIST
    或ERR_RESET_MAIL_DB
    @account: 账号（邮箱）
    """
    tid = mail_team(mail)
    if tid is None:
        return ACC_NO_FOUND
    else:
        # 账号密文
        hash_tid = encrypt(str(tid))
        team.reset_team(mail, hash_tid)
        send_163_mail(mail, '来自WeMeet', reset_mail_content(hash_tid, mail))
        return ACC_MNG_OK


def update_pwd(mail, hash_tid, pwd):
    """
    验证凭据激活账号修改密码
    成功：激活账号，修改密码， 返回OK_CHANGE_PWD
    失败：返回ERR_CHANGE_PWD_NOTEXIST
          或ERR_CHANGE_PWD_WRONG_CREDENTIAL
          或ERR_CHANGE_PWD_DB
    """
    ret = team.update_pwd(mail, hash_tid, pwd)
    if ret == DB_OK:
        return ACC_MNG_OK
    elif ret == DB_ACC_NOT_FOUND:
        return ACC_NO_FOUND


def invite(name, leader, tel, mail):
    return team.invite(name, leader, tel, mail)

