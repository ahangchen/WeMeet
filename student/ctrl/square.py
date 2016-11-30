"""
学生广场
"""
from student.db import stu_info, label
from student.ctrl.tag import OK_GET_TOP6


def top6():
    top_list = []
    for stu in stu_info.likes_sort()[0: 6]:
        label2_list = label.stu_filter(stu=stu)
        top_list.append({
            'stu_id': stu.id,
            'name': stu.name,
            'title': stu.title,
            'personal_signature': stu.personal_signature,
            'avatar_path': stu.avatar_path,
            'label2_list': list(label2_list.values())
        })
    return {'tag': OK_GET_TOP6, 'top_list': top_list}


def top6_in_label(label1):
    top_list = []
    for stu in stu_info.label_filter_sort(label1)[0: 6]:
        label2_list = label.stu_filter(stu=stu)
        top_list.append({
            'stu_id': stu.id,
            'name': stu.name,
            'title': stu.title,
            'personal_signature': stu.personal_signature,
            'avatar_path': stu.avatar_path,
            'label2_list': list(label2_list.values())
        })
    return {'tag': OK_GET_TOP6, 'top_list': top_list}
