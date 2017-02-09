#接口(团队部分)
## 账号逻辑
### 1 团队注册  
* http://wemeet.tech:8081/team/register/
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

### 2 团队登陆：
* http://wemeet.tech:8081/team/login/
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

### 3 请求发送密码重置邮件
* http://wemeet.tech:8081/team/reset/
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

### 4 获取找回密码的凭证（这是一个邮件里的链接，点击进入重置密码页面，这个页面由后端生成）
* http://wemeet.tech:8081/team/fetch?reset_key=xxxxxxx&mail=xxxxx
* POST
* 参数：
    * reset_key： 加密的账号（由后端加密，只能通过邮件链接传递给前端）
    * mail：账号邮箱
* 返回：
    * 重置密码页面 

***

### 5 修改密码
* http://wemeet.tech:8081/team/update_pwd/
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

## 统计业务
***
### 搜索模块
使用haystack搜索架构，并使用Whoosh搜索引擎，jieba做中文分词
入门教程： http://www.jianshu.com/p/5073e25de698
官方文档： http://django-haystack.readthedocs.io/en/latest/toc.html
***

***
### 6 搜索模块：
* http://wemeet.tech:8081/team/search/
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
### 7 热门团队模块：
* http://wemeet.tech:8081/team/hot_team/
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
### 8 热门项目模块：
* http://wemeet.tech:8081/team/hot_product/
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

##  职位
### 9 职位搜索
- http://wemeet.tech:8081/team/search_job/
- post
- 参数：
    jobTags: 职位标签
    team_id: 团队ID
- 返回：
    - 成功：
        - JSON:
        {"err": 0,
         "message":[{
             ob_id:职位id
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
                - job_state:职位发布状态
         },...]
        }
    - 失败：
        - JSON: {"err": err, "message": message}
        - err: -21/-1
        - message: 职位类型错误/请求方法错误

### 10 添加职位
- http://wemeet.tech:8081/team/add_job/
- post
- 参数：
  - name：职位名称
  - j_type: 职位类型
  - min_salary: 最低工资
  - max_salary: 最高工资
  - prince: 工作地点省份
  - city: 工作地点城市
  - town: 工作地点区
  - address: 详细地址
  - exp_cmd: 工作经验
  - w_type: 工作类型
  - job_cmd：岗位要求
  - work_cmd: 任职要求
  - pub_state: 职位发布状态
  - team_id: 团队ID
- 返回：
    - 成功：
        - JSON:
        {"err": 0,
         "message": "请求成功",
         "msg": 职位id
        }
    - 失败：
        - JSON: {"err": err, "message": message}
        - err: -22/-1
        - message: 参数错误信息列表/请求方法错误
        - 参数错误信息列表:{
            参数名：相应的错误信息
            "name":相应的错误信息
            ...
        }
- 说明：可以使用Json或form-data格式传输数据，但注意在是使用Json时，POST请求中CONTENT-TYPE要使用“application/json”

### 11 修改职位
- http://wemeet.tech:8081/team/update_job/
- post
- 参数：
  - id: 职位ID
  - name：职位名称
  - j_type: 职位类型
  - min_salary: 最低工资
  - max_salary: 最高工资
  - prince: 工作地点省份
  - city: 工作地点城市
  - town: 工作地点区
  - exp_cmd: 工作经验
  - w_type: 工作类型
  - job_cmd：岗位要求
  - work_cmd: 任职要求
  - pub_state: 职位发布状态
  - team_id: 团队ID
- 返回：
    - 成功：
        - JSON:
        {"err": 0,
         "message": "请求成功"
        }
    - 失败：
        - JSON: {"err": err, "message": message}
        - err: -23/-22/-1
        - message: 职位不存在/参数错误信息列表/请求方法错误
        - 参数错误信息列表:{
            参数名：相应的错误信息
            "name":相应的错误信息
            ...
        }
- 说明：可以使用Json或form-data格式传输数据，但注意在是使用Json时，POST请求中CONTENT-TYPE要使用“application/json”

