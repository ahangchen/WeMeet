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
from student.util.value_update import value, NO_INPUT
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


def id_stu_update(works_id, stu, path=NO_INPUT, site=NO_INPUT):
    """
    成功：返回OK_UPDATE
    失败：返回ERR_UPDATE_NOTEXIST
            或ERR_UPDATE_DB
    """
    try:
        update_works = StuWorks.objects.all().get(works_id=works_id, stu=stu)

        update_works.path = value(update_works.path, path)
        update_works.site = value(update_works.site, site)

        update_works.save()
        return OK_UPDATE
    except StuWorks.DoesNotExist:
        logger.error('尝试更新学生id和作品集信息id不匹配的作品集信息')
        return ERR_UPDATE_NOTEXIST
    except:
        logger.error('数据库异常导致更新作品集信息失败')
        return ERR_UPDATE_DB


def id_stu_delete(works_id, stu):
    """
    用works_id和stu删除作品集信息
    成功：返回OK_DELETE
    失败：返回ERR_DELETE_DB
    """
    try:
        delete_works = StuWorks.objects.all().get(works_id=works_id, stu=stu)  # 抛出MultipleObjectsReturned或DoesNotExist
        delete_works.delete()  # 不抛出异常
        return OK_DELETE

    except StuWorks.DoesNotExist:
        logger.error('尝试删除学生id和作品集信息id不匹配的作品集信息')
        return ERR_DELETE_DB

    except StuWorks.MultipleObjectsReturned:
        logger.info('数据库异常（存在重复记录）')
        StuWorks.objects.all().filter(works_id=works_id, stu=stu).delete()  # 不抛异常
        return OK_DELETE

    # 数据库异常
    except:
        logger.error('数据库异常导致删除项目作品集信息失败')
        return ERR_DELETE_DB


