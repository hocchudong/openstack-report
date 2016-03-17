import smtplib
from email.mime.text import MIMEText
from datetime import datetime


## send mail

def send_mail(mail_server, mail_server_port, sender, password_sender, received, body):
    alert = False
    msg = MIMEText(body)
    msg['Subject'] = 'Bao Cao Tai Nguyen Su Dung'
    msg['From'] = sender
    msg['To'] = received
    try:
        s = smtplib.SMTP(mail_server, mail_server_port)
        s.starttls()
        s.login(sender, password_sender)
        s.sendmail(sender, received, msg.as_string())
        alert = True
        s.quit()
        return alert
    except Exception, e:
        return alert


## Report resource to mail. using email in config file


def reports(node,cpu_used,cpu_total,ram_total,ram_used,hdd_total,hdd_free,
            instances,volumes,received,mail_server,mail_server_port,sender,password_sender):   
    alert = None
    now = datetime.now()
    body = """
    Report at %s  
    Node: %s     
    CPU cores used: %d cores
    CPU cores Total: %d cores
    RAM Free: %d MB
    RAM Used: %d MB
    RAM Total: %d MB
    Disk Used: %d GB
    Disk Free: %d GB
    Disk Total: %d GB
    Instances: %d
    Volumes: %d
    """ % (
        now, node,cpu_used, cpu_total, ram_total - ram_used, ram_used, ram_total, hdd_total - hdd_free, hdd_free,
        hdd_total,instances,volumes)
    
    if send_mail(mail_server,   mail_server_port, sender, password_sender, received, body):
        alert = 'Sent mail successful'
        return alert
    else:
        alert ='Send mail failed'
        return alert
if __name__ == '__main__':
    pass
