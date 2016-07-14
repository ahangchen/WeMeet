##接口(团队部分)

***
##搜索模块
使用haystack搜索架构，并使用Whoosh搜索引擎，jieba做中文分词
入门教程： http://www.jianshu.com/p/5073e25de698
官方文档： http://django-haystack.readthedocs.io/en/latest/toc.html
***

***
###搜索模块：
* http://127.0.0.1:8000/team/search/
* POST
* 参数：
    * model: job（职位）、team（团队）、项目（product）
    * type：对应每种model的不同type类型
    * keys:
* 返回：
    * 成功:
        * JSON: 符合要求model的列表
        job：
            job_name
            job_type
            min_salary
            max_salary
            job_summary

            team_name
            team_type
            team_about
        team:
            team_name
            team_logo
            team_about
            team_type
        product:
            product_name
            product_content
            product_img_path

            team_name
            type
            team_about
    * 失败：
        * JSON: {"err": err, "msg": msg}
            * err: -1
            * msg: 请求方法错误

***