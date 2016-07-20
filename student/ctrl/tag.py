OK_REG = 1
REG_FAIL_EXIST = -1
REG_FAIL_DB = -2

OK_ACTIVATE = 3
ERR_ACTIVATE_NOTEXIST = -3
ERR_ACTIVATE_DB = -4

OK_LOGIN = 5
ERR_LOGIN_NOTEXIST = -5  # 账号不存在
ERR_LOGIN_DB = -6
ERR_LOGIN_WRONG_PWD = -7
ERR_LOGIN_NONACTIVATED = -8  # 账号未激活

OK_RESET_MAIL = 9
ERR_RESET_MAIL_NOTEXIST = -9
ERR_RESET_MAIL_DB = -10

ERR_RESET_NOTEXIST = -11
ERR_RESET_DB = -12
ERR_RESET_OUT_DATE = -13

OK_CHANGE_PWD = 14
ERR_CHANGE_PWD_NOTEXIST = -14  # 账号不存在
ERR_CHANGE_PWD_WRONG_CREDENTIAL = -15  # 凭据错误
ERR_CHANGE_PWD_DB = -16

ERR_GET_INFO_NOTEXIST = -17  # 获取学生信息
ERR_GET_INFO_DB = -18  # 获取学生信息

OK_UPDATE_STU_INFO = 19  # 更新学生信息
ERR_UPDATE_STU_INFO_DB = -19  # 更新学生信息失败

OK_SAVE_AVATAR = 20
ERR_AVATAR_FILE_INVALID = -20
ERR_SAVE_AVATAR_FAIL = -21

OK_SAVE_RESUME = 22
ERR_RESUME_FILE_INVALID = -20
ERR_SAVE_RESUME_FAIL = -21





