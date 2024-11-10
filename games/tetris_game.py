import random
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QMessageBox
from PyQt5.QtCore import Qt, QBasicTimer
from PyQt5.QtGui import QPainter, QColor
from PyQt5 import QtWidgets, QtGui

class TetrisWindow(QWidget):
    def __init__(self, media_player):
        super().__init__()
        self.media_player = media_player
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Tetris')
        block_size = 30  # Adjusted block size for better visibility
        self.block_size = block_size
        window_width = TetrisArea.BOARD_WIDTH * block_size + 100  # Extra space for margins
        window_height = TetrisArea.BOARD_HEIGHT * block_size + 100  # Extra space for margins and header
        self.resize(window_width, window_height)
        self.center()
        self.setStyleSheet("background-color: #E0F7FA;")  # Set background color

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

        header_label = QLabel("Tetris")
        header_label.setAlignment(Qt.AlignCenter)
        header_label.setStyleSheet("font-size: 27px; font-weight: bold; color: #004D40; padding: 10px;")
        header_layout.addWidget(header_label)
        header_layout.addStretch()
        self.main_layout.addLayout(header_layout)

        # Center the Tetris area
        self.tetris_area = TetrisArea(self, block_size)
        self.tetris_area_container = QWidget()
        self.tetris_area_layout = QHBoxLayout()
        self.tetris_area_layout.addStretch()
        self.tetris_area_layout.addWidget(self.tetris_area)
        self.tetris_area_layout.addStretch()
        self.tetris_area_container.setLayout(self.tetris_area_layout)
        self.main_layout.addWidget(self.tetris_area_container)

        self.setLayout(self.main_layout)
        self.tetris_area.start()
        self.tetris_area.setFocus()  # Ensure the game area has focus

    def center(self):
        qr = self.frameGeometry()
        cp = QtWidgets.QApplication.primaryScreen().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def closeEvent(self, event):
        self.tetris_area.timer.stop()
        event.accept()

    def go_back(self):
        self.tetris_area.timer.stop()
        from ui.game_menu_window import GameMenuWindow  # Import inside method to avoid circular import
        self.game_menu_window = GameMenuWindow(self.media_player)
        self.game_menu_window.show()
        self.close()

    def pause_game(self):
        if self.pause_button.isChecked():
            self.tetris_area.pause()
            self.pause_button.setText("Resume")
        else:
            self.tetris_area.pause()
            self.pause_button.setText("Pause")

