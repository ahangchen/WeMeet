from team.models import Pwd, Team

DB_OK = 0
DB_ACC_NOT_FOUND = 1


def is_team_inv_match(mail, inv_code):
    return Pwd.objects.filter(team=mail, invite_code=inv_code) is not None


def update_team_pwd(team_id, pwd):
    Pwd.objects.filter(team=team_id).update(pwd_hash=pwd)
    return DB_OK


def team_of_mail_pwd(mail, pwd):
    if Pwd.objects.filter(team=mail, pwd_hash=pwd).count() > 0:
        return Team.objects.filter(contact_mail=mail)
    else:
        return None


def team_mail(team_id):
    team = Team.objects.filter(id=team_id).first()
    if team is None:
        return None
    return team['contact_mail']


def mail_team(mail):
    team = Team.objects.filter(contact_mail=mail).first()
    if team is None:
        return None
    else:
        return team['id']


def is_mail_valid(mail):
    return Pwd.objects.filter(team=mail).count() > 0


def reset_team(mail, reset_key):
    Pwd.objects.filter(team=mail).update(reset_key=reset_key)


def update_pwd(mail, hash_tid, new_pwd):
    team = Pwd.objects.filter(team=mail, reset_key=hash_tid).first()
    if team is None:
        return DB_ACC_NOT_FOUND
    else:
        team.update(pwd_hash=new_pwd)
        return DB_OK
