from PyQt5.QtWidgets import QApplication
import sys
from widget import AutoReport

if __name__ == '__main__':
  app = QApplication(sys.argv)
  ar = AutoReport()
  sys.exit(app.exec_())