class TetrisArea(QWidget):
    SPEED = 300  # Adjust the speed (lower is faster)
    BOARD_WIDTH = 10
    BOARD_HEIGHT = 20

    SHAPES = [
        [[1, 1, 1, 1]],  # I
        [[1, 1], [1, 1]],  # O
        [[0, 1, 0], [1, 1, 1]],  # T
        [[1, 0, 0], [1, 1, 1]],  # L
        [[0, 0, 1], [1, 1, 1]],  # J
        [[1, 1, 0], [0, 1, 1]],  # S
        [[0, 1, 1], [1, 1, 0]]   # Z
    ]

    COLORS = [
        QColor(77, 182, 172),  # Theme teal colors
        QColor(129, 199, 132),
        QColor(255, 241, 118),
        QColor(244, 143, 177),
        QColor(144, 202, 249),
        QColor(174, 213, 129),
        QColor(240, 98, 146)
    ]

    def __init__(self, parent, block_size):
        super().__init__(parent)
        self.block_size = block_size
        self.setFixedSize(self.BOARD_WIDTH * block_size, self.BOARD_HEIGHT * block_size)
        self.setFocusPolicy(Qt.StrongFocus)  # Accept keyboard focus
        self.setStyleSheet("background-color: #E0F7FA;")  # Set background color
        self.timer = QBasicTimer()
        self.is_paused = False
        self.is_started = False
        self.curX = 0
        self.curY = 0
        self.cur_shape = None
        self.board = []
        self.score = 0
        self.initBoard()

    def initBoard(self):
        self.board = [[0] * TetrisArea.BOARD_WIDTH for _ in range(TetrisArea.BOARD_HEIGHT)]

    def start(self):
        if self.is_started:
            return
        self.is_started = True
        self.new_piece()
        self.timer.start(TetrisArea.SPEED, self)

    def pause(self):
        if not self.is_started:
            return
        self.is_paused = not self.is_paused
        if self.is_paused:
            self.timer.stop()
        else:
            self.timer.start(TetrisArea.SPEED, self)
        self.update()

    def timerEvent(self, event):
        if event.timerId() == self.timer.timerId():
            if not self.move_piece(0, 1):
                self.piece_dropped()
        else:
            super(TetrisArea, self).timerEvent(event)

    def keyPressEvent(self, event):
        if not self.is_started or self.cur_shape is None:
            super(TetrisArea, self).keyPressEvent(event)
            return
        if self.is_paused:
            return
        key = event.key()
        if key == Qt.Key_Left:
            self.move_piece(-1, 0)
        elif key == Qt.Key_Right:
            self.move_piece(1, 0)
        elif key == Qt.Key_Down:
            if not self.move_piece(0, 1):
                self.piece_dropped()
        elif key == Qt.Key_Up:
            self.rotate_piece()
        elif key == Qt.Key_Space:
            self.drop_piece()
        elif key == Qt.Key_P:
            self.pause()
        else:
            super(TetrisArea, self).keyPressEvent(event)

    def paintEvent(self, event):
        painter = QPainter(self)
        rect = self.contentsRect()
        board_top = rect.bottom() - TetrisArea.BOARD_HEIGHT * self.block_size
        # Draw board
        for i in range(TetrisArea.BOARD_HEIGHT):
            for j in range(TetrisArea.BOARD_WIDTH):
                shape = self.board[i][j]
                if shape:
                    self.draw_square(painter,
                                     rect.left() + j * self.block_size,
                                     board_top + i * self.block_size,
                                     shape)
        # Draw current piece
        if self.cur_shape is not None:
            for i in range(len(self.cur_shape)):
                for j in range(len(self.cur_shape[i])):
                    if self.cur_shape[i][j]:
                        self.draw_square(painter,
                                         rect.left() + (self.curX + j) * self.block_size,
                                         board_top + (self.curY + i) * self.block_size,
                                         self.cur_shape_num + 1)
        # Draw score
        painter.setPen(QColor(0, 0, 0))
        painter.setFont(QtGui.QFont('Arial', 14))
        painter.drawText(5, 15, f"Score: {self.score}")

    def draw_square(self, painter, x, y, shape):
        color = TetrisArea.COLORS[shape - 1]
        size = self.block_size
        x = int(x)
        y = int(y)
        size = int(size)
        painter.fillRect(x + 1, y + 1, size - 2, size - 2, color)
        painter.setPen(color.lighter())
        painter.drawLine(x, y + size - 1, x, y)
        painter.drawLine(x, y, x + size - 1, y)
        painter.setPen(color.darker())
        painter.drawLine(x + 1, y + size - 1, x + size - 1, y + size - 1)
        painter.drawLine(x + size - 1, y + size - 1, x + size - 1, y + 1)

    def new_piece(self):
        self.cur_shape_num = random.randint(0, len(TetrisArea.SHAPES) - 1)
        self.cur_shape = TetrisArea.SHAPES[self.cur_shape_num]
        self.curX = TetrisArea.BOARD_WIDTH // 2 - len(self.cur_shape[0]) // 2
        self.curY = 0
        if not self.is_valid_position(self.curX, self.curY):
            self.cur_shape = None
            self.timer.stop()
            QMessageBox.information(self, "Game Over", f"Your score: {self.score}")
            self.reset_game()

    def reset_game(self):
        self.initBoard()
        self.score = 0
        self.is_started = False
        self.start()

    def move_piece(self, dx, dy):
        newX = self.curX + dx
        newY = self.curY + dy
        if self.is_valid_position(newX, newY):
            self.curX = newX
            self.curY = newY
            self.update()
            return True
        return False

    def rotate_piece(self):
        rotated_shape = [list(row) for row in zip(*self.cur_shape[::-1])]
        old_shape = self.cur_shape
        self.cur_shape = rotated_shape
        if not self.is_valid_position(self.curX, self.curY):
            self.cur_shape = old_shape
        else:
            self.update()

    def drop_piece(self):
        while self.move_piece(0, 1):
            pass
        self.piece_dropped()

    def piece_dropped(self):
        # Lock the piece into the board
        for i in range(len(self.cur_shape)):
            for j in range(len(self.cur_shape[i])):
                if self.cur_shape[i][j]:
                    self.board[self.curY + i][self.curX + j] = self.cur_shape_num + 1
        self.remove_full_lines()
        self.new_piece()

    def remove_full_lines(self):
        new_board = []
        removed_lines = 0
        for i in range(TetrisArea.BOARD_HEIGHT):
            if 0 in self.board[i]:
                new_board.append(self.board[i])
            else:
                removed_lines += 1
        for _ in range(removed_lines):
            new_board.insert(0, [0] * TetrisArea.BOARD_WIDTH)
        self.board = new_board
        self.score += removed_lines * 10
        self.update()

    def is_valid_position(self, x, y):
        for i in range(len(self.cur_shape)):
            for j in range(len(self.cur_shape[i])):
                if self.cur_shape[i][j]:
                    if (x + j < 0 or x + j >= TetrisArea.BOARD_WIDTH or
                        y + i >= TetrisArea.BOARD_HEIGHT or
                        self.board[y + i][x + j]):
                        return False
        return True
