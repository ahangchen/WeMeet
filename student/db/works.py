from student.db.tag import ERR_DELETE_DB
from student.db.tag import ERR_UPDATE_NOTEXIST
from student.db.tag import ERR_UPDATE_DB
from student.db.tag import ERR_INSERT_DB
from student.db.tag import ERR_SELECT_NOTEXIST
from student.db.tag import ERR_SELECT_DB
from student.db.tag import OK_DELETE
from student.db.tag import OK_INSERT
from student.db.tag import OK_UPDATE
from student.db.tag import OK_SELECT

from student.models import StuWorks
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


def insert(path, site, stu):
    """
    插入作品集信息
    成功：返回{'tag': OK_INSERT, 'works': new_works}
    失败：返回{'tag': ERR_INSERT_DB}
    """
    try:
        new_works = StuWorks(path=path,
                             site=site,
                             stu=stu)

        new_works.save()
        return {'tag': OK_INSERT,
                'works': new_works}
    except:
        logger.error('数据库异常导致插入作品集记录失败')
        return {'tag': ERR_INSERT_DB}



