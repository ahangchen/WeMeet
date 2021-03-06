from team.models import Pwd, Team, TeamImg, TeamStu, Label, BusinessType, TeamType, Product, Job
from team.util.data import random6

DB_OK = 0
DB_ACC_NOT_FOUND = 1


def is_team_inv_match(mail, inv_code):
    return Pwd.objects.filter(mail=mail, invite_code=inv_code).count() > 0


def update_team_pwd(team_id, pwd):
    Pwd.objects.filter(mail=team_id).update(pwd_hash=pwd, state=0)
    return DB_OK


def team_of_mail_pwd(mail, pwd):
    pwd = Pwd.objects.filter(mail=mail, pwd_hash=pwd)
    if pwd.count() > 0:
        pwd = pwd.first()
        return Team.objects.filter(pwd=pwd).first().id, pwd.state
    else:
        return None, None


def team_mail(team_id):
    team = Team.objects.filter(id=team_id).select_related().first()
    if team is None:
        return None
    return team.pwd.mail


def mail_team(mail):
    pwd = Pwd.objects.filter(mail=mail).first()
    team = Team.objects.filter(pwd=pwd).first()
    if team is None:
        return None
    else:
        return team.id


def id_team(team_id):
    team = Team.objects.filter(id=team_id).first()
    if team is None:
        return None
    return team


def is_mail_valid(mail):
    return Pwd.objects.filter(mail=mail).count() > 0


def reset_team(mail, reset_key):
    Pwd.objects.filter(mail=mail).update(reset_key=reset_key)


def update_pwd(mail, hash_tid, new_pwd):
    team = Pwd.objects.filter(mail=mail, reset_key=hash_tid)
    if team.count() <= 0:
        return DB_ACC_NOT_FOUND
    else:
        team.update(pwd_hash=new_pwd)
        return DB_OK


def info(tid):
    team = Team.objects.filter(id=tid).select_related().first()
    if team is None:
        return None
    stu_s = TeamStu.objects.select_related().filter(team=team)
    stu_dict = []
    for stu in stu_s:
        if len(stu.stu.name) == 0:
            stu_dict.append({
                'id': stu.stu.id, 'name': stu.stu.stuaccount_set.first().account, 'school': stu.stu.school, 'logo_path': stu.stu.avatar_path
            })
        else:
            stu_dict.append({
                'id': stu.stu.id, 'name': stu.stu.name, 'school': stu.stu.school, 'logo_path': stu.stu.avatar_path
            })
    img_s = TeamImg.objects.filter(team=team)
    img_dict = [{'id': img.id, 'path': img.path} for img in img_s]
    label_s = Label.objects.filter(team=team)
    label_dict = [label.name for label in label_s]
    return {
        'tid': team.id,
        'b_type': team.b_type,
        'slogan': team.slogan,
        'logo_path': team.logo_path,
        'about': team.about,
        'man_cnt': team.man_cnt,
        'history': team.history,
        'tel': team.contact_tel,
        'mail': team.pwd.mail,
        'stus': stu_dict,
        'imgs': img_dict,
        'label': label_dict,
        'name': team.name,
    }


def invite(name, leader, tel, mail):
    inv_code = str(random6())
    if Pwd.objects.filter(mail=mail).count() > 0:
        return None
    pwd = Pwd(mail=mail, invite_code=inv_code, state=1)
    pwd.save()
    team = Team(pwd=pwd, name=name, leader=leader, contact_tel=tel)
    team.save()
    return pwd.invite_code


def bus_names():
    business = list(BusinessType.objects.values())
    return business


def get(tid):
    return Team.objects.filter(id=tid)


def is_team_exist(tid):
    return Team.objects.filter(id=tid).count() > 0


def add_team_label(team, name):
    label = Label(team=team, name=name)
    label.save()
    return label.id


def rm_team_label(team, name):
    label = Label.objects.filter(team=team, name=name)
    if label.count() < 1:
        return False
    else:
        label.delete()
        return True


def add_stu(team, stu):
    team_stu = TeamStu(team=team, stu=stu)
    team_stu.save()
    return True


def rm_team_stu(team, stu):
    team_stus = TeamStu.objects.filter(team=team, stu=stu)
    if team_stus.count() < 1:
        return False
    else:
        team_stus.delete()
        return True


def acc(tid):
    return Pwd.objects.filter(id=tid)


def img_cnt():
    return TeamImg.objects.count()


def add_img(team, path):
    img = TeamImg(team=team, path=path)
    img.save()
    return img.id


def newest(new_count):
    teams = Team.objects.all().order_by('-id')[: new_count]
    team_ret = [{'tid': team.id, 'logo_path': team.logo_path, 'name': team.name} for team in teams]
    return team_ret


def newest_more(team_type, new_count):
    if team_type == -1:
        teams = Team.objects.all().order_by('-id')[: new_count]
    else:
        teams = Team.objects.filter(b_type=team_type).order_by('-id')[: new_count]
    team_ret = [
        {
            'tid': team.id, 'logo_path': team.logo_path, 'name': team.name, 'slogan': team.slogan,
            'proj_cnt': Product.objects.filter(team=team).count(),
            'job_cnt': Job.objects.filter(team=team).count(),
            'stu_cnt': team.man_cnt,
            'labels': [
                label.name for label in team.label_set.all()
            ]
         } for team in teams
        ]
    return team_ret
