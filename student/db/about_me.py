from student.db.tag import ERR_SELECT_NOTEXIST
from student.db.tag import ERR_SELECT_DB
from student.db.tag import OK_SELECT


from student.models import StuAboutMe

from student.util.logger import logger


def stu_select(stu_id):
    """
    成功：返回{'tag': OK_SELECT, 'stu': select_stu}
    失败：返回{'tag': ERR_SELECT_NOTEXIST}
           或{'tag': ERR_SELECT_DB}
    """
    selected = StuAboutMe.objects.all().filter(stu_id=stu_id)
    return {'tag': OK_SELECT, 'about_me': selected}

