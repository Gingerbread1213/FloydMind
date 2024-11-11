import random
from PyQt5.QtWidgets import (
    QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QLineEdit, QMessageBox
)
from PyQt5.QtCore import Qt
from PyQt5 import QtWidgets
from games.game import GameWindow

class HangmanWindow(GameWindow):
    def __init__(self, media_player):
        super().__init__(media_player)
        self.is_paused = False
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Hangman')
        self.resize(1000, 800)
        self.center()
        self.setStyleSheet("background-color: #E3F2FD;")

        # Main layout
        self.main_layout = QVBoxLayout()

        # Header with Go Back and Pause buttons
        header_layout = QVBoxLayout()
        self.back_button = QPushButton("Back")
        self.back_button.setStyleSheet("""
            background-color: #00897B;
            border-radius: 5px;
            color: white;
            padding: 8px;
            font-weight: bold;
            font-size: 17px;
        """)
        self.back_button.clicked.connect(self.go_back)
        header_layout.addWidget(self.back_button, alignment=Qt.AlignTop)

        self.pause_button = QPushButton("Pause")
        self.pause_button.setStyleSheet("""
            background-color: #00897B;
            border-radius: 5px;
            color: white;
            padding: 8px;
            font-weight: bold;
            font-size: 17px;
        """)
        self.pause_button.setCheckable(True)
        self.pause_button.clicked.connect(self.pause_game)
        header_layout.addWidget(self.pause_button, alignment=Qt.AlignTop)

        header_label = QLabel("Hangman")
        header_label.setAlignment(Qt.AlignCenter)
        header_label.setStyleSheet(
            "font-size: 27px; font-weight: bold; color: #004D40; padding: 12px;"
        )
        header_layout.addWidget(header_label, alignment=Qt.AlignCenter)
        self.main_layout.addLayout(header_layout)

        # Word display
        self.word_label = QLabel("")
        self.word_label.setAlignment(Qt.AlignCenter)
        self.word_label.setStyleSheet(
            "font-size: 35px; font-weight: bold; color: #004D40; padding: 20px;"
        )
        self.main_layout.addWidget(self.word_label)

        # Input field
        self.input_layout = QHBoxLayout()
        self.letter_input = QLineEdit()
        self.letter_input.setMaxLength(1)
        self.letter_input.setStyleSheet("""
            background-color: #ffffff;
            border: 1px solid #80CBC4;
            border-radius: 5px;
            padding: 10px;
            color: #004D40;
            font-size: 27px;
        """)
        self.input_layout.addWidget(self.letter_input)

        self.guess_button = QPushButton("Guess")
        self.guess_button.setStyleSheet("""
            background-color: #4DB6AC;
            border-radius: 5px;
            color: white;
            padding: 10px;
            font-weight: bold;
            font-size: 21px;
        """)
        self.guess_button.clicked.connect(self.guess_letter)
        self.input_layout.addWidget(self.guess_button)

        self.main_layout.addLayout(self.input_layout)

        # Hint button
        self.hint_button = QPushButton("Hint")
        self.hint_button.setStyleSheet("""
            background-color: #4DB6AC;
            border-radius: 5px;
            color: white;
            padding: 10px;
            font-weight: bold;
            font-size: 21px;
        """)
        self.hint_button.clicked.connect(self.give_hint)
        self.main_layout.addWidget(self.hint_button)

        # Hangman status
        self.status_label = QLabel("")
        self.status_label.setAlignment(Qt.AlignCenter)
        self.status_label.setStyleSheet(
            "font-size: 21px; color: #004D40; padding: 10px;"
        )
        self.main_layout.addWidget(self.status_label)

        self.setLayout(self.main_layout)

        self.reset_game()

    def reset_game(self):
        self.words = [
            'python', 'hangman', 'programming', 'pyqt', 'openai', 'algorithm',
            'function', 'variable', 'inheritance', 'polymorphism',
            'encapsulation', 'abstraction', 'debugging', 'interface',
            'database', 'network', 'encryption', 'compression', 'asynchronous',
            'synchronous', 'multithreading', 'exception', 'decorator',
            'generator', 'iterator', 'recursion', 'lambda', 'module', 'package',
            'syntax', 'semantics'
        ]
        self.word_to_guess = random.choice(self.words)
        self.display_word = ['_' for _ in self.word_to_guess]
        self.attempts_left = 6
        self.guessed_letters = []
        self.is_paused = False
        self.update_display()

    def update_display(self):
        self.word_label.setText(' '.join(self.display_word))
        self.status_label.setText(
            f"Attempts left: {self.attempts_left}\nGuessed letters: "
            f"{', '.join(self.guessed_letters)}"
        )
        self.letter_input.clear()

    def guess_letter(self):
        if self.is_paused:
            return
        letter = self.letter_input.text().lower()
        if not letter.isalpha() or letter in self.guessed_letters:
            return
        self.guessed_letters.append(letter)
        if letter in self.word_to_guess:
            for idx, char in enumerate(self.word_to_guess):
                if char == letter:
                    self.display_word[idx] = letter
            if '_' not in self.display_word:
                QMessageBox.information(self, "Hangman",
                                        "Congratulations! You've guessed the word!")
                self.reset_game()
        else:
            self.attempts_left -= 1
            if self.attempts_left == 0:
                QMessageBox.information(self, "Hangman",
                                        f"Game Over! The word was '{self.word_to_guess}'.")
                self.reset_game()
        self.update_display()

    def give_hint(self):
        if self.is_paused:
            return
        remaining_letters = [
            c for c, d in zip(self.word_to_guess, self.display_word) if d == '_'
        ]
        if remaining_letters:
            hint_letter = random.choice(remaining_letters)
            self.guessed_letters.append(hint_letter)
            for idx, char in enumerate(self.word_to_guess):
                if char == hint_letter:
                    self.display_word[idx] = hint_letter
            self.update_display()
            if '_' not in self.display_word:
                QMessageBox.information(self, "Hangman",
                                        "Congratulations! You've guessed the word!")
                self.reset_game()

    def pause_game(self):
        self.is_paused = self.pause_button.isChecked()
        if self.is_paused:
            self.pause_button.setText("Resume")
        else:
            self.pause_button.setText("Pause")
