import sys
from PyQt5.QtWidgets import QApplication
from database import init_db
from gui_login import LoginWindow

if __name__ == '__main__':
    init_db()
    app = QApplication(sys.argv)
    win = LoginWindow()
    win.show()
    sys.exit(app.exec_())
