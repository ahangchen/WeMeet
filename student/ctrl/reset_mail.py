from student.util.encrypt_decrypt import encrypt


def get_content(reset_key, acnt):
    content = '这是邮件内容'+'http://110.64.69.66:8081/student/fetch?reset_key=%s&mail=%s' % (reset_key, acnt)  # TODO(hjf): 修改内容和URL
    return content


