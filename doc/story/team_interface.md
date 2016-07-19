##接口(团队部分)

### 团队注册  
* http://110.64.69.66:8081/team/register/
* POST  
* 参数：
    * mail: 用于注册的邮箱
    * pwd:密码的hash值
    * inv_code:邀请码
    * code: 验证码
* 返回：  
    * 成功:
        * JSON: {"err": err, "msg": "操作成功"} 
            * err: 0  
            * msg：操作成功提示
    * 失败：
        * JSON: {"err": err, "msg": msg}
            * err: -4/-2/-1/-10
            * msg: 邀请码或账号不正确/验证码错误/请求方法错误/操作失败

***

### 团队账号不需要发邮件激活 

### 团队登陆：
* http://110.64.69.66:8081/team/login/
* POST
* 参数：
    * mail：用户邮箱
    * pwd：密码hash
* 返回：
    * 成功:
        * JSON: {"err": err, "msg": "团队id"} 
            * err: 0  
            * msg： 团队id
    * 失败：
        * JSON: {"err": err, "msg": msg}
            * err: -4/-5/-1/-10
            * msg: 账号或密码错误/账号不可用/请求方法错误/操作失败

***

###请求发送密码重置邮件
* http://110.64.69.66:8081/team/reset/
* POST
* 参数：
    * mail：被重置的账号的邮箱 
* 返回：
    * 成功:
        * JSON: {"err": err, "msg": "操作成功"} 
            * err: 0  
            * msg：操作成功提示
    * 失败：
        * JSON: {"err": err, "msg": msg}
            * err: -4/-1/-10
            * msg: 账号不存在/请求方法错误/操作失败

***

###获取找回密码的凭证（这是一个邮件里的链接，点击进入重置密码页面，这个页面由后端生成）
* http://110.64.69.66:8081/team/fetch?reset_key=xxxxxxx&mail=xxxxx
* POST
* 参数：
    * reset_key： 加密的账号（由后端加密，只能通过邮件链接传递给前端）
    * mail：账号邮箱
* 返回：
    * 重置密码页面 

***

###修改密码
* http://110.64.69.66:8081/team/update_pwd/
* POST
* 参数：
    * mail:账号id
    * key: 凭据
    * pwd:新密码hash值
* 返回：
    * 成功:
        * JSON: {"err": err, "msg": "操作成功"} 
            * err: 0  
            * msg：操作成功提示
    * 失败：
        * JSON: {"err": err, "msg": msg}
            * err: -4/-1/-10
            * msg: 账号或凭据错误/请求方法错误/其他错误

***

***
##搜索模块
使用haystack搜索架构，并使用Whoosh搜索引擎，jieba做中文分词
入门教程： http://www.jianshu.com/p/5073e25de698
官方文档： http://django-haystack.readthedocs.io/en/latest/toc.html
***

***
###搜索模块：
* http://110.64.69.66:8081/team/search/
* POST
* 参数：
    * model: job（职位）、team（团队）、项目（product）
    * type：对应每种model的不同type类型
    * keys:
* 返回：
    * 成功:
        JSON: {"err": 0, "msg": 结果列表}
        当model = job时：
            pk:对应的ID
            job_name
            job_type
            min_salary
            max_salary
            job_summary
            team_name
            team_type
            team_about
            team_id
            team_logo_path

        当model = team时：
            pk:对应的ID
            team_name
            team_logo
            team_about
            team_type

        当model = product时：
            pk:对应的ID
            product_name
            product_content
            product_img_path
            team_name
            team_type
            team_about
            team_id
            team_logo_path
    * 失败：
        * JSON: {"err": err, "msg": msg}
            * err: -1
            * msg: 请求方法错误/查询类型错误

***

***
###热门团队模块：
* http://110.64.69.66:8081/team/hot_team/
* GET
* 返回：
    * 成功:
        JSON: {"err": 0, "msg": 团队列表}
        msg：
            id: 团队ID
            name: 团队名
            about: 团队简介
            logo_path: 团队logo地址
    * 失败：
        * JSON: {"err": err, "msg": msg}
***

***
###热门项目模块：
* http://110.64.69.66:8081/team/hot_product/
* GET
* 返回：
    * 成功:
        JSON: {"err": 0, "msg": 项目列表}
        msg：
            id: 项目ID
            name: 项目名
            content: 项目简介
            img_path: 项目logo地址
    * 失败：
        * JSON: {"err": err, "msg": msg}
***

### 职位编辑
- http://110.64.69.66:8081/team/job_update/
- post
- 参数：
  - job_id:职位id
  - job_name：职位名称
  - job_type: 职位类型
  - min_salary: 最低工资
  - max_salary: 最高工资
  - prov: 工作地点省份
  - city: 工作地点城市
  - town: 工作地点区
  - exp: 工作经验
  - work_type: 工作类型
  - job_cmd：岗位要求
  - work_cmd: 任职要求
  
- 返回：
  - 成功：
 ```json 
  {
    "err": "0",
    "msg": "操作成功"
  }
  ```
  - 失败
  ```json
  {
    "err": "err_code",
    "msg": "对应的提示"
  }
  ```
  - err_code: -4/-1/-10
  - msg: 账号错误/请求方法错误/其他错误

  ***

### 获取职位信息
- http://110.64.69.66:8081/team/job_info/
- POST
- 参数：
    - id： 职位的id
- 返回：
    - 成功：
        - JSON:   
        {"err": err,   
         "team_name": team_name,  
         "job_name": job_name,  
         "min_salary": min,  
         "max_salary": max,  
         "prince": prince,  
         "city": city,  
         "town": town,  
         "address": address,  
         "edu_cmd": edu_cmd,  
         "exp_cmd": exp_cmd,  
         "work_type": work_type,  
         "summary": summary,  
         "pub_date": pub_date,  
         "job_cmd": job:cmd,  
         "work_cmd": work_cmd}  
        - err: 0
        - team_name： 公司名称
        - edu_cmd: 学历要求
        - exp_cmd: 经验要求
        - work_type: 工作性质（0表示全职，1表示兼职，2表示实习）
        - summary: 职位突出特点
        - pub_date: 发布日期
        - job_cmd: 岗位要求
        - work_cmd: 任职要求
    - 失败：
        - JSON: {"err": err, "msg": msg}
        - err: -13/-1
        - msg: 职位不存在/请求方法错误
        