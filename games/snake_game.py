import random
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QSlider, QMessageBox
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QPainter, QColor
from PyQt5 import QtWidgets
from games.game import GameWindow

class SnakeWindow(GameWindow):
    def __init__(self, media_player):
        super().__init__(media_player)
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Snake Game')
        self.resize(1000, 800)
        self.center()
        self.setStyleSheet("background-color: #E3F2FD;")

        self.game_area = SnakeGameArea(self)

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

        header_label = QLabel("Snake Game")
        header_label.setAlignment(Qt.AlignCenter)
        header_label.setStyleSheet("font-size: 27px; font-weight: bold; color: #004D40; padding: 10px;")
        header_layout.addWidget(header_label)
        header_layout.addStretch()
        self.main_layout.addLayout(header_layout)

        # Center the game area
        self.game_area_container = QWidget()
        self.game_area_layout = QHBoxLayout()
        self.game_area_layout.addStretch()
        self.game_area_layout.addWidget(self.game_area)
        self.game_area_layout.addStretch()
        self.game_area_container.setLayout(self.game_area_layout)
        self.main_layout.addWidget(self.game_area_container)

        # Speed slider
        self.speed_slider = QSlider(Qt.Horizontal)
        self.speed_slider.setMinimum(50)
        self.speed_slider.setMaximum(300)
        self.speed_slider.setValue(self.game_area.speed)
        self.speed_slider.setStyleSheet("""
            QSlider::handle:horizontal {
                background-color: #4DB6AC;
                border: 1px solid #B2DFDB;
                width: 15px;
            }
        """)
        self.speed_slider.valueChanged.connect(self.adjust_speed)
        self.main_layout.addWidget(self.speed_slider)

        self.setLayout(self.main_layout)

        # Start the game
        self.game_area.start_game()

    def adjust_speed(self, value):
        self.game_area.speed = value
        if self.game_area.timer.isActive():
            self.game_area.timer.start(self.game_area.speed)

    def closeEvent(self, event):
        self.game_area.timer.stop()
        event.accept()

    def pause_game(self):
        if self.pause_button.isChecked():
            self.game_area.timer.stop()
            self.pause_button.setText("Resume")
        else:
            self.pause_button.setText("Pause")
            self.game_area.pause_game()
            self.game_area.show_countdown()


class SnakeGameArea(QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.setFocusPolicy(Qt.StrongFocus)
        self.initGame()

    def initGame(self):
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.gameLoop)
        self.score = 0
        self.speed = 100  # Lower is faster
        self.cell_size = 20
        self.cols = 30
        self.rows = 20
        self.width = self.cols * self.cell_size
        self.height = self.rows * self.cell_size
        self.setFixedSize(self.width, self.height)
        self.countdown_label = QLabel(self)
        self.countdown_label.setAlignment(Qt.AlignCenter)
        self.countdown_label.setStyleSheet("font-size: 49px; font-weight: bold; color: #ff0000;")
        self.countdown_label.setGeometry(0, 0, self.width, self.height)
        self.countdown_label.hide()
        self.reset_game()

    def reset_game(self):
        self.direction = 'RIGHT'
        self.snake = [(5, 10), (4, 10), (3, 10)]
        self.spawn_food()
        self.timer.start(self.speed)

    def start_game(self):
        self.reset_game()

    def pause_game(self):
        self.timer.stop()

    def resume_game(self):
        self.countdown_label.hide()
        self.timer.start(self.speed)

    def show_countdown(self):
        self.countdown = 3
        self.countdown_label.setText(str(self.countdown))
        self.countdown_label.show()
        self.countdown_timer = QTimer()
        self.countdown_timer.timeout.connect(self.update_countdown)
        self.countdown_timer.start(1000)

    def update_countdown(self):
        self.countdown -= 1
        if self.countdown > 0:
            self.countdown_label.setText(str(self.countdown))
        else:
            self.countdown_timer.stop()
            self.resume_game()

    def spawn_food(self):
        while True:
            x = random.randint(0, self.cols - 1)
            y = random.randint(0, self.rows - 1)
            if (x, y) not in self.snake:
                self.food = (x, y)
                break

    def gameLoop(self):
        head = self.snake[0]
        x, y = head
        if self.direction == 'LEFT':
            x -= 1
        elif self.direction == 'RIGHT':
            x += 1
        elif self.direction == 'UP':
            y -= 1
        elif self.direction == 'DOWN':
            y += 1
        new_head = (x, y)

        # Check for collisions
        if (x < 0 or x >= self.cols or y < 0 or y >= self.rows or new_head in self.snake):
            self.timer.stop()
            QMessageBox.information(self, "Game Over", f"Your score: {self.score}")
            self.reset_game()
            return

        self.snake.insert(0, new_head)
        if new_head == self.food:
            self.score += 1
            self.spawn_food()
        else:
            self.snake.pop()
        self.update()

    def keyPressEvent(self, event):
        key = event.key()
        if key == Qt.Key_Left and self.direction != 'RIGHT':
            self.direction = 'LEFT'
        elif key == Qt.Key_Right and self.direction != 'LEFT':
            self.direction = 'RIGHT'
        elif key == Qt.Key_Up and self.direction != 'DOWN':
            self.direction = 'UP'
        elif key == Qt.Key_Down and self.direction != 'UP':
            self.direction = 'DOWN'

    def paintEvent(self, event):
        painter = QPainter(self)
        # Draw snake
        for x, y in self.snake:
            painter.fillRect(x * self.cell_size, y * self.cell_size, self.cell_size, self.cell_size, QColor(0, 128, 0))
        # Draw food
        fx, fy = self.food
        painter.fillRect(fx * self.cell_size, fy * self.cell_size, self.cell_size, self.cell_size, QColor(255, 0, 0))
        # Draw grid lines (optional)
        painter.setPen(QColor(220, 220, 220))
        for x in range(self.cols):
            painter.drawLine(x * self.cell_size, 0, x * self.cell_size, self.height)
        for y in range(self.rows):
            painter.drawLine(0, y * self.cell_size, self.width, y * self.cell_size)
