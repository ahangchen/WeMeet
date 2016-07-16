import smtplib
from email.mime.text import MIMEText

host_163 = 'smtp.163.com'  # 设置发件服务器地址
sender = 'm13660106752@163.com'  # 设置发件邮箱，一定要自己注册的邮箱
pwd = 'xuegongban118'  # 设置发件邮箱的密码，等会登陆会用到


def send_163_mail(receiver, subject, body):
    send_mail(subject, body, sender, receiver, host_163, pwd)


def send_mail(subject, body, sd, receiver, host, pwd):
    msg = MIMEText(body, 'html')  # 设置正文为符合邮件格式的HTML内容
    msg['subject'] = subject  # 设置邮件标题
    msg['from'] = sd  # 设置发送人
    msg['to'] = receiver  # 设置接收人

    s = smtplib.SMTP()  # 注意！如果是使用SSL端口，这里就要改为SMTP_SSL
    s.connect(host)
    s.login(sender, pwd)  # 登陆邮箱
    s.sendmail(sender, receiver, msg.as_string())  # 发送邮件！