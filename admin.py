from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QLineEdit, QComboBox, QTableWidget, QTableWidgetItem
from database import admin_daily_report, admin_user_report, get_all_usernames

class AdminWindow(QWidget):
    def __init__(self, username):
        super().__init__()
        self.setWindowTitle(f"Admin: {username} Reports")
        v = QVBoxLayout()
        self.date_in = QLineEdit()
        self.date_in.setPlaceholderText("YYYY-MM-DD")
        self.btn_day = QPushButton("Report for Day")
        self.label_day = QLabel()
        self.user_list = QComboBox()
        self.user_list.addItems(get_all_usernames())
        self.btn_user = QPushButton("Report for User")
        self.table_user = QTableWidget()
        v.addWidget(QLabel("Daily Report"))
        v.addWidget(self.date_in)
        v.addWidget(self.btn_day)
        v.addWidget(self.label_day)
        v.addWidget(QLabel("User Report"))
        v.addWidget(self.user_list)
        v.addWidget(self.btn_user)
        v.addWidget(self.table_user)
        self.setLayout(v)

        self.btn_day.clicked.connect(self.report_day)
        self.btn_user.clicked.connect(self.report_user)

    def report_day(self):
        d = self.date_in.text().strip()
        num_users, num_wins = admin_daily_report(d)
        self.label_day.setText(f"Users: {num_users}, Wins: {num_wins}")

    def report_user(self):
        username = self.user_list.currentText()
        rows = admin_user_report(username)
        self.table_user.setRowCount(len(rows))
        self.table_user.setColumnCount(3)
        self.table_user.setHorizontalHeaderLabels(["Date", "#Words Tried", "#Correct Guesses"])
        for i, (dt, num, wins) in enumerate(rows):
            self.table_user.setItem(i, 0, QTableWidgetItem(dt))
            self.table_user.setItem(i, 1, QTableWidgetItem(str(num)))
            self.table_user.setItem(i, 2, QTableWidgetItem(str(wins)))
