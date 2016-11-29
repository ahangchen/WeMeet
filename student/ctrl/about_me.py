from student.db import about_me
from student.util.logger import logger
from student.ctrl.tag import OK_GET_ABOUT_ME, ERR_GET_ABOUT_ME_NOTEXIST, ERR_GET_ABOUT_ME_DB


def get(stu_id):
    """
    @param stu_id:
    @return:
    """
    rlt = about_me.select(stu_id)
    if rlt['tag'] == about_me.OK_SELECT:
        return {'tag': OK_GET_ABOUT_ME,
                'about_me_id': rlt['about_me'].about_me_id,
                'experience': rlt['about_me'].experience,
                'self_description': rlt['about_me'].self_description,
                'internship': rlt['about_me'].internship}

    elif rlt['tag'] == about_me.ERR_SELECT_NOTEXIST:
        logger.error('学生不存在，获取学生"关于我"失败')
        return {'tag': ERR_GET_ABOUT_ME_NOTEXIST}

    # 如果数据库异常导致获取学生"关于我"失败(select_rlt['tag'] == ERR_SELECT_DB)
    else:
        logger.error('数据库异常导致获取学生信息失败')
        return {'tag': ERR_GET_ABOUT_ME_DB}

