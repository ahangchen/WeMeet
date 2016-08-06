import time

from student.db.stu_info import query
from student.db import account
from team.ctrl.defines import URL_HEADER, LOCAL_HEADER
from team.db import team

from student.util.file_helper import save
from team.models import TeamImg

TEAM_OK = 0
LABEL_EXIST = -1
STU_NO_FOUND = -2
NO_MATCH = -3
ACC_NO_FOUND = -4
LABEL_NO_FOUND = -5


def info(tid):
    return team.info(tid)


def bus_names():
    return team.bus_names()


def update_info(tid, name, logo_path, slogan, about, history):
    teams = team.get(tid)
    if teams.count() < 1:
        return ACC_NO_FOUND
    else:
        teams.update(name=name, logo_path=logo_path, slogan=slogan, about=about, history=history)
        return TEAM_OK


def update_contact(tid, tel, mail):
    teams = team.get(tid)
    pwds = team.acc(tid)
    if teams.count() < 1:
        return ACC_NO_FOUND
    if pwds.count() < 1:
        return ACC_NO_FOUND
    pwds.update(mail=mail)
    teams.update(contact_tel=tel)
    return TEAM_OK


def add_label(tid, name):
    teams = team.get(tid)
    if teams.count() < 1:
        return ACC_NO_FOUND
    else:
        return team.add_team_label(teams.first(), name)


def rm_label(tid, name):
    teams = team.get(tid)
    if teams.count() < 1:
        return ACC_NO_FOUND
    elif team.rm_team_label(teams.first(), name):
        return TEAM_OK
    else:
        return LABEL_NO_FOUND


def add_stu(tid, sid):
    teams = team.get(tid)
    if teams.count() < 1:
        return ACC_NO_FOUND
    stus = query(sid)
    if stus.count() < 1:
        return STU_NO_FOUND
    team.add_stu(teams.first(), stus.first())
    return TEAM_OK


def rm_stu(tid, sid):
    teams = team.get(tid)
    if teams.count() < 1:
        return ACC_NO_FOUND
    stus = query(sid)
    if stus.count() < 1:
        return STU_NO_FOUND
    if team.rm_team_stu(teams.first(), stus.first()):
        return TEAM_OK
    else:
        return STU_NO_FOUND


def url2path(url):
    return url.replace(URL_HEADER, LOCAL_HEADER)


def path2url(path):
    return path.replace(LOCAL_HEADER, URL_HEADER)


def name2path(name):
    return LOCAL_HEADER + name


def name2url(name):
    return URL_HEADER + name


def save_photo(tid, name, img):
    teams = team.get(tid)
    if teams.count() < 1:
        return ACC_NO_FOUND
    img_count = team.img_cnt()
    name = str(time.time()).replace('.', '') + str(img_count) + name
    path = name2path(name)
    save(img, path)
    img_id = team.add_img(teams.first(), path)
    return img_id


def save_logo(name, img):
    name = str(time.time()).replace('.', '') + name
    path = name2path(name)
    print(path)
    save(img, path)
    return path


def rm_photo(tid, img_id):
    teams = team.get(tid)
    if teams.count() < 1:
        return ACC_NO_FOUND
    imgs = TeamImg.objects.filter(id=img_id)
    if imgs.count() < 1:
        return ACC_NO_FOUND
    imgs.delete()
    return TEAM_OK


def name2mail(name):
    return account.name2mail(name)