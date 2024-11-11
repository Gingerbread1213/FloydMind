import random
import functools
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QComboBox, QMessageBox, QGridLayout
)
from PyQt5.QtCore import Qt, QTimer

from games.game import GameWindow  # Ensure this path is correct based on your project structure

class MemoryGameWindow(GameWindow):
    def __init__(self, media_player=None):
        super().__init__(media_player)
        self.is_paused = False
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Memory Matching Game')
        self.resize(1000, 800)
        self.center()
        self.setStyleSheet("background-color: #E3F2FD;")

        # Main layout
        self.main_layout = QVBoxLayout()
        self.setLayout(self.main_layout)

        # Header with Back and Pause buttons
        header_layout = QHBoxLayout()

        # Back Button
        self.back_button = QPushButton("Back")
        self.back_button.setStyleSheet("""
            background-color: #00897B;
            border-radius: 5px;
            color: white;
            padding: 8px;
            font-weight: bold;
            font-size: 17px;
        """)
        self.back_button.clicked.connect(self.go_back)  # Inherited from GameWindow
        header_layout.addWidget(self.back_button, alignment=Qt.AlignLeft)

        # Pause Button
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
        header_layout.addWidget(self.pause_button, alignment=Qt.AlignRight)

        self.main_layout.addLayout(header_layout)

        # Header Label
        header_label = QLabel("Memory Matching Game")
        header_label.setAlignment(Qt.AlignCenter)
        header_label.setStyleSheet(
            "font-size: 27px; font-weight: bold; color: #004D40; padding: 12px;"
        )
        label_layout = QHBoxLayout()
        label_layout.addStretch()
        label_layout.addWidget(header_label)
        label_layout.addStretch()
        self.main_layout.addLayout(label_layout)

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
        self.main_layout.addWidget(self.difficulty_combo, alignment=Qt.AlignCenter)

        # Game board container
        self.grid_widget = QWidget()
        self.grid_layout = QGridLayout()
        self.grid_widget.setLayout(self.grid_layout)
        self.main_layout.addWidget(self.grid_widget)

        # Initialize the game
        self.reset_game()

    def create_board(self):
        self.grid_size = self.get_grid_size()
        total_pairs = (self.grid_size * self.grid_size) // 2

        # Example with letters
        # Ensure that total_pairs does not exceed available unique symbols
        symbol_pool = [chr(i) for i in range(65, 65 + total_pairs)]  # 'A', 'B', etc.
        
        # Alternatively, use emojis for better visual appeal
        # symbol_pool = ['🍎', '🍌', '🍇', '🍓', '🍒', '🍑', '🥝', '🍍']
        # Adjust the pool size based on grid_size
        # symbols_list = symbol_pool * (self.grid_size * self.grid_size // (2 * len(symbol_pool)))
        
        symbols_list = symbol_pool * 2  # Create pairs
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
            # Updated stylesheet with explicit text color and adjusted font size
            button.setStyleSheet("""
                font-size: 24px;  /* Adjusted font size */
                font-weight: bold;
                color: black;     /* Ensures text is visible */
                background-color: #ffffff;
                border: 1px solid #B2DFDB;
            """)
            # Use functools.partial to bind the current index correctly
            button.clicked.connect(functools.partial(self.reveal_symbol, i))
            button.symbol = self.symbols[i]
            button.is_revealed = False
            self.buttons.append(button)
            self.grid_layout.addWidget(button, i // self.grid_size, i % self.grid_size)
            print(f"Button {i} assigned symbol: {button.symbol}")  # Debug statement

    def get_grid_size(self):
        difficulty = self.difficulty_combo.currentText()
        return {'Easy': 4, 'Medium': 6, 'Hard': 8}.get(difficulty, 4)  # Default to 4 if not found

    def reveal_symbol(self, index):
        if self.locked:
            print("Game is locked. Please wait.")
            return
        if self.is_paused:
            print("Game is paused.")
            return
        if self.buttons[index].is_revealed:
            print(f"Button {index} is already revealed.")
            return

        print(f"Revealing symbol at index: {index} with symbol: {self.buttons[index].symbol}")
        self.buttons[index].setText(self.buttons[index].symbol)
        self.buttons[index].is_revealed = True

        if self.first_choice is None:
            self.first_choice = index
            print(f"First choice set to {index}")
        elif self.second_choice is None:
            self.second_choice = index
            print(f"Second choice set to {index}")
            self.check_match()

    def check_match(self):
        first_symbol = self.buttons[self.first_choice].symbol
        second_symbol = self.buttons[self.second_choice].symbol
        print(f"Checking match: {first_symbol} vs {second_symbol}")

        if first_symbol == second_symbol:
            print("It's a match!")
            self.first_choice = None
            self.second_choice = None
            if all(button.is_revealed for button in self.buttons):
                QMessageBox.information(self, "Game Over",
                                        "You've matched all pairs!")
                self.reset_game()
        else:
            print("Not a match. Hiding symbols.")
            self.locked = True
            QTimer.singleShot(1000, self.hide_symbols)

    def hide_symbols(self):
        print(f"Hiding symbols at indices: {self.first_choice}, {self.second_choice}")
        self.buttons[self.first_choice].setText('')
        self.buttons[self.second_choice].setText('')
        self.buttons[self.first_choice].is_revealed = False
        self.buttons[self.second_choice].is_revealed = False
        self.first_choice = None
        self.second_choice = None
        self.locked = False

    def reset_game(self):
        print("Resetting game.")
        self.create_board()

    def pause_game(self):
        self.is_paused = self.pause_button.isChecked()
        if self.is_paused:
            self.pause_button.setText("Resume")
            self.disable_game_board()
            if self.media_player:
                self.media_player.pause()
            QMessageBox.information(self, "Game Paused", "The game has been paused.")
            print("Game paused.")
        else:
            self.pause_button.setText("Pause")
            self.enable_game_board()
            if self.media_player:
                self.media_player.play()
            print("Game resumed.")

    def disable_game_board(self):
        print("Disabling game board.")
        for button in self.buttons:
            button.setEnabled(False)

    def enable_game_board(self):
        print("Enabling game board.")
        for button in self.buttons:
            if not button.is_revealed:
                button.setEnabled(True)
