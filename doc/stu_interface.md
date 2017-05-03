##接口(学生部分)

***
### 1. 学生注册：  
* http://110.64.69.66:8081/student/register/
* POST  
* 参数：
    * account: 
    * pwd
    * code: 验证码
* 返回：  
    * 成功:
        * JSON: {"err": err} 
            * err: 0  
    * 失败：
        * JSON: {"err": err, "msg": msg}
            * err: -2/-3/-1/-10
            * msg: 验证码错误/账号已存在/请求方法错误/操作失败

***

### 2. 激活账号：（前端用不到）
* http://110.64.69.66:8081/student/activate/(cipher)
* GET
* 参数：
    * cipher： 加密的账号（由后端加密，只能通过邮件链接传递给前端）
* 返回：
    * 成功：
        * JSON: {"err": err}
            * err: 0
    * 失败：
        * JSON: {"err": err, "msg": msg}
            * err: -4/-1/-10
            * msg: 账号不存在/请求方法错误/操作失败

***

### 3. 登陆：
* http://110.64.69.66:8081/student/login/
* POST
* 参数：
    * account
    * pwd
* 返回：
    * 成功：
        * JSON: {"err": err, 'id': stu_id}
            * err: 0
            * id: 对应的学生id 
    * 失败：
        * JSON: {"err": err, "msg": msg}
            * err: -4/-5/-6/-1/-10
            * msg: 账号不存在/密码错误/账号未激活/请求方法错误/操作失败

***

### 4. 请求发送密码重置邮件
* http://110.64.69.66:8081/student/rsmail/ 　　　（rsmail: reset mail)
* POST
* 参数：
    * account
* 返回：
    * 成功：
        * JSON: {"err": err}
            * err: 0
    * 失败：
        * JSON: {"err": err, "msg": msg}
            * err: -4/-1/-10
            * msg: 账号不存在/请求方法错误/操作失败

***

### 5. 获取找回密码的凭证（同时重置密码，修改账号状态为未激活）
* http://110.64.69.66:8081/student/reset/
* POST
* 参数：
    * account： 加密的账号（由后端加密，只能通过邮件链接传递给前端）
* 返回：
    * 成功：
        * JSON: {"err": err, "credential": credential, "account": account}
            * err: 0
            * credential： 凭据
            * account : 无加密的账号
    * 失败：
        * JSON: {"err": err, "msg": msg}
            * err: -4/-11/-1/-10
            * msg: 账号不存在/请求已过期/请求方法错误/操作失败

***

### 6. 修改密码
* http://110.64.69.66:8081/student/cpwd/
* POST
* 参数：
    * account:
    * credential: 凭据
    * pwd
* 返回：
    * 成功：
        * JSON: {"err": err}
            * err: 0
    * 失败：
        * JSON: {"err": err, "msg": msg}
            * err: -4/-7/-1/-10
            * msg: 账号不存在/凭据错误/请求方法错误/操作失败

***

### 7. 获取学生信息
* http://110.64.69.66:8081/student/info/get/
* POST
* 参数：
    * id： 学生id（由登陆获得）
* 返回：
    * 成功：
        * JSON: 　　{  
        　　　　　"err": err,  
        　　　　　"avatar_pah": avatar_path,   
        　　　　　"name": name,     
        　　　　　"title": title,  
        　　　　　"personal_signature": personal_signature,  
        　　　　　"sex": sex,  
        　　　　　"school": school,  
        　　　　　"grade": grade,  
        　　　　　"is_engineering": is_engineering,     
        　　　　　"is_literature": is_literature,     
        　　　　　"is_management": is_management,     
        　　　　　"is_humanity": is_humanity,     
        　　　　　"likes": likes  
        　　　　}  

            * err: 0
            * sex: 性别 -1(未填) 0(男) 1(女)  
            * title: 头衔 
            * personal_signature：个性签名
            * grade: 年级 -1(未填)，0(大一) 1(大二) 2(大三) 3(大四) 4(研一) 5(研二) 6(研三) 7(博士)
            * is_engineering：0(未选) 1(选定)
            * is_literature 0(未选) 1(选定)
            * is_management 0(未选) 1(选定)
            * his_humanity 0(未选) 1(选定)
            * likes： 人气
            
    * 失败：
        * JSON: {"err": err, "msg": msg}
            * err: -8/-1/-10
            * msg: 学生不存在/请求方法错误/操作失败

