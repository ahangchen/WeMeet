from student.db.tag import ERR_DELETE_DB
from student.db.tag import ERR_UPDATE_NOTEXIST
from student.db.tag import ERR_UPDATE_DB
from student.db.tag import ERR_INSERT_DB
from student.db.tag import ERR_SELECT_NOTEXIST
from student.db.tag import ERR_SELECT_DB
from student.db.tag import OK_DELETE
from student.db.tag import OK_INSERT
from student.db.tag import OK_UPDATE
from student.db.tag import ERR_DELETE_NOTEXIST

from student.models import StuWorks
from student.util.value_update import value, NO_INPUT
from student.util.logger import logger


def stu_filter(stu):
    """
    用学生查询作品信息
    返回QuerySet
    """
    return StuWorks.objects.filter(stu=stu, is_deleted=False)


def insert(name, duty, url, description, stu, img='', audio='', video=''):
    """
    插入作品集信息
    成功：返回{'tag': OK_INSERT, 'works': new_works}
    失败：返回{'tag': ERR_INSERT_DB}
    """
    try:
        new_works = StuWorks(name=name,
                             duty=duty,
                             url=url,
                             description=description,
                             img=img,
                             audio=audio,
                             video=video,
                             stu=stu,
                             is_deleted=False)
        new_works.save()
        return {'tag': OK_INSERT, 'works': new_works}

    except Exception as e:
        logger.error(e.__str__() + '数据库异常导致插入作品记录失败')
        return {'tag': ERR_INSERT_DB}


def update(works_id, stu, name=NO_INPUT, duty=NO_INPUT, url=NO_INPUT, description=NO_INPUT,
           img=NO_INPUT, audio=NO_INPUT, video=NO_INPUT):
    """
    成功：返回OK_UPDATE
    失败：返回ERR_UPDATE_NOTEXIST
            或ERR_UPDATE_DB
    """
    try:
        update_works = StuWorks.objects.all().get(works_id=works_id, stu=stu, is_deleted=False)

        update_works.name = value(update_works.name, name)
        update_works.duty = value(update_works.duty, duty)
        update_works.url = value(update_works.url, url)
        update_works.description = value(update_works.description, description)
        update_works.img = value(update_works.img, img)
        update_works.audio = value(update_works.audio, audio)
        update_works.video = value(update_works.video, video)

        update_works.save()
        return OK_UPDATE
    except StuWorks.DoesNotExist:
        logger.error('尝试更新学生id和作品信息id不匹配或已删除的作品集信息')
        return ERR_UPDATE_NOTEXIST
    except Exception as e:
        logger.error(e.__str__() + '数据库异常导致更新作品信息失败')
        return ERR_UPDATE_DB


def delete(works_id, stu):
    """
    用works_id和stu删除作品集信息
    成功：返回OK_DELETE
    失败：返回ERR_DELETE_DB
    """
    try:
        delete_works = StuWorks.objects.all().get(works_id=works_id, stu=stu, is_deleted=False)

        delete_works.is_deleted = True

        delete_works.save()
        return OK_DELETE
    except StuWorks.DoesNotExist:
        logger.error('尝试删除学生id和作品信息id不匹配或已删除的作品集信息')
        return ERR_DELETE_NOTEXIST
    except Exception as e:
        logger.error(e.__str__() + '数据库异常导致删除作品信息失败')
        return ERR_DELETE_DB



