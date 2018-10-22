from email.header import Header
from email.mime.text import MIMEText
from email.utils import parseaddr, formataddr
import smtplib

def _format_addr(s):
    name, addr = parseaddr(s)
    return formataddr((Header(name, 'utf-8').encode(), addr))


def send_email(msg, to_addr=None):
    if to_addr is None:
        to_addr = ['zhagnlinw0822@163.com']
    from_addr = 'zlw0822@163.com'
    password = 'wei860822'
    smtp_server = 'smtp.163.com'
    msg = MIMEText(msg, 'plain', 'utf-8')
    msg['From'] = _format_addr('下单服务 <%s>' % from_addr)
    msg['Subject'] = Header('服务异常', 'utf-8').encode()
    server = smtplib.SMTP(smtp_server, 25)
    server.set_debuglevel(1)
    server.login(from_addr, password)
    server.sendmail(from_addr, to_addr, msg.as_string())
    server.quit()

if __name__ == '__main__':
    to_addr = ['zhanglinw0822@163.com']
    send_email('服务异常！',to_addr)