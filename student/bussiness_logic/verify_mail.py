from student.utility.encrypt_decrypt import encrypt


def get_content(stu_id):
    content = '这是邮件内容'+'student/verify/'+encrypt(stu_id)  # TODO(hjf): 修改内容和URL
    return content