***

### 8. 上传头像
* http://110.64.69.66:8081/student/info/avatar/
* POST
* 参数：
    * id: 学生id（由登陆获得）
    * avatar： 头像文件
* 返回：
    * 成功：
        * JSON: {'err': err, 'path': avatar_path}
            * err: 0
            * path: 头像路径
    * 失败
        * JSON: {'err': err, 'msg': msg}
            * err: -12/-1/-10
            * msg: 头像不合法/请求方法错误/操作失败

***

### 9. 修改学生信息
* http://110.64.69.66:8081/student/info/update/
* POST
* 参数： 
    * stu_id:
    * name 
    * title 
    * personal_signature  
    * sex: 性别 0表示未填，1表示男，2表示女 
    * school:  
    * grade: 年级 -1(未填)，0(大一) 1(大二) 2(大三) 3(大四) 4(研一) 5(研二) 6(研三) 7(博士) 
    * avatar_path  
    * is_engineering: 0(未选) 1(选定)
    * is_literature： 0(未选) 1(选定)  
    * is_management： 0(未选) 1(选定)  
    * is_humanity： 0(未选) 1(选定)  
* 返回： 
    * 成功：
        * JSON: {"err": err}
            * err: 0
    * 失败：
        * JSON: {"err": err, "msg": msg}
            * err: -1/-10
            * msg： 请求方法错误/操作失败

***

### 10. 上传简历
* http://110.64.69.66:8081/student/resume/upload/
* POST
* 参数：
    * id: 学生id
    * resume： 简历文件
* 返回：
    * 成功：
        * JSON： {"err": err, "path": resume_path}
            * err: 0
            * path: 简历文件的路径
    * 失败：
        * JSON： {"err": err, "msg": msg}
            * err: -14/-1/10
            * msg: 简历文件不合法/请求方法错误/操作失败

***

### 11. 投递简历
* http://110.64.69.66:8081/student/resume/apply/
* POST
* 参数：
    * stu_id: 学生id
    * job_id: 职位id
* 返回：
    * 成功：
        * JSON： {"err": err, "apply_id": job_apply_id}
            * err: 0
            * apply_id: 投递记录的id 
    * 失败：
        * JSON： {"err": err, "msg": msg}
            * err: -15/-16/-1/10
            * msg: 未上传简历/多次投递同一职位/请求方法错误/操作失败

***

### 12. 查询简历
* http://110.64.69.66:8081/student/resume/get/
* POST
* 参数：
    * stu_id: 学生id
* 返回：
    * 成功：
        * JSON： {"err": err, "path": resume_path}
            * err: 0
            * resume_path: 简历的路径
    * 失败：
        * JSON： {"err": err, "msg": msg}
            * err: -15/-1/10
            * msg: 未上传简历/请求方法错误/操作失败

***

### 12.1. 删除简历
* http://110.64.69.66:8081/student/resume/del/
* POST
* 参数：
    * stu_id: 学生id
* 返回：
    * 成功：
        * JSON： {"err": err}
            * err: 0
    * 失败：
        * JSON： {"err": err, "msg": msg}
            * err: -1/10
            * msg: 请求方法错误/操作失败

***

### 13. 查询教育经历
* http://110.64.69.66:8081/student/info/edu/get/
* POST
* 参数：
    * stu_id: 学生id
* 返回：
    * 成功：
        * JSON： {"err": err,  "grade": grade,  "edu_background": edu_background,    
        　　　"edu_list": [{  
            　　　　　"edu_id": edu_id,  
            　　　　　"major": major,   
            　　　　　"graduation_year": graduation_year,   
            　　　　　"edu_background": edu_background,   
            　　　　　"school": school},  
            　　　...]}
            * err: 0
            * grade: 个人信息中的年级
            * edu_background: 个人信息中的学历 
            * edu_list.edu_id: 教育经历记录的id
            * edu_list.major: 教育经历的专业
            * edu_list.graduation_year: 教育经历的毕业年份 
            * edu_list.edu_background: 教育经历的学历 
            * edu_list.school: 教育经历的学校
    * 失败：
        * JSON： {"err": err, "msg": msg}
            * err: -118/-1/-10
            * msg: 无教育经历/请求方法错误/操作失败
            
