from student.ctrl.tag import OK_GET_WORKS, ERR_GET_NO_WORKS, ERR_GET_WORKS_DB

from student.util.logger import logger
from student.db import stu_info, works


def get_works(stu_id):
    """
    获取学生的作品集
    """
    select_rlt = stu_info.select(stu_id=stu_id)
    # 如果学生存在
    if select_rlt['tag'] == stu_info.OK_SELECT:
        filter_set = works.stu_filter(stu=select_rlt['stu'])

        # 如果该学生有合法的作品数量数量
        if filter_set.count() in range(1, 6):
            return {'tag': OK_GET_WORKS,
                    'works_list': list(filter_set.values())}

        # 如果该学生无作品
        elif filter_set.count() == 0:
            return {'tag': ERR_GET_NO_WORKS}
        # 如果该学生的作品数量不合法
        else:
            logger.error('学生id为%s的学生拥有不合法的作品数量，导致获取作品失败' % stu_id)
            return {'tag': ERR_GET_WORKS_DB}

    # 如果学生不存在
    elif select_rlt['tag'] == stu_info.ERR_SELECT_NOTEXIST:
        logger.warning('尝试获取不存在的学生的作品')
        return {'tag': ERR_GET_WORKS_DB}
    # 如果数据库异常导致无法确认学生是否存在(select_rlt['tag'] == ERR_SELECT_DB)
    else:
        logger.error('数据库异常导致无法确认学生是否存在，查询作品失败')
        return {'tag': ERR_GET_WORKS_DB}
