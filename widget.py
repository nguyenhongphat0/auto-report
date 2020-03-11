from PyQt5.QtWidgets import (QWidget, QPushButton, QLineEdit, QInputDialog, QApplication, QLabel, QPlainTextEdit)
import sys
import store
from mail import sendmail
from datetime import datetime

class AutoReport(QWidget):

  def __init__(self):
    super().__init__()
    self.initUI()

  def initUI(self):
    # Make widgets
    _, self.email = self.makeInputCombo('Email', 20, 20, 200, 25, 'email')
    _, self.password = self.makeInputCombo('Password', 240, 20, 200, 25, 'password')
    self.password.setEchoMode(QLineEdit.Password);
    _, self.to = self.makeInputCombo('To', 20, 70, 420, 25, 'to')
    _, self.cc = self.makeInputCombo('CC', 20, 120, 420, 25, 'cc')
    _, self.bcc = self.makeInputCombo('BCC', 20, 170, 420, 25, 'bcc')
    _, self.prefix = self.makeInputCombo('Prefix', 20, 250, 800, 25, 'prefix')
    _, self.postfix = self.makeInputCombo('Postfix', 20, 300, 800, 25, 'postfix')
    self.content = self.makeTextarea('Content', 20, 360, 800, 200, 'content')
    self.sendBtn = self.makeButton('Send', 20, 570, self.send)

    # Window configurations
    self.setGeometry(300, 300, 840, 600)
    self.setWindowTitle('Input dialog')
    self.show()

  def makeLabel(self, title, left, top):
    lbl = QLabel(title, self)
    lbl.move(left, top)
    return lbl

  def makeButton(self, title, left, top, callback):
    btn = QPushButton(title, self)
    btn.move(left, top)
    btn.clicked.connect(callback)
    return btn

  def makeTextarea(self, title, left, top, width, height, model):
    ta = QPlainTextEdit(self)
    ta.move(left, top)
    ta.resize(width, height)
    ta.setPlainText(store.readConfig(model))
    return ta
    
  def makeInput(self, left, top, width, height, callback = lambda _ : _):
    le = QLineEdit(self)
    le.move(left, top)
    le.resize(width, height)
    le.textChanged.connect(callback)
    return le

  def makeInputCombo(self, title, left, top, width, height, model):
    title = self.makeLabel(title, left, top)
    text = self.makeInput(left, top + 20, width, height, lambda text : store.writeConfig(model, text))
    text.setText(store.readConfig(model))
    return title, text

  def generateSubject(self):
    base = '[MDM - Report] Daily Report {0}'
    today = datetime.today().strftime('%d/%m/%Y')
    subject = base.format(today)
    return subject
    
  def send(self):
    subject = self.generateSubject()
    content = self.content.toPlainText()
    store.writeConfig('content', content)
    content = '<p>{}</p><p>{}</p><p>{}</p>'.format(self.prefix.text(), content, self.postfix.text())
    sendmail(
      self.email.text(),
      self.password.text(),
      self.to.text(),
      self.cc.text(),
      self.bcc.text(),
      subject,
      content
    )