### 11.1 删除职位
* http://wemeet.tech:8081/team/delete_job/
* POST
* 参数：
    * jobId: 职位id
* 返回：
    * 成功：* JSON: {'err': err, 'msg': msg}
        err: 0
        msg: 操作成功
    * 失败
        * JSON: {'err': err, 'msg': msg}
            * err: -122/-1/-101
            * msg: 职位不存在/请求方法错误/操作失败
***

### 11.2 查找职位类型
* http://wemeet.tech:8081/team/job_type/
* POST
* 返回：
    * 成功：* JSON: {'err': err, 'msg': msg}
        err: 0
        msg:[{
                id: 职位类型ID,
                name: 职位类型name,
            },
            ...
        ]
***


### 12 职位编辑
- http://wemeet.tech:8081/team/job_update/
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

### 13 获取职位信息
- http://wemeet.tech:8081/team/job_info/
- POST
- 参数：
    - id： 职位的id
- 返回：
    - 成功：
        - JSON:   
        {"err": err,   
         "team_id": team_id,  
         "job_name": job_name,  
         "min_salary": min,  
         "max_salary": max,  
         "prince": prince,  
         "city": city,  
         "town": town,  
         "address": address,  
         "edu_cmd": edu_cmd,  
         "exp_cmd": exp_cmd,  
         "job_type": job_type,   
         "work_type": work_type,  
         "summary": summary,  
         "pub_date": pub_date,  
         "pub_state": pub_state,    
         "job_cmd": job_cmd,  
         "work_cmd": work_cmd}  
        - err: 0
        - team_id： 所属团队id
        - edu_cmd: 学历要求
        - exp_cmd: 经验要求
        - job_type: 职位类型：（产品，开发，设计。。。
        - work_type: 工作性质（0表示全职，1表示兼职，2表示实习）
        - summary: 职位突出特点
        - pub_date: 发布日期
        - pub_state: 发布状态（0表示待发布，1表示已发布，2表示已下架）
        - job_cmd: 岗位要求
        - work_cmd: 任职要求
    - 失败：
        - JSON: {"err": err, "msg": msg}
        - err: -13/-1
        - msg: 职位不存在/请求方法错误

##  项目
### 14 项目查找
- http://wemeet.tech:8081/team/product/info/
- post
- 参数：
    productId: 项目ID
