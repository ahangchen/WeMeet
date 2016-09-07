from student.db import stu_info
from student.db import job_apply
from team.db import job
from student.db.tag import OK_SELECT, ERR_SELECT_NOTEXIST, ERR_SELECT_DB, OK_INSERT,\
                           OK_UPDATE, ERR_UPDATE_NOTEXIST,\
                           NO_RESUME
from student.ctrl.tag import OK_SAVE_RESUME, ERR_SAVE_RESUME_FAIL, ERR_RESUME_FILE_INVALID, \
                             OK_APPLY, ERR_APPLY_DB, ERR_APPLY_NO_RESUME, ERR_APPLY_EXIST, \
                             OK_GET_RESUME, ERR_GET_RESUME_DB, ERR_GET_NO_RESUME, \
                             OK_DEL_RESUME, ERR_DEL_RESUME_DB
from student.util.logger import logger
from student.util import file_helper, date_helper
from student.util.value_update import NO_INPUT
import time


RESUME_PATH_ROOT = 'student/resume'


def upload(stu_id, resume):
    """
    上传简历文件
    @stu_id 学生id
    @resume: 简历文件
    成功：返回{'tag': OK_SAVE_RESUME, 'path': resume_path}
    失败：返回{'tag': ERR_SAVE_RESUME_FAIL}
    """

    def check_resume_file(file):  # TODO(hjf): Check resume file
        """return true if avatar file is valid"""
        return True

    def get_resume_path(folder, file_name, file_type):
        return '%s/%s/%s.%s' % (RESUME_PATH_ROOT, folder, file_name, file_type)

    # 确认学生是否存在
    select_rlt = stu_info.select(stu_id=stu_id)
    # 如果学生存在
    if select_rlt['tag'] == OK_SELECT:
        # 如果简历文件合法
        if check_resume_file(resume):
            pre_ref_path = select_rlt['stu'].resume_path
            resume_path = get_resume_path(folder=stu_id,
                                          file_name=int(time.time()),
                                          file_type=file_helper.get_file_type(resume.name))  # 用时间作简历文件名称
            ref_path = '/media/' + resume_path

            # 更新学生的当前简历路径
            update_stu_tag = stu_info.update(stu_id=stu_id, resume_path=ref_path)
            # 如果更新学生的当前简历路径成功：
            if update_stu_tag == OK_UPDATE:

                # 如果简历文件上传成功
                if file_helper.save(resume, resume_path):
                    return {'tag': OK_SAVE_RESUME,
                            'path': ref_path}
                # 如果简历文件上传失败，
                else:
                    logger.error('简历文件上传失败')
                    # 回滚
                    roll_tag = stu_info.update(stu_id=stu_id, resume_path=pre_ref_path)
                    if roll_tag != OK_UPDATE:
                        logger.error('简历文件上传失败，但学生的简历路径已更新，无法回滚')
                    return {'tag': ERR_SAVE_RESUME_FAIL}

            # 如果更新学生的当前简历路径时学生记录不存在
            elif update_stu_tag == ERR_UPDATE_NOTEXIST:
                logger.error('更新学生当前简历路径时，学生记录丢失，导致上传简历失败')
                return {'tag': ERR_SAVE_RESUME_FAIL}
            # 如果数据库异常导致无法更新学生的当前简历路径update_stu_tag == ERR_UPDATE_DB
            else:
                logger.error('数据库异常导致无法更新学生当前简历路径，上传简历失败')
                return {'tag': ERR_SAVE_RESUME_FAIL}

        # 如果简历不合法
        else:
            return {'tag': ERR_RESUME_FILE_INVALID}

    # 如果学生不存在
    elif select_rlt['tag'] == ERR_SELECT_NOTEXIST:
        logger.warning('尝试为不存在的学生上传简历')
        return {'tag': ERR_SAVE_RESUME_FAIL}
    # 如果数据库异常导致查询学生是否存在失败(select_rlt['tag'] == ERR_SELECT_DB)
    else:
        logger.error('数据库异常导致无法确定学生是否存在，上传简历失败')
        return {'tag': ERR_SAVE_RESUME_FAIL}


