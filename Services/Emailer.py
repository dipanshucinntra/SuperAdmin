from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from posixpath import basename
import smtplib
import os
import ssl


def sendMail(toEmail, subject, message, attachments):
    try:        
        ServerHost = "smtp.gmail.com"
        ServerPort = 587  # For starttls
        Sender = "vishal.dubey@cinntra.com"
        Password = "Vishal123!@#"
        # Create message
        # msg = MIMEText(message, "HTML")
        msg = MIMEMultipart()
        msg['Subject'] = subject
        msg['From'] = Sender
        msg['To'] = toEmail
        msg.attach(MIMEText(message, "HTML"))    
        if attachments != "":
            filename = os.path.basename(attachments)
            attachUrl = '/home/www/b2b/wae_pre1/bridge/bridge'+attachments
            with open(attachUrl, "rb") as fil:
                part = MIMEApplication(
                        fil.read(),
                        Name=basename(attachUrl)
                )
            # After the file is closed
            part['Content-Disposition'] = 'attachment; filename="%s"' % filename
            msg.attach(part)
        context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
        context.options |= ssl.OP_NO_TLSv1 | ssl.OP_NO_TLSv1_1
        server = smtplib.SMTP(ServerHost, ServerPort)
        server.starttls(context=context)
        # Perform operations via server
        server.login(Sender, Password)
        server.sendmail(Sender, [toEmail], msg.as_string())
        server.quit()
        return 'Sent'
    except Exception as e:
        return str(e)