- 返回：
    - 成功：
        - JSON:
        {"err": 0,
         "msg":{
                - name: 项目名称
                - img_path: 照片路径
                - content: 团队简介
                - reward: 获奖情况
                - team_id: 团队ID
                - last_visit_cnt： 上周访问量
                - week_visit_cnt: 每周访问量
        }
    - 失败：
        - JSON: {"err": err, "msg": msg}
        - err: -102/-1/-101
        - msg: 项目不存在/请求方法错误/操作失败

### 15 添加项目
- http://wemeet.tech:8081/product/insert/
- post
- 参数：
    - name: 项目名称
    - img_path: 照片路径(file)
    - content: 团队简介
    - reward: 综合字段，内容格式为json形式，包含标签，slogan，url，例如：

```
{'slogan': '为人民服务', url: 'www.baidu.com', 'tag':['萌', '炫', '酷']}
```

    - team_id: 团队ID
- 返回：
    - 成功：
        - JSON:
        {"err": 0,"msg": 项目id}
    - 失败：
        - JSON: {"err": err, "msg": msg}
        - err: -104/-103/-102/-101/-22/-1
        - message: 项目照片格式错误/项目照片保存失败/项目不存在/操作失败/参数错误信息列表/请求方法错误
        - 参数错误信息列表:{
            参数名：相应的错误信息
            "name":相应的错误信息
            ...
        }
- 说明：可以使用Json或form-data格式传输数据，但注意在是使用Json时，POST请求中CONTENT-TYPE要使用“application/json”

### 16 修改项目
- http://wemeet.tech:8081/team/product/update/
- post
- 参数：
    - id: 项目ID
    - name: 项目名称
    - img_path: 照片路径(file)
    - content: 团队简介
    - reward: 综合字段，内容格式为json形式，包含标签，slogan，url，例如：

```
{'slogan': '为人民服务', url: 'www.baidu.com', 'tag':['萌', '炫', '酷']}
```

    - team_id: 团队ID
- 返回：
    - 成功：
        - JSON:
        {"err": 0,
         "msg": "请求成功"
        }
    - 失败：
        - JSON: {"err": err, "msg": msg}
        - err: -104/-103/-102/-101/-22/-1
        - message: 项目照片格式错误/项目照片保存失败/项目不存在/操作失败/参数错误信息列表/请求方法错误
        - 参数错误信息列表:{
            参数名：相应的错误信息
            "name":相应的错误信息
            ...
        }
- 说明：可以使用Json或form-data格式传输数据，但注意在是使用Json时，POST请求中CONTENT-TYPE要使用“application/json”

### 17 删除项目
- http://wemeet.tech:8081/team/product/delete/
- post
- 参数：
    productId: 项目ID
- 返回：
    - 成功：
        - JSON:
        {"err": 0,
         "msg": 操作成功
        }
    - 失败：
        - JSON: {"err": err, "msg": msg}
        - err: -102/-1/-101
        - msg: 项目不存在/请求方法错误/操作失败

### 18 上传项目照片
* http://wemeet.tech:8081/team/product/save_img/
* POST
* 参数：
    * id: 项目id
    * prod_img： 项目照片
* 返回：
    * 成功：
        * JSON: {'err': err, 'msg': msg}
            * err: 0
            * msg: 项目照片路径
    * 失败
        * JSON: {'err': err, 'msg': msg}
            * err: -104/-103/-102/-1/-101
            * msg: 项目照片格式错误/项目照片保存失败/项目不存在/请求方法错误/操作失败

***

### 19 项目搜索
- http://wemeet.tech:8081/team/product/search/
- post
- 参数：
    teamId: 团队ID
- 返回：
    - 成功：
        - JSON:
        {"err": 0,
         "msg":[{
                - name: 项目名称
                - img_path: 照片路径
                - content: 团队简介
                - reward: 获奖情况
                - id: 项目ID
                - last_visit_cnt： 上周访问量
                - week_visit_cnt: 每周访问量
                },
             ...
            ]
        }
    - 失败：
        - JSON: {"err": err, "msg": message}
        - err: -1
        - message: 请求方法错误



## 团队

### 21 团队邀请
- http://wemeet.tech:8081/team/invite/
- POST
- 参数
  - mail
  - leader
  - tel
  - name:团队名称
- 返回：
  - 成功：
``` json 
    {
    "err": "0",
    "msg":"tid"
    }
  ``` 
   - 失败
 ```json 
   {
   "err": "-10",
   "msg": "已存在"
   }
 ``` 
   
### 22 团队信息
- http://wemeet.tech:8081/team/info?tid=xxxx
- 参数：
  - tid: 团队id
- 返回：
  - 查询成功
  - stus, imgs, label的值可能是\[\]的空串 
  
```json
{
	"res": {
		"man_cnt": 0,
		"slogan": "",
                "name": "wemeet",
		"about": "",
		"mail": "1418659400@qq.com",
		"tid": 1,
		"tel": "666752",
		"b_type": 0,
		"stus": [
			{
				"school": null,
				"id": 1,
				"name": "cwh",
				"logo_path": null
			},
			{
				"school": null,
				"id": 2,
				"name": "mlh",
				"logo_path": null
			}
		],
		"imgs": [
            {
                id: 3,
                path: "media/team/info/10"
            },
            {
                id: 4,
                path: "media/team/info/10"
            }     
		],
		"label": [
			"school",
			"web"
		],
		"history": "",
		"logo_path": ""
	},
	"err": 0
}
```
- 查询失败
 ```json
   {
   "err": "-4",
   "msg": "账号不存在"
   }
 ``` 
### 23 更新团队信息
- url
  -  http://wemeet.tech:8081/team/update_team_info/
  - post
- 参数
  - tid: 团队id
  - name: 团队名
  - logo_path：logo路径
  - slogan：口号
  - about：团队介绍
  - history：发展历程
  - b_type：行业类型：只有有限个可选，查询行业类型接口可以得到对应的名字
 
- 返回
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

### 24 增加团队标签
- url
  -  http://wemeet.tech:8081/team/add_team_label/
  - post
- 参数
  - tid: 团队id
  - name: 标签名
  
- 返回
   - 成功：
   
```json 
  {
    "err": "0",
    "msg": "label_id"
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

### 25 删除团队标签
- url
  -  http://wemeet.tech:8081/team/rm_team_label/
  - post
- 参数
  - tid: 团队id
  - name: 标签名
  
- 返回
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
  
  - err_code: -31/-4/-1/-10
  - msg: 标签不存在/账号错误/请求方法错误/其他错误

### 26 获取行业类型
* http://wemeet.tech:8081/team/business/
* POST
* 参数：
    - 无
* 返回：
    * 成功:
        * JSON: {"err": err, "msg": "操作成功"} 
            * err: 0  
            * msg：操作成功提示
    * 失败：
        * JSON: {"err": err, "msg": msg}
            * err: -10
            * msg: 未知错误

***

### 27 新增团队学生
- url
  -  http://wemeet.tech:8081/team/add_team_stu/
  - post
- 参数
  - tid: 团队id
  - sid: 学生id
  
- 返回
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
  
  - err_code: -32/-4/-1/-10
  - msg: 要添加的学生不存在/账号错误/请求方法错误/其他错误
  
### 28 删除团队学生
- url
  -  http://wemeet.tech:8081/team/rm_team_stu/
  - post
- 参数
  - tid: 团队id
  - sid: 标签id
  
- 返回
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
  
  - err_code: -32/-4/-1/-10
  - msg: 要删除的学生不存在/账号错误/请求方法错误/其他错误
  

### 29 查询学生邮箱

- url
  -  http://wemeet.tech:8081/team/name2mail?name=cwh
  - get
- 参数
  - name: 学生名字
  
- 返回
   - 成功：
   
```json 
  {
    "err": "0",
    "res": [
        {
        "sid": "1",
        "mail": "1418659400@qq.com"
        },
        {
        "sid": "2",
        "mail": "cweihang@foxmail.com"
        }
        ]
  }
``` 
  
  res里是名字对应的学生邮箱列表
  
  - 失败
  
```json 
  {
    "err": "err_code",
    "msg": "对应的提示"
  }
``` 
  - err_code: -4/-10
  - msg: 找不到对应的学生邮箱/其他错误
  
### 30 邀请团队成员注册

- url
  -  http://wemeet.tech:8081/team/invite_stu/
  - post
- 参数
  - tid: 团队id 
  - mail: 学生邮箱
  
- 返回
  - 成功：
  
``` json 
    {
    "err": "0",
    "msg":"操作成功"
    }
  ``` 
   - 失败
   
 ```json 
   {
   "err": "-3",
   "msg": "已存在"
   }
 ``` 


### 31 新增团队照片
- url
  -  http://wemeet.tech:8081/team/add_team_photo/
  - post
- 参数
  - tid: 团队id
- FILES['photo']：img: 图片

- 返回
   - 成功：
   
```json 
  {
    "err": "0",
    "msg": {'img_id': ret, 'path': path}
  }
``` 
  - 会返回团队图片id
  
  - 失败
  
```json 
  {
    "err": "err_code",
    "msg": "对应的提示"
  }
``` 
  
  - err_code: -6/-4/-1/-10
  - msg: 参数错误/请求方法错误/其他错误



### 32 删除团队照片
- url
  -  http://wemeet.tech:8081/team/rm_team_photo/
  - post
- 参数
  - tid: 团队id
  - img_id: 照片路径

- 返回
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
  
  - err_code: -6/-4/-1/-10
  - msg: 参数错误/请求方法错误/其他错误

### 33 更新团队联系方式
- url
  -  http://wemeet.tech:8081/team/update_team_contact/
  - post
- 参数
  - tid: 团队id
  - tel: 联系电话
  - mail：联系邮箱
  
- 返回
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
  
### 34 上传团队logo
- url
  -  http://wemeet.tech:8081/team/upload_logo/
  - post
- 参数
  - name: 本地图片名字
- FILES['photo']：img: 图片

- 返回
   - 成功：
   
```json 
  {
    "err": "0",
    "msg": "logo_path"
  }
``` 
  - 会返回团队logo路径
  
  - 失败
  
```json 
  {
    "err": "err_code",
    "msg": "对应的提示"
  }
``` 
  
  - err_code: -6/-4/-1/-10
  - msg: 参数错误/请求方法错误/其他错误


### 35 团队最新动态

- url: http://wemeet.tech:8081/team/all/newest/
- 响应：

```json

{"res": [
    {
        "team": [
          {
              "logo_path": "team/info/14708380004627852016-08-10 13:55:47屏幕截图.png", 
              "tid": 1, 
              "name": "wemeet"
          }
        ]
    }, 
    {
        "products": [
           {
              "p_name": "first_prj", 
              "tid": 1, 
              "t_name": "wemeet", 
              "pid": 1, 
              "p_img": "team/info/14708380004627852016-08-10 13:55:47屏幕截图.png"
           }
          ]
    }, 
    {
        "jobs": [
            {
                "team_logo": "team/info/14708380004627852016-08-10 13:55:47屏幕截图.png", 
                "tid": 1, 
                "t_name": "wemeet", 
                "jid": 7, 
                "j_name": "sfa"
            }, 
            {
                "team_logo": "team/info/14708380004627852016-08-10 13:55:47屏幕截图.png", 
                "tid": 1, 
                "t_name": "wemeet", 
                "jid": 6, 
                "j_name": "sdaf"
            }, 
            {
                "team_logo": "team/info/14708380004627852016-08-10 13:55:47屏幕截图.png", 
                "tid": 1, 
                "t_name": "wemeet", 
                "jid": 5, 
                "j_name": "测试啊"
            }
          ]
    }
  ], 
  "err": "0"
  }
```

### 36 最新团队

- url: http://wemeet.tech:8081/team/team/newest/
- 响应：

```json
{"res": {
        "team": [
          {
              "logo_path": "team/info/14708380004627852016-08-10 13:55:47屏幕截图.png", 
              "tid": 1, 
              "name": "wemeet"
          }
        ]
  },
  "err": "0"
}
```

## 互动社区

### 37 话题查找
- http://wemeet.tech:8081/team/topic/info/
- post
- 参数：
    topic: 话题ID
- 返回：
    - 成功：
        - JSON:
        {"err": 0,
         "msg":{
                - id: 话题id
                - title: 标题
                - content: 内容
        }
    - 失败：
        - JSON: {"err": err, "msg": msg}
        - err: -102/-1/-101
        - msg: 不存在/请求方法错误/操作失败

### 38 添加话题
- http://wemeet.tech:8081/team/topic/new/
- post
- 参数：
    - tid: 团队id
    - title: 标题
    - content: 内容

- 返回：
    - 成功：
        - JSON:
        {"err": 0,"msg": 话题id}
    - 失败：
        - JSON: {"err": err, "msg": msg}
        - err: -1
        - message: 操作失败/参数错误信息列表/请求方法错误

### 39 修改话题
- http://wemeet.tech:8081/team/topic/update/
- post
- 参数：
    - topic: 话题ID
    - title: 标题
    - content: 内容 


- 返回：
    - 成功：
        - JSON:
        {"err": 0,
         "msg": "请求成功"
        }
    - 失败：
        - JSON: {"err": err, "msg": msg}
        - err: -22/-1
        - message: 话题不存在/操作失败/参数错误信息列表/请求方法错误

### 40 删除话题 
- http://wemeet.tech:8081/team/topic/remove/
- post
- 参数：
    - topic: 话题ID

- 返回：
    - 成功：
        - JSON:
        {"err": 0,
         "msg": "请求成功"
        }
    - 失败：
        - JSON: {"err": err, "msg": msg}
        - err: -22/-1
        - message: 话题不存在/操作失败/参数错误信息列表/请求方法错误
