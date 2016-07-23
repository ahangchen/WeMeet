from student.models import StuWorks

from student.db.tag import OK_SELECT
from student.db.tag import ERR_SELECT_NOTEXIST
from student.db.tag import ERR_SELECT_DB
from student.util.logger import logger


def stu_select(stu):
    """
    成功：返回{'tag': OK_SELECT, 'works': select_works}
    失败：返回 {'tag': ERR_SELECT_NOTEXIST}或{'tag': ERR_SELECT_DB}
    """
    try:
        select_works = StuWorks.objects.all().get(stu=stu)
        return {'tag': OK_SELECT,
                'works': select_works}
    except StuWorks.DoesNotExist:
        return {'tag': ERR_SELECT_NOTEXIST}
    except:
        logger.error('数据库异常导致获取作品信息失败')
        return {'tag': ERR_SELECT_DB}