def apply(stu_id, job_id):
    """
    投递简历
    成功：返回{'tag': OK_APPLY, 'apply_id': insert_apply_rlt['apply'].id}
    失败：返回{'tag': ERR_APPLY_DB}
          或{’tag': ERR_APPLY_NO_RESUME}
    @stu_id:学生id
    @job_id:职位id
    """
    select_stu_rlt = stu_info.select(stu_id)
    # 如果学生存在
    if select_stu_rlt['tag'] == OK_SELECT:
        select_job_rlt = job.id_job(job_id)
        # 如果职位存在
        if select_job_rlt is not None:
            team = select_job_rlt.team  # team一定存在（由model外键的on_delete=CASCADE保证）
            stu = select_stu_rlt['stu']

            # 如果学生无简历
            if stu.resume_path == NO_RESUME:
                return {'tag': ERR_APPLY_NO_RESUME}

            # 如果学生有简历
            else:
                select_apply_rlt = job_apply.stu_job_select(stu=stu, job=select_job_rlt)
                # 如果尚未投递
                if select_apply_rlt['tag'] == ERR_SELECT_NOTEXIST:
                    insert_apply_rlt = \
                        job_apply.insert(stu=stu, job=select_job_rlt, state=0, team=team,
                                         apply_time=date_helper.curr_time(), resume_path=stu.resume_path,
                                         change_time=date_helper.now(), stu_read=True)

                    # 如果投递成功
                    if insert_apply_rlt['tag'] == OK_INSERT:
                        return {'tag': OK_APPLY,
                                'apply_id': insert_apply_rlt['apply'].apply_id}

                    # 如果投递失败insert_apply_rlt['tag'] == ERR_INSERT_DB
                    else:
                        logger.error('数据库异常导致投递记录插入失败，投递简历失败')
                        return {'tag': ERR_APPLY_DB}

                # 如果已经投递过了
                elif select_apply_rlt['tag'] == OK_SELECT:
                    return {'tag': ERR_APPLY_EXIST}

                # 如果数据库异常导致无法确认是否已经投递过了(select_apply_rlt['tag'] == ERR_SELECT_DB)
                else:
                    logger.error('数据库异常导致无法确认是否已经投递过，投递简历失败')
                    return {'tag': ERR_APPLY_DB}

        # 如果职位不存在(select_job_rlt is None)
        else:
            logger.warning('尝试投递简历给不存在的职位')
            return {'tag': ERR_APPLY_DB}

    # 如果学生不存在(select_stu_rlt['tag'] == ERR_SELECT_NOTEXIST)
    elif select_stu_rlt['tag'] == ERR_SELECT_NOTEXIST:
        logger.warning('尝试用不存在的学生投递简历')
        return {'tag': ERR_APPLY_DB}

    # 如果数据库异常导致无法确认学生是否存在(select_stu_rlt['tag'] == ERR_SELECT_DB)
    else:
        logger.error('数据库异常导致无法确认学生是否存在，投递简历失败')
        return {'tag': ERR_APPLY_DB}


def get(stu_id):
    """
    获取学生的简历路径
    成功：返回{'tag': OK_GET_RESUME, 'resume_path': select_rlt['stu'].resume_path}
    失败：返回{'tag': ERR_GET_RESUME_DB}
    """
    select_rlt = stu_info.select(stu_id)
    # 如果学生存在
    if select_rlt['tag'] == OK_SELECT:
        # 如果没有简历
        if select_rlt['stu'].resume_path == NO_RESUME:
            return {'tag': ERR_GET_NO_RESUME}

        # 如果成功
        return {'tag': OK_GET_RESUME,
                'resume_path': select_rlt['stu'].resume_path}

    # 如果学生不存在
    elif select_rlt['tag'] == ERR_SELECT_NOTEXIST:
        logger.warning('尝试获取不存在学生的简历路径')
        return {'tag': ERR_GET_RESUME_DB}

    # 如果数据库异常导致无法确认学生是否存在 select_rlt['tag'] == ERR_SELECT_DB
    else:
        logger.error('数据库异常导致无法确认学生是否存在，获取简历路径失败')
        return {'tag': ERR_GET_RESUME_DB}


def delete(stu_id):
    """
    删除简历（只删除学生信息的简历路径）
    成功：返回{'tag': OK_DEL_RESUME}
    失败：返回{'tag': ERR_DEL_RESUME_DB}
    """
    select_rlt = stu_info.select(stu_id)
    # 如果学生存在
    if select_rlt['tag'] == OK_SELECT:
        stu = select_rlt['stu']
        update_rlt = stu_info.update(stu_id=stu.id, resume_path=NO_RESUME)
        if update_rlt == OK_UPDATE:
            return {'tag': OK_DEL_RESUME}
        else:
            logger.error('数据库异常导致无法删除学生的简历（路径）')
            return {'tag': ERR_DEL_RESUME_DB}

    # 如果学生不存在
    elif select_rlt['tag'] == ERR_SELECT_NOTEXIST:
        logger.warning('尝试删除不存在学生的简历路径')
        return {'tag': ERR_DEL_RESUME_DB}

    # 如果数据库异常导致无法确认学生是否存在 select_rlt['tag'] == ERR_SELECT_DB
    else:
        logger.error('数据库异常导致无法确认学生是否存在，删除简历路径失败')
        return {'tag': ERR_DEL_RESUME_DB}