***

### 14. 查询实习经历
* http://110.64.69.66:8081/student/info/intern/get/
* POST
* 参数：
    * stu_id: 学生id
* 返回：
    * 成功：
        * JSON： {"err": err,    
        　　　　"intern_list": [{  
            　　　　　　"intern_id": intern_id,  
            　　　　　　"company": company,   
            　　　　　　"position": position,   
            　　　　　　"begin_time": begin_time,   
            　　　　　　"end_time": end_time,  
            　　　　　　"description": description},  
            　　　...]}
            * err: 0
            * intern_list.intern_id: 实习经历记录的id 
            * intern_list.company: 公司
            * intern_list.position: 职位
            * intern_list.begin_time: 开始时间
            * intern_list.end_time: 结束时间
            * intern_list.description: 职能描述
    * 失败：
        * JSON： {"err": err, "msg": msg}
            * err: -119/-1/-10
            * msg: 无实习经历/请求方法错误/操作失败
            
***

### 15. 查询项目经历
* http://110.64.69.66:8081/student/info/proj/get/
* POST
* 参数：
    * stu_id: 学生id
* 返回：
    * 成功：
        * JSON： {"err": err,    
        　　　　"proj_list": [{  
            　　　　　　"proj_id": proj_id,  
            　　　　　　"name": name,   
            　　　　　　"duty": duty,   
            　　　　　　"year": year,     
            　　　　　　"description": description},  
            　　　...]}
            * err: 0
            * proj_id: 项目经历记录的id 
            * name: 项目名称
            * duty: 职责
            * year: 项目年份 
            * description: 项目简述
    * 失败：
        * JSON： {"err": err, "msg": msg}
            * err: -120/-1/-10
            * msg: 无项目经历/请求方法错误/操作失败
                        
***

### 16. 查询作品集
* http://110.64.69.66:8081/student/info/works/get/
* POST
* 参数：
    * stu_id: 学生id
* 返回：
    * 成功：
        * JSON：  
        {  
        　　"err": err,  
        　　"works_list":  
        　　[{  
        　　　　"works_id": works_id,  
        　　　　"name": name,  
        　　　　"url": url,  
        　　　　"description": description,  
        　　　　"img": img,  
        　　　　"audio": audio,  
        　　　　"video": video,    
        　　},...]  
        }
            * err: 0
            * works_id: 作品集记录的id 
            * img: 作品文件的路径，可能为空
            * audio: 作品文件的路径，可能为空
            * video: 作品文件的路径，可能为空
                * 仅有一个不为空
    * 失败：
        * JSON： {"err": err, "msg": msg}
            * err: -121/-1/-10
            * msg: 无作品集/请求方法错误/操作失败

***

### 17. 查询技能评价
* http://110.64.69.66:8081/student/skill/get/
* POST
* 参数：
    * stu_id: 学生id
* 返回：
    * 成功：
        * JSON： {"err": err,    
        　　　　"skill_list": [{  
            　　　　　　"skill_id": skill_id,  
            　　　　　　"name": name,   
            　　　　　　"value": value},  
            　　　...]}
            * err: 0
            * skill_id: 技能评价记录的id 
            * name: 技能名称
            * value: 技能评价的值 
    * 失败：
        * JSON： {"err": err, "msg": msg}
            * err: -122/-1/-10
            * msg: 无技能评价/请求方法错误/操作失败

***                                   

### 18. 增加教育经历
* http://110.64.69.66:8081/student/info/edu/add/
* POST
* 参数：
    * stu_id: 学生id
    * major: 专业
    * graduation_year: 毕业年份
    * edu_background: 学历（0表示其他，1表示大专，2表示本科，3表示硕士，4表示博士） 
    * school: 学校
* 返回：
    * 成功：
        * JSON： {"err": err, "edu_id": edu_id, "grade": grade, "edu_background": edu_background}
            * err: 0
            * edu_id: 增加的教育经历记录的id 
            * grade: 个人信息中的年级
            * edu_background: 个人信息中的学历学历（0表示其他，1表示大专，2表示本科，3表示硕士，4表示博士） 
    * 失败：
        * JSON： {"err": err, "msg": msg}
            * err: -123/-1/-10
            * msg: 教育经历已达上限/请求方法错误/操作失败

