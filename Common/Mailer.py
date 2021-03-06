import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from datetime import datetime
from jinja2 import Environment, FileSystemLoader


class EmailSender:

    # 发送邮件
    @classmethod
    def send_report(cls, conf, result_file_abs_path):
        result_file_name = result_file_abs_path.split("/")[-1]
        sender = conf.get("sender")
        receivers = conf.get("receivers")
        subject = conf.get("subject")
        mail_server = conf.get("smtp_server")
        username = conf.get("username")
        password = conf.get("password")
        msg_root = MIMEMultipart('related')
        msg_root['Subject'] = subject + str(datetime.now())
        msg_root["From"] = sender
        msg_root["To"] = ", ".join(receivers)

        frameworkDir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        reportPath = os.path.join(frameworkDir, "Report", "Mailer_Report.html")
        with open(result_file_abs_path, "rb") as f:
            content = f.read()

        with open(reportPath, "rb") as f:
            main_content = f.read()

        msg_content_html = MIMEText(main_content, _subtype='html', _charset='utf-8')
        msg_attach = MIMEText(content, 'base64', 'utf-8')
        msg_attach["Content-Type"] = 'application/octet-stream'
        msg_attach["Content-Disposition"] = 'attachment; filename=%s' % result_file_name
        msg_root.attach(msg_content_html)
        msg_root.attach(msg_attach)
        smtp = smtplib.SMTP()
        smtp.connect(mail_server)
        smtp.login(username, password)
        smtp.sendmail(sender, receivers, msg_root.as_string())
        smtp.quit()
