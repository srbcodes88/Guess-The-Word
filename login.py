from PyQt5.QtWidgets import QWidget, QPushButton, QLineEdit, QLabel, QFormLayout, QMessageBox
from PyQt5.QtCore import Qt
from database import login_user
from register import RegisterWindow
from player import PlayerWindow
from admin import AdminWindow

class LoginWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Login")
        self.layout = QFormLayout()
        self.username = QLineEdit()
        self.password = QLineEdit()
        self.password.setEchoMode(QLineEdit.Password)
        self.btn_login = QPushButton("Login")
        self.btn_register = QPushButton("Register")
        self.layout.addRow("Username:", self.username)
        self.layout.addRow("Password:", self.password)
        self.layout.addRow(self.btn_login)
        self.layout.addRow(self.btn_register)
        self.setLayout(self.layout)
        self.btn_login.clicked.connect(self.login)
        self.btn_register.clicked.connect(self.open_register)

    def login(self):
        uname = self.username.text()
        pwd = self.password.text()
        role = login_user(uname, pwd)
        if role:
            self.close()
            if role == "admin":
                AdminWindow(uname).show()
            else:
                PlayerWindow(uname).show()
        else:
            QMessageBox.warning(self, "Login failed", "Wrong username or password.")

    def open_register(self):
        self.reg = RegisterWindow()
        self.reg.show()
