from PyQt5.QtWidgets import (QWidget, QPushButton, QLineEdit, QInputDialog, QApplication, QLabel, QPlainTextEdit, QBoxLayout)
from PyQt5.QtCore import (QUrl, Qt)
from PyQt5.QtWebEngineWidgets import (QWebEngineView)
import sys
import os
import store
from mail import sendmail
from datetime import datetime
from threading import Timer

class AutoReport(QWidget):

  def __init__(self):
    super().__init__()
    self.initUI()

  def initUI(self):
    # Report sender
    _, self.email = self.makeInputCombo('Email', 20, 20, 200, 25, 'email')
    _, self.password = self.makeInputCombo('Password', 240, 20, 200, 25, 'password')
    self.password.setEchoMode(QLineEdit.Password);
    _, self.to = self.makeInputCombo('To', 20, 70, 420, 25, 'to')
    _, self.cc = self.makeInputCombo('CC', 20, 120, 420, 25, 'cc')
    _, self.bcc = self.makeInputCombo('BCC', 20, 170, 420, 25, 'bcc')
    _, self.subject = self.makeInputCombo('Subject template', 20, 220, 200, 25, 'subject')
    _, self.dateformat = self.makeInputCombo('Date format', 240, 220, 200, 25, 'dateformat')
    self.prefix = self.makeTextarea('Prefix', 20, 270, 420, 70, 'prefix')
    self.content = self.makeTextarea('Content', 20, 350, 420, 200, 'content')
    self.postfix = self.makeTextarea('Postfix', 20, 560, 420, 70, 'postfix')
    self.sendBtn = self.makeButton('Send', 20, 640, self.send)
    self.makeSubjectView()
    self.makeWebView()

    # Report picker
    self.loadReports()

    # Window configurations
    self.setWindowTitle('Auto Report')
    self.setFixedSize(1080, 680)
    self.setWindowFlags(Qt.WindowCloseButtonHint | Qt.WindowMinimizeButtonHint)
    self.setBackground()
    self.show()

  def loadReports(self):
    self.reports = []
    _ = self.makeLabel('Choose another report', 480, 20)
    self.createButton = self.makeButton('New report', 990, 20, self.createReport)
    self.reportTop = 20
    for r, d, f in os.walk('sqlite'):
      for file in f:
        if '.db' in file:
          self.appendReport(file)

  def appendReport(self, file):
    self.reportTop += 30
    name = file[0:-3]
    btn = self.makeButton(name, 480, self.reportTop, lambda _, file=file : self.loadConfig(file))
    self.reports.append(btn)

  def setBackground(self):
    palette = self.palette()
    palette.setColor(self.backgroundRole(), Qt.white)
    self.setPalette(palette)

  def loadConfig(self, file):
    store.use(file)
    self.email.setText(store.readConfig('email'))
    self.password.setText(store.readConfig('password'))
    self.to.setText(store.readConfig('to'))
    self.cc.setText(store.readConfig('cc'))
    self.bcc.setText(store.readConfig('bcc'))
    self.dateformat.setText(store.readConfig('dateformat'))
    self.subject.setText(store.readConfig('subject'))
    self.prefix.setPlainText(store.readConfig('prefix'))
    self.postfix.setPlainText(store.readConfig('postfix'))
    self.content.setPlainText(store.readConfig('content'))

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
    ta.textChanged.connect(lambda : store.writeConfig(model, ta.toPlainText()))
    return ta
    
  def makeInput(self, left, top, width, height, callback = lambda _ : _):
    le = QLineEdit(self)
    le.move(left, top)
    le.resize(width, height)
    le.textChanged.connect(callback)
    return le

  def makeInputCombo(self, title, left, top, width, height, model):
    title = self.makeLabel(title, left, top)
    text = self.makeInput(left, top + 15, width, height, lambda text : store.writeConfig(model, text))
    return title, text

  def makeSubjectView(self):
    self.subjectLabel = self.makeLabel('Subject Preview', 450, 238)
    self.subjectLabel.resize(440, 20)
    self.subject.textChanged.connect(lambda text : self.subjectLabel.setText(self.getSubject()))

  def makeWebView(self):
    self.web = QWebEngineView(self)
    self.web.move(450, 270)
    self.web.resize(620, 390)
    self.content.textChanged.connect(lambda : self.web.setHtml(self.getBody()))

  def createReport(self):
    os.makedirs('sqlite', exist_ok=True)
    name, ok = QInputDialog.getText(self, 'Input dialog', 'Name of the new report:', QLineEdit.Normal)
    if ok and name:
      file = name + '.db'
      store.use(file)
      self.appendReport(file)
      self.update()

  def getSubject(self):
    today = datetime.today().strftime(self.dateformat.text())
    subject = self.subject.text().format(today)
    return subject

  def getBody(self):
    prefix = self.prefix.toPlainText()
    content = self.content.toPlainText()
    postfix = self.postfix.toPlainText()
    return '<div style="font-family: Arial,Helvetica,sans-serif;"><p>{}</p><p>{}</p><p>{}</p></div>'.format(prefix, content, postfix)
    
  def send(self):
    subject = self.getSubject()
    body = self.getBody()
    sendmail(
      self.email.text(),
      self.password.text(),
      self.to.text(),
      self.cc.text(),
      self.bcc.text(),
      subject,
      body
    )
