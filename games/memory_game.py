import random
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QPushButton, QComboBox, QMessageBox
)
from PyQt5.QtCore import Qt, QTimer
from PyQt5 import QtWidgets

class MemoryGameWindow(QWidget):
    def __init__(self, media_player):
        super().__init__()
        self.media_player = media_player
        self.is_paused = False
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Memory Matching Game')
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

        header_label = QLabel("Memory Matching Game")
        header_label.setAlignment(Qt.AlignCenter)
        header_label.setStyleSheet(
            "font-size: 27px; font-weight: bold; color: #004D40; padding: 12px;"
        )
        header_layout.addWidget(header_label, alignment=Qt.AlignCenter)
        self.main_layout.addLayout(header_layout)

        # Difficulty selection
        difficulty_label = QLabel("Select Difficulty:")
        difficulty_label.setAlignment(Qt.AlignCenter)
        difficulty_label.setStyleSheet(
            "font-size: 19px; font-weight: bold; color: #004D40;"
        )
        self.main_layout.addWidget(difficulty_label)

        self.difficulty_combo = QComboBox()
        self.difficulty_combo.addItems(['Easy', 'Medium', 'Hard'])
        self.difficulty_combo.currentIndexChanged.connect(self.reset_game)
        self.main_layout.addWidget(self.difficulty_combo)

        # Game board container
        self.grid_widget = QWidget()
        self.grid_layout = QtWidgets.QGridLayout()
        self.grid_widget.setLayout(self.grid_layout)
        self.main_layout.addWidget(self.grid_widget)

        self.setLayout(self.main_layout)

        # Initialize the game
        self.reset_game()

    def center(self):
        qr = self.frameGeometry()
        cp = QtWidgets.QApplication.primaryScreen().availableGeometry() \
            .center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def create_board(self):
        self.grid_size = self.get_grid_size()
        total_pairs = (self.grid_size * self.grid_size) // 2
        symbols_list = [chr(i) for i in range(65, 65 + total_pairs)] * 2
        random.shuffle(symbols_list)
        self.symbols = symbols_list

        self.buttons = []
        self.first_choice = None
        self.second_choice = None
        self.locked = False

        # Clear existing widgets
        for i in reversed(range(self.grid_layout.count())):
            widget = self.grid_layout.itemAt(i).widget()
            if widget is not None:
                widget.setParent(None)

        for i in range(self.grid_size * self.grid_size):
            button = QPushButton("")
            button.setFixedSize(80, 80)
            button.setStyleSheet("""
                font-size: 37px;
                font-weight: bold;
                background-color: #ffffff;
                border: 1px solid #B2DFDB;
            """)
            button.clicked.connect(
                lambda _, idx=i: self.reveal_symbol(idx)
            )
            button.symbol = self.symbols[i]
            button.is_revealed = False
            self.buttons.append(button)
            self.grid_layout.addWidget(button, i // self.grid_size, i % self.grid_size)

    def get_grid_size(self):
        difficulty = self.difficulty_combo.currentText()
        return {'Easy': 4, 'Medium': 6, 'Hard': 8}[difficulty]

    def reveal_symbol(self, index):
        if self.locked or self.is_paused or self.buttons[index].is_revealed:
            return

        self.buttons[index].setText(self.buttons[index].symbol)
        self.buttons[index].is_revealed = True

        if self.first_choice is None:
            self.first_choice = index
        elif self.second_choice is None:
            self.second_choice = index
            self.check_match()

    def check_match(self):
        if self.buttons[self.first_choice].symbol == \
                self.buttons[self.second_choice].symbol:
            self.first_choice = None
            self.second_choice = None
            if all(button.is_revealed for button in self.buttons):
                QMessageBox.information(self, "Game Over",
                                        "You've matched all pairs!")
                self.reset_game()
        else:
            self.locked = True
            QTimer.singleShot(1000, self.hide_symbols)

    def hide_symbols(self):
        self.buttons[self.first_choice].setText('')
        self.buttons[self.second_choice].setText('')
        self.buttons[self.first_choice].is_revealed = False
        self.buttons[self.second_choice].is_revealed = False
        self.first_choice = None
        self.second_choice = None
        self.locked = False

    def reset_game(self):
        self.create_board()

    def go_back(self):
        from ui.game_menu_window import GameMenuWindow  # Import inside method
        self.game_menu_window = GameMenuWindow(self.media_player)
        self.game_menu_window.show()
        self.close()

    def pause_game(self):
        self.is_paused = self.pause_button.isChecked()
        if self.is_paused:
            self.pause_button.setText("Resume")
        else:
            self.pause_button.setText("Pause")
