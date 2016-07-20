from student.db import stu_info
from student.db.tag import OK_SELECT, ERR_SELECT_NOTEXIST, ERR_SELECT_DB
from student.ctrl.tag import OK_SAVE_RESUME, ERR_SAVE_RESUME_FAIL, ERR_RESUME_FILE_INVALID
from student.util.logger import logger
from student.util import file_helper


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

    def get_avatar_path(file_name, file_type):
        return '%s/%s.%s' % (RESUME_PATH_ROOT, file_name, file_type)

    # 确认学生是否存在
    select_rlt = stu_info.select(stu_id=stu_id)
    # 如果学生存在
    if select_rlt['tag'] == OK_SELECT:
        # 如果简历文件合法
        if check_resume_file(resume):
            resume_path = get_avatar_path(file_name=stu_id,
                                          file_type=file_helper.get_file_type(resume.name))  # 用学生id作简历文件名称

            # 如果简历文件上传成功
            if file_helper.save(resume, resume_path):
                return {'tag': OK_SAVE_RESUME,
                        'path': resume_path}
            # 如果简历文件上传失败，
            else:
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

