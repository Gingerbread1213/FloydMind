import random
from PyQt5.QtWidgets import (
    QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QMessageBox
)
from PyQt5.QtCore import Qt, QTimer
from PyQt5 import QtWidgets
from games.game import GameWindow

class TicTacToeWindow(GameWindow):
    def __init__(self, media_player):
        super().__init__(media_player)
        self.is_paused = False
        self.agent_thinking = False
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Tic-Tac-Toe')
        self.resize(1000, 800)
        self.center()
        self.setStyleSheet("background-color: #E3F2FD;")

        # Main layout
        self.main_layout = QVBoxLayout()

        # Header with Go Back and Pause buttons
        header_layout = QHBoxLayout()
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
        header_layout.addWidget(self.back_button)

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
        header_layout.addWidget(self.pause_button)

        header_label = QLabel("Tic-Tac-Toe")
        header_label.setAlignment(Qt.AlignCenter)
        header_label.setStyleSheet(
            "font-size: 27px; font-weight: bold; color: #004D40; padding: 12px;"
        )
        header_layout.addWidget(header_label)
        header_layout.addStretch()
        self.main_layout.addLayout(header_layout)

        # Game board
        self.create_board()

        self.setLayout(self.main_layout)

        # Agent starts the game
        self.agent_thinking = True
        QTimer.singleShot(1000, self.computer_move)

    def create_board(self):
        self.board = ['' for _ in range(9)]
        self.buttons = []
        grid_layout = QtWidgets.QGridLayout()
        for i in range(9):
            button = QPushButton("")
            button.setFixedSize(200, 200)
            button.setStyleSheet("""
                font-size: 49px;
                font-weight: bold;
                background-color: #ffffff;
                border: 1px solid #B2DFDB;
            """)
            button.clicked.connect(
                lambda _, idx=i: self.make_move(idx)
            )
            self.buttons.append(button)
            grid_layout.addWidget(button, i // 3, i % 3)
        self.main_layout.addLayout(grid_layout)

    def get_button_style(self, player):
        color = '#d32f2f' if player == 'X' else '#1976d2'
        return f"""
            font-size: 49px;
            font-weight: bold;
            color: {color};
            background-color: #ffffff;
            border: 1px solid #B2DFDB;
        """

    def make_move(self, index):
        if self.board[index] == '' and not self.is_paused \
                and not self.agent_thinking:
            self.board[index] = 'X'
            self.buttons[index].setText('X')
            self.buttons[index].setStyleSheet(self.get_button_style('X'))
            if not self.check_winner('X'):
                self.agent_thinking = True
                QTimer.singleShot(1000, self.computer_move)

    def computer_move(self):
        if self.is_paused:
            return
        available_moves = [i for i, spot in enumerate(self.board) if spot == '']
        if available_moves:
            index = random.choice(available_moves)
            self.board[index] = 'O'
            self.buttons[index].setText('O')
            self.buttons[index].setStyleSheet(self.get_button_style('O'))
            self.check_winner('O')
        self.agent_thinking = False

    def check_winner(self, player):
        winning_combinations = [
            (0,1,2), (3,4,5), (6,7,8),  # rows
            (0,3,6), (1,4,7), (2,5,8),  # columns
            (0,4,8), (2,4,6)            # diagonals
        ]
        for combo in winning_combinations:
            if all(self.board[i] == player for i in combo):
                self.show_winner(player)
                return True
        if '' not in self.board:
            self.show_winner(None)
            return True
        return False

    def show_winner(self, player):
        message = f"Player '{player}' wins!" if player else "It's a tie!"
        QMessageBox.information(self, "Game Over", message)
        self.reset_game()

    def reset_game(self):
        self.board = ['' for _ in range(9)]
        for button in self.buttons:
            button.setText('')
            button.setStyleSheet("""
                font-size: 49px;
                font-weight: bold;
                background-color: #ffffff;
                border: 1px solid #B2DFDB;
            """)
        self.agent_thinking = True
        QTimer.singleShot(1000, self.computer_move)

    def pause_game(self):
        self.is_paused = self.pause_button.isChecked()
        if self.is_paused:
            self.pause_button.setText("Resume")
        else:
            self.pause_button.setText("Pause")
