
import smtplib
import json
from email.mime.text import MIMEText
## send mail

def send_mail(mail_server,mail_server_port,sender,password_sender,received,body):
    alert = False
    msg = MIMEText(body)
    msg['Subject'] = 'Bao Cao Tai Nguyen Su Dung'
    msg['From'] = sender
    msg['To'] = received
    try:
        s = smtplib.SMTP(mail_server,mail_server_port)
        s.starttls()
        s.login(sender,password_sender)
        s.sendmail(sender,received,msg.as_string())
        alert = True
        s.quit()
        return alert
    except Exception,e:
        return alert
if __name__=='__main__':
    pass