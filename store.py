import sqlite3

def open():
  con = sqlite3.connect('config.db')
  c = con.cursor()
  return con, c

def scaffold():
  con, c = open()
  c.execute('CREATE TABLE IF NOT EXISTS config(key text unique, value text)')
  con.commit()
  con.close()

def readConfig(key):
  con, c = open()
  c.execute('SELECT value FROM config WHERE key = ?', [key])
  value = c.fetchone()
  if value is None:
    value = ''
  else:
    value = value[0]
  con.close()
  return value

def writeConfig(key, value):
  con, c = open()
  c.execute('INSERT OR REPLACE INTO config (key, value) VALUES (?, ?)', [key, value])
  con.commit()
  con.close()

scaffold()