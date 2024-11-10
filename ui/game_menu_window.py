from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton
from PyQt5.QtCore import Qt
from PyQt5 import QtWidgets, QtCore

class GameMenuWindow(QWidget):
    def __init__(self, media_player):
        super().__init__()
        self.media_player = media_player
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Game Menu')
        self.resize(1000, 800)
        self.center()
        self.setStyleSheet("background-color: #E3F2FD;")

        # Main layout
        self.main_layout = QVBoxLayout()

        # Header with Go Back button
        header_layout = QVBoxLayout()
        self.back_button = QPushButton("Go Back")
        self.back_button.setStyleSheet("""
            background-color: #00897B;
            border-radius: 10px;
            color: white;
            padding: 5px;
            font-weight: bold;
            font-size: 17px;
        """)
        self.back_button.clicked.connect(self.go_back)
        header_layout.addWidget(self.back_button, alignment=Qt.AlignTop | Qt.AlignLeft)

        header_label = QLabel("Enjoy the Games")
        header_label.setAlignment(Qt.AlignCenter)
        header_label.setStyleSheet("font-size: 31px; font-weight: bold; color: #004D40; padding: 12px;")
        header_layout.addWidget(header_label, alignment=Qt.AlignCenter)

        self.main_layout.addLayout(header_layout)

        # Game buttons
        self.tic_tac_toe_button = QPushButton(" Tic-Tac-Toe")
        self.tic_tac_toe_button.setIconSize(QtCore.QSize(40, 40))
        self.tic_tac_toe_button.setStyleSheet("""
            background-color: #80CBC4;
            border-radius: 15px;
            color: white;
            padding: 15px;
            font-weight: bold;
            font-size: 21px;
            text-align: left;
        """)
        self.tic_tac_toe_button.clicked.connect(self.open_tic_tac_toe)
        self.main_layout.addWidget(self.tic_tac_toe_button)

        self.memory_game_button = QPushButton(" Memory Matching Game")
        self.memory_game_button.setIconSize(QtCore.QSize(40, 40))
        self.memory_game_button.setStyleSheet("""
            background-color: #80CBC4;
            border-radius: 15px;
            color: white;
            padding: 15px;
            font-weight: bold;
            font-size: 21px;
            text-align: left;
        """)
        self.memory_game_button.clicked.connect(self.open_memory_game)
        self.main_layout.addWidget(self.memory_game_button)

        self.hangman_button = QPushButton(" Hangman")
        self.hangman_button.setIconSize(QtCore.QSize(40, 40))
        self.hangman_button.setStyleSheet("""
            background-color: #80CBC4;
            border-radius: 15px;
            color: white;
            padding: 15px;
            font-weight: bold;
            font-size: 21px;
            text-align: left;
        """)
        self.hangman_button.clicked.connect(self.open_hangman)
        self.main_layout.addWidget(self.hangman_button)

        self.snake_button = QPushButton(" Snake Game")
        self.snake_button.setIconSize(QtCore.QSize(40, 40))
        self.snake_button.setStyleSheet("""
            background-color: #80CBC4;
            border-radius: 15px;
            color: white;
            padding: 15px;
            font-weight: bold;
            font-size: 21px;
            text-align: left;
        """)
        self.snake_button.clicked.connect(self.open_snake_game)
        self.main_layout.addWidget(self.snake_button)

        self.tetris_button = QPushButton(" Tetris")
        self.tetris_button.setIconSize(QtCore.QSize(40, 40))
        self.tetris_button.setStyleSheet("""
            background-color: #80CBC4;
            border-radius: 15px;
            color: white;
            padding: 15px;
            font-weight: bold;
            font-size: 21px;
            text-align: left;
        """)
        self.tetris_button.clicked.connect(self.open_tetris_game)
        self.main_layout.addWidget(self.tetris_button)

        self.setLayout(self.main_layout)

    def center(self):
        qr = self.frameGeometry()
        cp = QtWidgets.QApplication.primaryScreen().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def go_back(self):
        from ui.start_window import StartWindow  # Import inside method
        self.start_window = StartWindow(self.media_player)
        self.start_window.show()
        self.close()

    def open_tic_tac_toe(self):
        from games.tic_tac_toe import TicTacToeWindow  # Import inside method
        self.tic_tac_toe_window = TicTacToeWindow(self.media_player)
        self.tic_tac_toe_window.show()
        self.close()

    def open_memory_game(self):
        from games.memory_game import MemoryGameWindow  # Import inside method
        self.memory_game_window = MemoryGameWindow(self.media_player)
        self.memory_game_window.show()
        self.close()

    def open_hangman(self):
        from games.hangman import HangmanWindow  # Import inside method
        self.hangman_window = HangmanWindow(self.media_player)
        self.hangman_window.show()
        self.close()

    def open_snake_game(self):
        from games.snake_game import SnakeWindow  # Import inside method
        self.snake_window = SnakeWindow(self.media_player)
        self.snake_window.show()
        self.close()

    def open_tetris_game(self):
        from games.tetris_game import TetrisWindow  # Import inside method
        self.tetris_window = TetrisWindow(self.media_player)
        self.tetris_window.show()
        self.close()
