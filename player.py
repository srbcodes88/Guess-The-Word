from PyQt5.QtWidgets import QWidget, QLineEdit, QVBoxLayout, QHBoxLayout, QPushButton, QMessageBox, QLabel
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

class PlayerWindow(QWidget):
    def __init__(self, username):
        super().__init__()
        self.setWindowTitle(f"Player: {username}")
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

        if get_daily_guess_count(username) >= 3:
            QMessageBox.information(self,"Limit reached","Already played 3 games today.")
            self.close()
            return

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
        self.guesses_layout = QVBoxLayout()
        self.game_active = True

    def show_guesses(self):
        while self.guesses_layout.count():
            item = self.guesses_layout.takeAt(0)
            widget = item.widget()
            if widget is not None:
                widget.setParent(None)
            else:
                child_layout = item.layout()
                if child_layout is not None:
                    while child_layout.count():
                        child_item = child_layout.takeAt(0)
                        child_widget = child_item.widget()
                        if child_widget is not None:
                            child_widget.setParent(None)


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
            QMessageBox.information(self, "You Win!", "Congratulations!")
            self.game_active = False
            self.close()
            return
        if self.guess_count == 5:
            QMessageBox.information(self, "Game Over", "Better luck next time!")
            self.game_active = False
            self.close()