***

### 19. 更新教育经历
* http://110.64.69.66:8081/student/info/edu/update/
* POST
* 参数：
    * stu_id
    * edu_id: 
    * major: 专业
    * graduation_year: 毕业年份
    * edu_background: 学历（0表示其他，1表示大专，2表示本科，3表示硕士，4表示博士）
    * school: 学校
* 返回：
    * 成功：
        * JSON： {"err": err, "grade": grade, "edu_background": edu_background}
            * err: 0
            * grade: 个人信息中的年级
            * edu_background: 个人信息中的学历 
    * 失败：
        * JSON： {"err": err, "msg": msg}
            * err: -1/-10
            * msg: 请求方法错误/操作失败

***

### 20. 增加实习经历
* http://110.64.69.66:8081/student/info/intern/add/
* POST
* 参数：
    * stu_id: 学生id
    * company: 公司
    * position: 职位
    * begin_time: 开始时间
    * end_time: 结束时间
    * description: 职能描述
* 返回：
    * 成功：
        * JSON： {"err": err, "intern_id": intern_id}
            * err: 0
            * intern_id: 增加的实习经历记录的id 
    * 失败：
        * JSON： {"err": err, "msg": msg}
            * err: -124/-1/-10
            * msg: 实习经历已达上限/请求方法错误/操作失败
        
***

### 21. 更新实习经历
* http://110.64.69.66:8081/student/info/intern/update/
* POST
* 参数：
    * stu_id
    * intern_id: 
    * company: 公司
    * position: 职位
    * begin_time: 开始时间
    * end_time: 结束时间
    * description: 职能描述
* 返回：
    * 成功：
        * JSON： {"err": err}
            * err: 0
    * 失败：
        * JSON： {"err": err, "msg": msg}
            * err: -1/-10
            * msg: 请求方法错误/操作失败

***

### 22. 增加项目经历
* http://110.64.69.66:8081/student/info/proj/add/
* POST
* 参数：
    * stu_id: 学生id
    * name: 项目名称
    * duty: 职责
    * year: 项目年份
    * description: 项目简述
* 返回：
    * 成功：
        * JSON： {"err": err, "proj_id": proj_id}
            * err: 0
            * proj_id: 增加的项目经历记录的id 
    * 失败：
        * JSON： {"err": err, "msg": msg}
            * err: -125/-1/-10
            * msg: 项目经历已达上限/请求方法错误/操作失败

***

### 23. 更新项目经历
* http://110.64.69.66:8081/student/info/proj/update/
* POST
* 参数：
    * stu_id
    * proj_id: 
    * name: 项目名称
    * duty: 职责
    * year: 项目年份
    * description: 项目简述
* 返回：
    * 成功：
        * JSON： {"err": err}
            * err: 0
    * 失败：
        * JSON： {"err": err, "msg": msg}
            * err: -1/-10
            * msg: 请求方法错误/操作失败

***

### 24. 增加作品集
* http://110.64.69.66:8081/student/works/add/
* POST
* 参数：
    * stu_id: 学生id
    * name: 作品名
    * duty: 职责
    * url: 作品的url
    * description: 描述
    * img: 图片，无则为空
    * audio: 音频，无则为空
    * video: 视频，无则为空 
        * 三个仅有一个不为空
* 返回：
    * 成功：
        * JSON： {"err": err, "works_id": works_id}
            * err: 0
            * works_id: 增加的作品集的id 
    * 失败：
        * JSON： {"err": err, "msg": msg}
            * err: -126/-1/-10
            * msg: 作品数量已满/请求方法错误/操作失败

***

### 25. 更新作品集
* http://110.64.69.66:8081/student/works/update/
* POST
* 参数：
    * stu_id
    * works_id: 
    * name: 作品名
    * duty: 职责
    * url: 作品的url
    * description: 描述
    * img: 图片，无则为空
    * audio: 音频，无则为空
    * video: 视频，无则为空
        * 三个仅有一个不为空
