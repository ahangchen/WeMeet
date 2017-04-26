"""
学生广场
"""
from student.db import stu_info
from student.ctrl.tag import OK_GET_TOP6
from student import ctrl


def top6():
    top_list = []
    for stu in stu_info.likes_sort()[0: 6]:
        skill_rlt = ctrl.skill.get(stu_id=stu.id)
        top_list.append({
            'stu_id': stu.id,
            'name': stu.name,
            'title': stu.title,
            'personal_signature': stu.personal_signature,
            'avatar_path': stu.avatar_path,
            'skill_list': [] if skill_rlt['tag'] != ctrl.skill.OK_GET_SKILL else skill_rlt['skill_list']
        })
    return {'tag': OK_GET_TOP6, 'top_list': top_list}


def top6_in_label(label):
    top_list = []
    for stu in stu_info.label_filter_sort(label)[0: 6]:
        skill_rlt = ctrl.skill.get(stu_id=stu.id)
        top_list.append({
            'stu_id': stu.id,
            'name': stu.name,
            'title': stu.title,
            'personal_signature': stu.personal_signature,
            'avatar_path': stu.avatar_path,
            'skill_list': [] if skill_rlt['tag'] != ctrl.skill.OK_GET_SKILL else skill_rlt['skill_list']
        })
    return {'tag': OK_GET_TOP6, 'top_list': top_list}
