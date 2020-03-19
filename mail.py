import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from PyQt5.QtWidgets import QMessageBox

mailserver = 'smtp.office365.com:587'

def sendmail(email, password, to, cc, bcc, subject, content):
  try:
    server = smtplib.SMTP(mailserver)
    server.ehlo()
    server.starttls()
    server.ehlo()
    server.login(email, password)

    msg = MIMEMultipart('alternative')
    msg['Subject'] = subject
    msg['From'] = email
    msg['To'] = to
    msg['Cc'] = cc
    msg['Bcc'] = bcc
    message = MIMEText(content, 'html')
    msg.attach(message)

    server.sendmail(email, '{},{},{}'.format(to, cc, bcc).split(','), msg.as_string())
    alert(QMessageBox.Information, 'Mail sent successfully!', '{} was sent successfully to {}'.format(subject, to))
  except Exception as e:
    alert(QMessageBox.Warning, 'Error sending email', str(e))
  finally:
    server.quit()

def alert(icon, title, text):
  global box
  box = QMessageBox()
  box.setIcon(icon)
  box.setWindowTitle(title)
  box.setText(text)
  box.show()