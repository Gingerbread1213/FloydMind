# game_menu_window.py
from PyQt5.QtWidgets import QPushButton, QVBoxLayout
from PyQt5.QtCore import Qt, QSize
from ui.base_window import BaseWindow  # Import the BaseWindow

class GameMenuWindow(BaseWindow):
    def __init__(self, media_player):
        super().__init__(media_player, title="Game Menu", header_text="Enjoy the Games")
        self.init_game_menu_ui()

    def init_game_menu_ui(self):
        # Game buttons
        game_buttons = [
            ("Tic-Tac-Toe", self.open_tic_tac_toe),
            ("Memory Matching Game", self.open_memory_game),
            ("Hangman", self.open_hangman),
            ("Snake Game", self.open_snake_game),
            ("Tetris", self.open_tetris_game)
        ]

        for text, slot in game_buttons:
            button = QPushButton(f" {text}")
            button.setIconSize(QSize(40, 40))
            button.setStyleSheet("""
                background-color: #80CBC4;
                border-radius: 15px;
                color: white;
                padding: 15px;
                font-weight: bold;
                font-size: 21px;
                text-align: left;
            """)
            button.clicked.connect(slot)
            self.content_layout.addWidget(button)

    def open_tic_tac_toe(self):
        from games.tic_tac_toe import TicTacToeWindow  # Adjust the import path as necessary
        self.tic_tac_toe_window = TicTacToeWindow(self.media_player)
        self.tic_tac_toe_window.show()
        self.close()

    def open_memory_game(self):
        from games.memory_game import MemoryGameWindow  # Adjust the import path as necessary
        self.memory_game_window = MemoryGameWindow(self.media_player)
        self.memory_game_window.show()
        self.close()

    def open_hangman(self):
        from games.hangman import HangmanWindow  # Adjust the import path as necessary
        self.hangman_window = HangmanWindow(self.media_player)
        self.hangman_window.show()
        self.close()

    def open_snake_game(self):
        from games.snake_game import SnakeWindow  # Adjust the import path as necessary
        self.snake_window = SnakeWindow(self.media_player)
        self.snake_window.show()
        self.close()

    def open_tetris_game(self):
        from games.tetris_game import TetrisWindow  # Adjust the import path as necessary
        self.tetris_window = TetrisWindow(self.media_player)
        self.tetris_window.show()
        self.close()
