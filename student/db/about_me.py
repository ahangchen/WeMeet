from student.db.tag import OK_UPDATE
from student.db.tag import ERR_UPDATE_DB
from student.db.tag import OK_SELECT


from student.models import StuAboutMe

from student.util.logger import logger


def stu_select(stu_id):
    """
    成功：返回{'tag': OK_SELECT, 'about_me': selected}
    """
    selected = StuAboutMe.objects.all().filter(stu_id=stu_id)
    return {'tag': OK_SELECT, 'about_me': selected}


def update(about_me_id, title, text, stu_id):
    """
    成功:返回OK_UPDATE
    失败:返回ERR_UPDATE_DB
    """
    try:
        updated = StuAboutMe.objects.all().get(about_me_id=about_me_id, stu_id=stu_id)

        updated.title = title
        updated.text = text
        updated.save()
        return OK_UPDATE

    except StuAboutMe.DoesNotExist:
        logger.warning("尝试用不匹配的stu_id和about_me_id更新关于我")
        return ERR_UPDATE_DB
    except Exception as e:
        logger.error(e.__str__() + '数据库异常导致更新关于我失败')
        return ERR_UPDATE_DB
