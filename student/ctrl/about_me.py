from student.db import about_me
from student.util.logger import logger
from student.ctrl.tag import OK_GET_ABOUT_ME, ERR_GET_ABOUT_ME_NOTEXIST, ERR_GET_ABOUT_ME_DB


def get(stu_id):
    """
    @param stu_id:
    @return:
    """
    rlt = about_me.stu_select(stu_id)
    if rlt['tag'] == about_me.OK_SELECT:
        return {'tag': OK_GET_ABOUT_ME, 'about_me_list': list(rlt['about_me'].values())}

    # 如果异常导致获取学生"关于我"失败
    else:
        logger.error('数据库异常导致获取学生信息失败')
        return {'tag': ERR_GET_ABOUT_ME_DB}

