from student.db import about_me
from student.util.logger import logger
from student.ctrl.tag import OK_GET_ABOUT_ME, ERR_GET_ABOUT_ME_DB,\
                             OK_UPDATE_ABOUT_ME, ERR_UPDATE_ABOUT_ME_DB, \
                             OK_ADD_ABOUT_ME, ERR_ADD_ABOUT_ME_DB, \
                             OK_DEL_ABOUT_ME, ERR_DEL_ABOUT_ME


def get(stu_id):
    rlt = about_me.stu_filter(stu_id)
    if rlt['tag'] == about_me.OK_SELECT:
        return {'tag': OK_GET_ABOUT_ME, 'about_me_list': list(rlt['about_me'].values())}

    # 如果异常导致获取学生"关于我"失败
    else:
        logger.error('数据库异常导致获取学生信息失败')
        return {'tag': ERR_GET_ABOUT_ME_DB}


def update(about_me_id, title, text, stu_id):
    return {'tag': OK_UPDATE_ABOUT_ME} \
        if about_me.update(about_me_id, title, text, stu_id) == about_me.OK_UPDATE \
        else {'tag': ERR_UPDATE_ABOUT_ME_DB}


def add(title, text, stu_id):
    rlt = about_me.insert(title, text, stu_id)
    if rlt['tag'] == about_me.OK_INSERT:
        return {'tag': OK_ADD_ABOUT_ME, 'about_me_id': rlt['about_me'].about_me_id}
    else:
        return {'tag': ERR_ADD_ABOUT_ME_DB}


def delete(about_me_id, stu_id):
    return {'tag': OK_DEL_ABOUT_ME} \
        if about_me.delete(about_me_id, stu_id) == about_me.OK_DELETE \
        else {'tag': ERR_DEL_ABOUT_ME}
