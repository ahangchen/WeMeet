SUCCEED = '0'

ERR_METHOD = '-1'
ERR_METHOD_MSG = '请求方法错误'

ERR_VALID_CODE = '-2'
ERR_VALID_CODE_MSG = '验证码错误'  # 用在注册

ERR_REG_IDEXIST = '-3'
ERR_REG_IDEXIST_MSG = '账号已存在'  # 用在注册

ERR_ACCOUNT_NOTEXIST = '-4'
ERR_ACCOUNT_NOTEXIST_MSG = '账号不存在'  # 用在邮件验证/登陆/重置密码的邮件的发送请求/修改密码

ERR_LOGIN_STU_WRONG_PWD = '-5'
ERR_LOGIN_STU_WRONG_PWD_MSG = '密码错误'
ERR_LOGIN_STU_NONACTIVATED = '-6'
ERR_LOGIN_STU_NONACTIVATED_MSG = '账号未激活'

ERR_WRONG_CREDENTIAL = '-7'
ERR_WRONG_CREDENTIAL_MSG = '凭据错误'  # 用在修改密码

ERR_STU_NOTEXIST = '-8'
ERR_STU_NOTEXIST_MSG = '学生不存在'  # 用在获取学生信息


FAIL = '-10'  # 数据库异常导致的失败
FAIL_MSG = '操作失败'

ERR_OUT_DATE = '-11'  # 用在通过邮件链接重置账号
ERR_OUT_DATE_MSG = '请求已过期'

AVATAR_INVALID = '-12'  # 用在保存头像
AVATAR_INVALID_MSG = '头像不合法'

RESUME_INVALID = '-14'
RESUME_INVALID_MSG = '简历文件不合法'

NO_RESUME = '-15'  # 用在简历投递
NO_RESUME_MSG = '未上传简历'

ERR_MULTI_APPLY = '-16'  # 用在简历投递
ERR_MULTI_APPLY_MSG = '多次投递同一职位'

NO_EDU = '-118'  # 用在获取教育经历
NO_EDU_MSG = '无教育经历'

NO_INTERN = '-119'  # 用在获取实习经历
NO_INTERN_MSG = '无实习经历'

NO_PROJ = '-120'  # 用在获取项目经历
NO_PROJ_MSG = '无项目经历'

NO_WORKS = '-121'  # 用再获取作品集
NO_WORKS_MSG = '无作品集'

NO_SKILL = '-122'  # 用在获取技能评价
NO_SKILL_MSG = '无技能评价'

ERR_EDU_FULL = '-123' # 用在增加教育经历
ERR_EDU_FULL_MSG = '教育经历已达上限'

ERR_INTERN_FULL = '-124' # 用在增加实习经历
ERR_INTERN_FULL_MSG = '实习经历已达上限'

ERR_PROJ_FULL = '-125' # 用在增加项目经历
ERR_PROJ_FULL_MSG = '项目经历已达上限'

ERR_SKILL_FULL = '-127' # 用在增加技能评
ERR_SKILL_FULL_MSG = '技能评价已达上限'

WORKS_INVALID = '-128'  # 用在上传作品集文件
WORKS_INVALID_MSG = '作品集不合法'

WORKS_EXIST = '-126'  # 用在增加作品集信息
WORKS_EXIST_MSG = '已有作品集'




# ERROR_LOGIN_STU_DOESNOTEXIST = '-5'
# ERROR_LOGIN_STU_DOESNOTEXIST_MSG = '账号不存在'  # 用以登陆

# ERROR_SEND_RSMAIL_DOESNOTEXIST = '-6'
# ERROR_SEND_RSMAIL_DOESNOTEXIST_MSG = '账号不存在'  # 用以重置密码的邮件的发送请求

# ERROR_CHANGE_PWD = '-93'
# ERROR_CHANGE_PWD_MSG = '账号不存在'  # 用以修改密码

# ERROR_UPDATE_STU_IDMISS = '-94'
# ERROR_UPDATE_STU_IDMISS_MSG = 'update err: post does not contain stu_id'
#
# ERROR_UPDATE_STU_AVATAR_SAVE_FAILED = '-95'
# ERROR_UPDATE_STU_AVATAR_SAVE_FAILED_MSG = 'update err: avatar file save failed'
#
# ERROR_UPDATE_STU_AVATAR_INVALID = '-96'
# ERROR_UPDATE_STU_AVATAR_INVALID_MSG = 'update err: avatar file invalid'
#
# ERROR_UPDATE_STU_DOESNOTEXIST = '-97'
# ERROR_UPDATE_STU_DOESNOTEXIST_MSG = 'update err: stu_id does not exist'
#
# ERROR_GET_STU_IDMISS = '-98'
# ERROR_GET_STU_IDMISS_MSG = 'get err: post does not contain stu_id'
#
# ERROR_GET_STU_DOESNOTEXIST = '-99'
# ERROR_GET_STU_DOESNOTEXIST_MSG = 'get err: stu_id does not exist'