* 返回：
    * 成功：
        * JSON： {"err": err}
            * err: 0
    * 失败：
        * JSON： {"err": err, "msg": msg}
            * err: -1/-10
            * msg: 请求方法错误/操作失败

***

### 26. 增加技能评价
* http://110.64.69.66:8081/student/skill/add/
* POST
* 参数：
    * stu_id: 学生id
    * name: 技能名称
    * value: 技能评价的值
* 返回：
    * 成功：
        * JSON： {"err": err, "skill_id": skill_id}
            * err: 0
            * skill_id: 增加的技能评价的id 
    * 失败：
        * JSON： {"err": err, "msg": msg}
            * err: -127/-1/-10
            * msg: 技能评价已达上限/请求方法错误/操作失败

***

### 27. 更新技能评价
* http://110.64.69.66:8081/student/skill/update/
* POST
* 参数：
    * stu_id
    * skill_id: 
    * name: 技能名称
    * value: 技能评价的值
* 返回：
    * 成功：
        * JSON： {"err": err}
            * err: 0
    * 失败：
        * JSON： {"err": err, "msg": msg}
            * err: -1/-10
            * msg: 请求方法错误/操作失败

***

### 28. 上传作品集
* http://110.64.69.66:8081/student/works/upload/
* POST
* 参数：
    * stu_id: 学生id
    * works： 作品集文件
* 返回：
    * 成功：
        * JSON： {"err": err, "path": works_path}
            * err: 0
            * path: 作品集的路径
    * 失败：
        * JSON： {"err": err, "msg": msg}
            * err: -128/-1/10
            * msg: 作品集文件不合法/请求方法错误/操作失败

***

### 29. 删除教育经历
* http://110.64.69.66:8081/student/info/edu/del/
* POST
* 参数：
    * stu_id: 
    * edu_id: 
* 返回：
    * 成功：
        * JSON： {"err": err, "grade": grade, "edu_background": edu_background}
            * err: 0
            * grade: 个人信息中的年级
            * edu_background: 个人信息中的学历
        * JSON: {"err": err}
            * err: 1 (表示成功删除学生的最后一条教育经历）
    * 失败：
        * JSON： {"err": err, "msg": msg}
            * err: -1/-10
            * msg: 请求方法错误/操作失败

***

### 30. 删除实习经历
* http://110.64.69.66:8081/student/info/intern/del/
* POST
* 参数：
    * stu_id
    * intern_id: 
* 返回：
    * 成功：
        * JSON： {"err": err}
            * err: 0
    * 失败：
        * JSON： {"err": err, "msg": msg}
            * err: -1/-10
            * msg: 请求方法错误/操作失败

***

### 31. 删除项目经历
* http://110.64.69.66:8081/student/info/proj/del/
* POST
* 参数：
    * stu_id:
    * proj_id: 
* 返回：
    * 成功：
        * JSON： {"err": err}
            * err: 0
    * 失败：
        * JSON： {"err": err, "msg": msg}
            * err: -1/-10
            * msg: 请求方法错误/操作失败

***

### 32. 删除作品集
* http://110.64.69.66:8081/student/works/del/
* POST
* 参数：
    * stu_id
    * works_id: 
* 返回：
    * 成功：
        * JSON： {"err": err}
            * err: 0
    * 失败：
        * JSON： {"err": err, "msg": msg}
            * err: -1/-10
            * msg: 请求方法错误/操作失败

***

### 33. 删除技能评价
* http://110.64.69.66:8081/student/skill/del/
* POST
* 参数：
    * stu_id
    * skill_id: 
* 返回：
    * 成功：
        * JSON： {"err": err}
            * err: 0
    * 失败：
        * JSON： {"err": err, "msg": msg}
            * err: -1/-10
            * msg: 请求方法错误/操作失败

***

### 34. 获取投递列表(学生）
* http://110.64.69.66:8081/student/apply/list/
* POST
* 参数：
    * stu_id: 学生id
    * state: 投递状态，0表示待查看，1表示待沟通，2表示待面试，3表示录用， 4表示不合适，5表示全部
* 返回：
    * 成功：
        * JSON: {"err": err,  
         　　　"apply_list": [{   
        　　　　　"apply_id": apply_id,  
        　　　　　"state": state  
        　　　　　"job_id": job_id,  
        　　　　　"is_read": is_read,    
        　　　　　"job_name": job_name,  
        　　　　　"prince": prince,  
        　　　　　"city": city,  
        　　　　　"town": town,  
        　　　　　"address": address,  
        　　　　　"team_name": team_name,  
        　　　　　"min_salary": min_salary,  
        　　　　　"max_salary": max_salary,  
        　　　　　"change_time": change_time,  
        　　　　　"contact": leader,  
         　　　　　"mail": mail},...  
        　　　　]}
        * err: 0
        * is_read: 0表示未读，1表示已读， 
        * team_name: 公司
        * change_time: 状态更改时间
        * contact: 联系人名字（待查看和不合适时为"")
        * mail： 联系邮箱（待查看和不合适时为"")
    * 失败：
        * 返回：
            * JOSN: {"err": err, "msg": msg}
                * err: -129/-1/-10
                * msg: 无投递记录/请求方法错误/操作失败

