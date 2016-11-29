from student.db.tag import ERR_SELECT_NOTEXIST
from student.db.tag import ERR_SELECT_DB
from student.db.tag import OK_SELECT


from student.models import StuAboutMe

from student.util.logger import logger


def select(stu_id):
    """
    成功：返回{'tag': OK_SELECT, 'stu': select_stu}
    失败：返回{'tag': ERR_SELECT_NOTEXIST}
           或{'tag': ERR_SELECT_DB}
    """
    try:
        selected = StuAboutMe.objects.all().get(stu_id=stu_id)
        return {'tag': OK_SELECT,
                'about_me': selected}
    except StuAboutMe.DoesNotExist:
        return {'tag': ERR_SELECT_NOTEXIST}
    except Exception as e:
        logger.error(e.__str__() + '数据库异常导致查询学生“关于我”失败')
        return {'tag': ERR_SELECT_DB}
