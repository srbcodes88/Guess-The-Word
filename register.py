from PyQt5.QtWidgets import QWidget, QPushButton, QLineEdit, QFormLayout, QMessageBox
from validation import validate_user
from database import register_user


class RegisterWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Register")
        self.layout = QFormLayout()
        self.username = QLineEdit()
        self.password = QLineEdit()
        self.password.setEchoMode(QLineEdit.Password)
        self.btn_register = QPushButton("Register")
        self.layout.addRow("Username:", self.username)
        self.layout.addRow("Password:", self.password)
        self.layout.addRow(self.btn_register)
        self.setLayout(self.layout)
        self.btn_register.clicked.connect(self.try_register)

    def try_register(self):
        uname = self.username.text()
        pwd = self.password.text()
        valid, message = validate_user(uname, pwd)
        if valid:
            if register_user(uname, pwd, "player"):
                QMessageBox.information(self, "Success", "User registered!")
                from login import LoginWindow
                self.close()
                self.login_window = LoginWindow()
                self.login_window.show()
            else:
                QMessageBox.warning(self, "Failed", "Username already taken.")
                self.username.clear()
                self.password.clear()
        else:
            QMessageBox.warning(self, "Failed", message)
            self.password.clear()