***

### 35. 标记投递纪录为已读(学生)
* http://110.64.69.66:8081/student/apply/read/
* POST
* 参数：
    * apply_list: apply_id的数组
* 返回：
    * 成功：
        * JSON: {"err": err}
        * err: 0
    * 失败：
        * 返回：
            * JOSN: {"err": err, "msg": msg}
                * err: -1/-10
                * msg: 请求方法错误/操作失败

***

### 36. 获取投递列表(团队）
* http://110.64.69.66:8081/team/apply/list/
* POST
* 参数：
    * team_id: 团队id
    * state: 投递状态，0表示新接收，1表示待沟通，2表示待面试，3表示完成
* 返回：
    * 成功：
        * JSON: {"err": err,  
        　　　"unread_num": num  
         　　　"apply_list": [{   
        　　　　　"apply_id": apply_id,  
        　　　　　"state": state  
        　　　　　"job_id": job_id,  
        　　　　　"stu_id": stu_id,    
        　　　　　"job_name": job_name,  
        　　　　　"stu_name": stu_name,  
        　　　　　"apply_time": apply_time,  
        　　　　　"is_read": is_read},...  
        　　　　]}
        * err: 0
        * unread_num: 待查看投递数量 
        * apply_time: 投递时间
        * is_read: 0表示未读，1表示已读
        * state: 0表示新接收，1表示待沟通，2表示待面试，3表示录用， 4表示不合适
    * 失败：
        * 返回：
            * JOSN: {"err": err, "msg": msg}
                * err: -129/-1/-10
                * msg: 无投递记录/请求方法错误/操作失败

***

### 37. 查看投递(团队)  
* http://110.64.69.66:8081/team/apply/info/
* POST
* 参数：
    * apply_id: 
* 返回：
    * 成功：
        * JSON：  　{"err": err,   
            　　　　　"stu_id": stu_id,   
            　　　　　"name": name,   
            　　　　　"avatar_pah": avatar_path,   
            　　　　　"sex": sex,   
            　　　　　"age": age,   
            　　　　　"mail": mail,   
            　　　　　"tel": tel,  
            　　　　　"school": school,  
            　　　　　"major": major,  
            　　　　　"location": location,  
            　　　　　"resume_path": resume_path,  
            　　　　　"state": state}
            
            * state: 0表示待查看，1表示待沟通，2表示待面试，3表示录用， 4表示不合适

    * 失败：
        * JSON： {"err": err, "msg": msg}
            * err: -1/-10
            * msg: 请求方法错误/操作失败
        
***

### 38. 发送邮件通知(团队）
* http://110.64.69.66:8081/team/apply/mail/
* POST
* 参数：
    * apply_id
    * text：内容
 * 返回：
    * 成功：
        * JSON： {"err": err}
            * err: 0
   * 失败：
        * JSON： {"err": err, "msg": msg}
            * err: -1/-10
            * msg: 请求方法错误/操作失败  

***

### 39. 处理投递(团队）
* http://110.64.69.66:8081/team/apply/handle/
* POST
* 参数：
    * apply_id: 
    * state：投递状态，1表示待沟通，2表示待面试，3表示录用， 4表示不合适，
 * 返回：
    * 成功：
        * JSON： {"err": err}
            * err: 0

   * 失败：
        * JSON： {"err": err, "msg": msg}
            * err: -1/-10
            * msg: 请求方法错误/操作失败  

