from PyQt5.QtWidgets import QWidget, QPushButton, QLineEdit, QFormLayout, QMessageBox, QComboBox
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
        self.role = QComboBox()
        self.role.addItems(["player", "admin"])
        self.btn_register = QPushButton("Register")
        self.layout.addRow("Username:", self.username)
        self.layout.addRow("Password:", self.password)
        self.layout.addRow("Role:", self.role)
        self.layout.addRow(self.btn_register)
        self.setLayout(self.layout)
        self.btn_register.clicked.connect(self.try_register)

    def try_register(self):
        uname = self.username.text()
        pwd = self.password.text()
        role = self.role.currentText()
        if validate_user(uname, pwd) and register_user(uname, pwd, role):
            QMessageBox.information(self, "Success", "User registered!")
            self.close()
        else:
            QMessageBox.warning(self, "Failed", "Invalid details or username already taken.")
            self.username.clear()
            self.password.clear()