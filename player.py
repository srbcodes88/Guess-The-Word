from PyQt5.QtWidgets import QWidget, QLineEdit, QVBoxLayout, QHBoxLayout, QPushButton, QMessageBox, QLabel, QDialog
from PyQt5.QtCore import Qt
from database import get_daily_guess_count, get_random_word, log_guess
from PyQt5.QtGui import QColor

class GuessLabel(QLabel):
    def __init__(self,text,res):
        super().__init__(text)
        if res == 'g':
            self.setStyleSheet("background-color: #90ee90; font-weight: bold;") # green
        elif res == 'o':
            self.setStyleSheet("background-color: orange; font-weight: bold;") # orange
        else:
            self.setStyleSheet("background-color: #DDDDDD; font-weight: bold;") # grey
        self.setFixedWidth(40)
        self.setAlignment(Qt.AlignCenter)

def result_colors(word, guess):
    result = []
    used = [False]*5
    for i in range(5):
        if guess[i] == word[i]:
            result.append('g')
            used[i] = True
        else:
            result.append('')
    for i in range(5):
        if result[i] != 'g':
            for j in range(5):
                if not used[j] and guess[i] == word[j]:
                    result[i] = 'o'
                    used[j] = True
                    break
            else:
                result[i] = 'x'
    return result

def open_player_window(username):
    # Check daily guess limit before creating window
    if get_daily_guess_count(username) >= 3:
        msg_box = QMessageBox()
        msg_box.setWindowTitle("Limit reached")
        msg_box.setText("Already played 3 games today.")
        exit_button = msg_box.addButton("Exit", QMessageBox.AcceptRole)
        msg_box.setDefaultButton(exit_button)
        msg_box.setEscapeButton(exit_button)
        msg_box.setStandardButtons(QMessageBox.NoButton)
        msg_box.exec_()
        if msg_box.clickedButton() == exit_button:
            from login import LoginWindow
            login_window = LoginWindow()
            login_window.show()
        return None  # Do not create PlayerWindow

    player_window = PlayerWindow(username)
    player_window.show()
    return player_window

class PlayerWindow(QWidget):
    def __init__(self, username):
        super().__init__()
        self.setWindowTitle(f"Player: {username}")
        self.hide()
        self.username = username
        self.layout = QVBoxLayout()
        self.guesses_layout = QVBoxLayout()
        self.input_line = QLineEdit()
        self.input_line.setMaxLength(5)
        self.input_line.setPlaceholderText("Enter 5-letter Word (UPPERCASE)")
        self.btn_submit = QPushButton("Submit Guess")
        self.guess_count = 0
        self.target = None
        self.previous_guesses = []
        self.game_active = False

        '''if get_daily_guess_count(username) >= 3:
            msg_box = QMessageBox(self)
            msg_box.setWindowTitle("Limit reached")
            msg_box.setText("Already played 3 games today.")
            exit_button = msg_box.addButton("Exit", QMessageBox.AcceptRole)
            msg_box.setDefaultButton(exit_button)
            msg_box.setEscapeButton(exit_button)
            msg_box.setStandardButtons(QMessageBox.NoButton)
            msg_box.exec_()
            if msg_box.clickedButton() == exit_button:
                from login import LoginWindow
                self.login_window = LoginWindow()
                self.login_window.show()
            self.close()
            return
        self.show()'''

        self.new_game()

        self.layout.addLayout(self.guesses_layout)
        self.layout.addWidget(self.input_line)
        self.layout.addWidget(self.btn_submit)
        self.setLayout(self.layout)
        self.btn_submit.clicked.connect(self.make_guess)

    def new_game(self):
        self.guess_count = 0
        self.target = get_random_word()
        self.previous_guesses = []
        self.clear_guesses_display()
        self.game_active = True


    def show_guesses(self):
        existing_guess_count = self.guesses_layout.count()
        for guess_index in range(existing_guess_count, len(self.previous_guesses)):
            guess, res = self.previous_guesses[guess_index]
            hbox = QHBoxLayout()
            for i in range(5):
                hbox.addWidget(GuessLabel(guess[i], res[i]))
            self.guesses_layout.addLayout(hbox)

    def show_endgame_dialog(self, title, message):
        dialog = QDialog(self)
        dialog.setWindowTitle(title)
        layout = QVBoxLayout()
        layout.addWidget(QLabel(message))

        buttons = QHBoxLayout()
        btn_new_game = QPushButton("New Game")
        btn_exit = QPushButton("Exit")
        buttons.addWidget(btn_new_game)
        buttons.addWidget(btn_exit)
        layout.addLayout(buttons)
        dialog.setLayout(layout)

        def start_new_game():
            if get_daily_guess_count(self.username) >= 3:
                self.show_limit_popup()
                return
            dialog.accept()
            self.new_game()
            self.clear_guesses_display()
            self.game_active = True

        def exit_game():
            dialog.accept()
            self.close()

        btn_new_game.clicked.connect(start_new_game)
        btn_exit.clicked.connect(exit_game)
        dialog.exec_()



    def make_guess(self):
        if not self.game_active:
            return
        guess = self.input_line.text().strip().upper()
        if len(guess) != 5 or not guess.isalpha():
            QMessageBox.warning(self, "Error", "Enter a 5-letter uppercase word.")
            return
        res = result_colors(self.target, guess)
        win = all(x == 'g' for x in res)
        self.previous_guesses.append((guess, res))
        self.guess_count += 1
        log_guess(self.username, self.target, guess, self.guess_count, win)
        self.show_guesses()
        self.input_line.clear()
        if win:
            self.game_active = False
            self.show_endgame_dialog("You Win!", "Congratulations!")
            return
        if self.guess_count == 5:
            self.game_active = False
            self.show_endgame_dialog("Game Over", f"Better luck next time! The correct word was: {self.target}")
            return

    def clear_guesses_display(self):
        while self.guesses_layout.count():
            child = self.guesses_layout.takeAt(0)
            if child is not None:
                if child.widget():
                    child.widget().deleteLater()
                elif child.layout():
                    self.clear_layout(child.layout())
        self.previous_guesses = []

    @staticmethod
    def clear_layout(layout):
        while layout.count():
            item = layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
            elif item.layout():
                PlayerWindow.clear_layout(item.layout())


