from student.utility.encrypt_decrypt import encrypt


def get_content(account):
    content = '这是邮件内容'+'student/verify/'+encrypt(account)  # TODO(hjf): 修改内容和URL
    return content


