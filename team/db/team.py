from team.models import Pwd, Team

DB_OK = 0
DB_ACC_NOT_FOUND = 1


def is_team_inv_match(team_id, inv_code):
    return Pwd.objects.filter(team=team_id, invite_code=inv_code) is not None


def update_team_pwd(team_id, pwd):
    Pwd.objects.filter(team=team_id).update(pwd_hash=pwd)
    return DB_OK


def team_of_id_pwd(team_id, pwd):
    return Pwd.objects.filter(team=team_id, pwd_hash=pwd).first()


def team_mail(team_id):
    team = Team.objects.filter(id=team_id).first()
    if team is None:
        return None
    return team['contact_mail']


def reset_team(team_id, reset_key):
    Pwd.objects.filter(team=team_id).update(reset_key=reset_key)


def update_pwd(tid, hash_tid, new_pwd):
    team = Pwd.objects.filter(id=tid, reset_key=hash_tid).first()
    if team is None:
        return DB_ACC_NOT_FOUND
    else:
        team.update(pwd_hash=new_pwd)
        return DB_OK