***

### 40. 广场获取人气最高的6个学生
* http://110.64.69.66:8081/student/top6/
* GET
* 参数：无
 * 返回：
    * 成功：
        * JSON  
        {  
        　　"err": err,  
        　　"top_list":  
        　　[{  
        　　　　"stu_id": stu_id,   
        　　　　"name": name,  
        　　　　"title": title,   
        　　　　"personal_signature": personal_signature,  
        　　　　"avatar_path": avatar_pah,  
        　　　　"skill_list":  
        　　　　[{  
            　　　　　"skill_id": skill_id,  
            　　　　　"name": name,  
            　　　　　"value": value  
        　　　　},...]  
        　　},...]}
            * err: 0
            * top_list：学生列表
            * title: 头衔
            * name: 学生姓名
            * personal_signature: 个性签名
            * skill_list: 二级标签的列表
                * skill_list.name: 技能的名字
                * skill_list.value: 技能的评价值（0-10）

   * 失败：
        * JSON： {"err": err, "msg": msg}
            * err: -1/-10
            * msg: 请求方法错误/操作失败  

***

### 41. 广场获取标签内人气最高的6个学生
* http://110.64.69.66:8081/student/top6/label/
* POST
* 参数：
     label: 0表示工程，1表示经管，2表示文艺，3表示人文
 * 返回：
    * 成功：
        * JSON：   
        {  
        　　"err": err,  
        　　"top_list":  
        　　[{  
        　　　　"stu_id": stu_id,   
        　　　　"name": name,  
        　　　　"title": title,   
        　　　　"personal_signature": personal_signature,  
        　　　　"avatar_path": avatar_pah,  
        　　　　"skill_list":  
        　　　　[{  
            　　　　　"skill_id": skill_id,  
            　　　　　"name": name,  
            　　　　　"value": value  
        　　　　},...]  
        　　},...]}
            * err: 0
            * top_list：学生列表
            * title: 头衔
            * name: 学生姓名
            * personal_signature: 个性签名
            * skill_list: 二级标签的列表
                * skill_list.name: 技能的名字
                * skill_list.value: 技能的评价值（0-10）

   * 失败：
        * JSON： {"err": err, "msg": msg}
            * err: -1/-10
            * msg: 请求方法错误/操作失败  

***

### 42. 获取关于我
* http://110.64.69.66:8081/student/aboutme/get/
* POST
* 参数：
     stu_id:
 * 返回：
    * 成功：
        * JSON：   
        {  
        　　"err": err,  
        　　"about_me_list":  
        　　[{  
        　　　　"about_me_id": about_me_id,  
        　　　　"title": title,  
        　　　　"text": text  
        　　},...]  
        }
            * err: 0
            * title: 自我描述的标题
            * text: 自我描述的内容

   * 失败：
        * JSON： {"err": err, "msg": msg}
            * err: -1/-10
            * msg: 请求方法错误/操作失败  



### 43. 更新关于我
* http://110.64.69.66:8081/student/aboutme/update/
* POST
* 参数：
    * stu_id
    * about_me_id: 
    * title: 
    * text: 
* 返回：
    * 成功：
        * JSON： {"err": err}
            * err: 0
    * 失败：
        * JSON： {"err": err, "msg": msg}
            * err: -1/-10
            * msg: 请求方法错误/操作失败

***

### 44. 添加关于我
* http://110.64.69.66:8081/student/aboutme/add/
* POST
* 参数：
    * stu_id: 
    * title: 
    * text: 
* 返回：
    * 成功：
        * JSON： {"err": err, "about_me_id": about_me_id}
            * err: 0 
    * 失败：
        * JSON： {"err": err, "msg": msg}
            * err: -1/-10
            * msg: 请求方法错误/操作失败

***

### 45. 删除关于我
* http://110.64.69.66:8081/student/aboutme/del/
* POST
* 参数：
    * about_me_id: 
    * stu_id: 
* 返回：
    * 成功：
        * JSON： {"err": err}
            * err: 0 
    * 失败：
        * JSON： {"err": err, "msg": msg}
            * err: -1/-10
            * msg: 请求方法错误/操作失败
