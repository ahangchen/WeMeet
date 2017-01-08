from student.db.tag import OK_UPDATE
from student.db.tag import ERR_UPDATE_DB
from student.db.tag import OK_SELECT
from student.db.tag import OK_INSERT
from student.db.tag import ERR_INSERT_DB
from student.db.tag import OK_DELETE
from student.db.tag import ERR_DELETE_DB


from student.models import StuAboutMe

from student.util.logger import logger


def stu_filter(stu_id):
    """
    成功：返回{'tag': OK_SELECT, 'about_me': selected}
    """
    selected = StuAboutMe.objects.all().filter(stu_id=stu_id, is_deleted=False)
    return {'tag': OK_SELECT, 'about_me': selected}


def update(about_me_id, title, text, stu_id):
    """
    成功:返回OK_UPDATE
    失败:返回ERR_UPDATE_DB
    """
    try:
        updated = StuAboutMe.objects.all().get(about_me_id=about_me_id, stu_id=stu_id, is_deleted=False)

        updated.title = title
        updated.text = text
        updated.save()
        return OK_UPDATE

    except StuAboutMe.DoesNotExist:
        logger.warning("尝试用不匹配的stu_id和about_me_id的更新关于我或更新已删除的关于我")
        return ERR_UPDATE_DB
    except Exception as e:
        logger.error(e.__str__() + '数据库异常导致更新关于我失败')
        return ERR_UPDATE_DB


def insert(title, text, stu_id):
    try:
        new_about_me = StuAboutMe(title=title,
                                  text=text,
                                  stu_id=stu_id,
                                  is_deleted=False)

        new_about_me.save()
        return {'tag': OK_INSERT,
                'about_me': new_about_me}
    except Exception as e:
        logger.error(e.__str__() + '数据库异常导致插入关于我失败')
        return {'tag': ERR_INSERT_DB}


def delete(about_me_id, stu_id):
    try:
        deleted = StuAboutMe.objects.all().get(about_me_id=about_me_id, stu_id=stu_id, is_deleted=False)

        deleted.is_deleted = True
        deleted.save()
        return OK_DELETE

    except StuAboutMe.DoesNotExist:
        logger.warning("尝试用不匹配的stu_id和about_me_id的删除关于我或删除已删除的关于我")
        return ERR_DELETE_DB
    except Exception as e:
        logger.error(e.__str__() + '数据库异常导致更新关于我失败')
        return ERR_DELETE_DB
