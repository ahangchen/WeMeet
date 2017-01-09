import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


def send_163_mail_attach(user, pwd, to_addr, from_addr, subject, attach_path):
    # 创建一个带附件的实例
    msg = MIMEMultipart()

    # 构造附件1
    att1 = MIMEText(open(attach_path, 'rb').read(), 'base64', 'utf-8')
    att1["Content-Type"] = 'application/octet-stream'
    att1["Content-Disposition"] = 'attachment; filename="%s"'% attach_path  # 这里的filename可以任意写，写什么名字，邮件中显示什么名字
    msg.attach(att1)

    # 加邮件头
    msg['to'] = to_addr
    msg['from'] = from_addr
    msg['subject'] = subject
    # 发送邮件
    try:
        server = smtplib.SMTP_SSL('smtp.163.com', 465)
        server.starttls()
        server.set_debuglevel(1)
        server.login(user, pwd)  # XXX为用户名，XXXXX为密码
        server.sendmail(msg['from'], msg['to'], msg.as_string())
        server.quit()
        print('发送成功')
    except smtplib.SMTPConnectError:
        print('SMTPConnectError')


def send_163_mail(user, pwd, from_addr, to_addr, subject, content):
    msg = MIMEText(content)
    # 加邮件头
    msg['to'] = to_addr
    msg['from'] = from_addr
    msg['subject'] = subject
    # 发送邮件
    try:
        server = smtplib.SMTP_SSL('smtp.163.com', 465)
        server.starttls()
        server.set_debuglevel(1)
        server.login(user, pwd)  # XXX为用户名，XXXXX为密码
        server.sendmail(msg['from'], msg['to'], msg.as_string())
        server.quit()
        print('发送成功')
    except smtplib.SMTPConnectError:
        print('SMTPConnectError')
