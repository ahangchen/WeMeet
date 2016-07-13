##接口(学生部分)

***
###注册：  
* http://127.0.0.1:8000/student/register/  
* POST  
* 参数：
    * account: 
    * pwd
    * code: 验证码
* 返回：  
    * 成功：
        * err: 0  
    * 失败：
        * err: -2/-3/-1
        * msg: 验证码错误/账号已存在/请求方法错误

***

###激活账号：
* http://127.0.0.1:8000/student/activate/
* POST
* 参数：
    * account： 加密的账号（由后端加密，只能通过邮件链接传递给前端）
* 返回：
    * 成功：
        * err: 0
    * 失败：
        * err: -4/-1
        * msg: 账号不存在/请求方法错误

***

###登陆：
* http://127.0.0.1:8000/student/login/
* POST
* 参数：
    * account
    * pwd
* 返回：
    * 成功：
        * err: 0
    * 失败：
        * err: -4/-5/-6/-1
        * msg: 账号不存在/密码错误/账号未激活/请求方法错误

***

###请求发送密码重置邮件
* http://127.0.0.1:8000/student/rsmail/　　　　　（rsmail: reset mail)
* POST
* 参数：
    * account
* 返回：
    * 成功：
        * err: 0
    * 失败：
        * err: -4/-1
        * msg: 账号不存在/请求方法错误

***

###获取找回密码的凭证（同时重置密码，修改账号状态为未激活）
* http://127.0.0.1:8000/student/reset/
* POST
* 参数：
    * account： 加密的账号（由后端加密，只能通过邮件链接传递给前端）
* 返回：
    * 成功：
        * err: 0
        * credential： 凭据
        * account : 无加密的账号
    * 失败：
        * err: -4/-1
        * msg: 账号不存在/请求方法错误

***

###修改密码
* http://127.0.0.1:8000/student/cpwd/
* POST
* 参数：
    * account:
    * credential: 凭据
    * pwd
* 返回：
    * 成功：
        * err: 0
    * 失败：
        * err: -4/-7/-1
        * msg: 账号不存在/凭据错误/请求方法错误

***

###获取学生信息
* http://127.0.0.1:8000/student/info/
* POST
* 参数：
    * account
* 返回：
    * 成功：
        * err: 0
        * avatar_path
        * name
        * school
        * edu_background
        * grade
        * major
        * loaction
        * tel
        * mail
    * 失败：
        * err: -8/-1
        * msg: 学生不存在/请求方法错误


