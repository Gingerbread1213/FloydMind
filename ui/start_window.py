import os
import random
from PyQt5.QtWidgets import QLabel, QPushButton, QWidget, QVBoxLayout
from PyQt5.QtGui import QMovie
from PyQt5.QtCore import Qt
from PyQt5 import QtWidgets

from assets.quotes import quotes

class StartWindow(QWidget):
    def __init__(self, media_player):
        super().__init__()
        self.media_player = media_player
        self.initUI()

    def initUI(self):
        self.setWindowTitle('FloydMind')
        self.resize(1000, 800)
        self.center()

        # Create a QLabel to display the GIF
        self.background_label = QLabel(self)
        self.background_label.setGeometry(0, 0, self.width(), self.height())
        self.background_label.setScaledContents(True)

        # Load the GIF file
        current_path = os.getcwd()
        gif_file = os.path.join(current_path, 'assets', 'resources', 'background.gif')
        if os.path.exists(gif_file):
            self.movie = QMovie(gif_file)
            self.background_label.setMovie(self.movie)
            self.movie.start()
        else:
            print("GIF file not found. Background animation will not play.")

        # Main layout
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(0, 0, 0, 0)

        # Overlay widget to hold the content on top of the GIF
        self.overlay_widget = QWidget(self)
        self.overlay_widget.setStyleSheet("background-color: rgba(0, 0, 0, 80);")
        self.overlay_layout = QVBoxLayout(self.overlay_widget)
        self.overlay_layout.setAlignment(Qt.AlignCenter)
        self.overlay_layout.setContentsMargins(20, 20, 20, 20)

        # Header
        header = QLabel("FloydMind")
        header.setAlignment(Qt.AlignCenter)
        header.setStyleSheet("font-size: 35px; font-weight: bold; color: #FFFFFF; padding: 12px;")
        self.overlay_layout.addWidget(header)

        # Display random quote
        quote = random.choice(quotes)
        quote_label = QLabel(f"\"{quote}\"")
        quote_label.setAlignment(Qt.AlignCenter)
        quote_label.setWordWrap(True)
        quote_label.setStyleSheet("font-size: 21px; color: #FFFFFF; padding: 10px;")
        self.overlay_layout.addWidget(quote_label)

        # Buttons
        self.chat_button = QPushButton("Chat with Assistant")
        self.chat_button.setStyleSheet("""
            background-color: #4DB6AC;
            border-radius: 15px;
            color: white;
            padding: 15px;
            font-weight: bold;
            font-size: 21px;
        """)
        self.chat_button.clicked.connect(self.open_chat)
        self.overlay_layout.addWidget(self.chat_button)

        self.game_button = QPushButton("Play Games")
        self.game_button.setStyleSheet("""
            background-color: #80CBC4;
            border-radius: 15px;
            color: white;
            padding: 15px;
            font-weight: bold;
            font-size: 21px;
        """)
        self.game_button.clicked.connect(self.open_game_menu)
        self.overlay_layout.addWidget(self.game_button)

        self.settings_button = QPushButton("Settings")
        self.settings_button.setStyleSheet("""
            background-color: #00897B;
            border-radius: 15px;
            color: white;
            padding: 15px;
            font-weight: bold;
            font-size: 21px;
        """)
        self.settings_button.clicked.connect(self.open_settings)
        self.overlay_layout.addWidget(self.settings_button)

        # Add the overlay widget to the main layout
        self.main_layout.addWidget(self.overlay_widget)

        # Ensure the overlay is on top
        self.overlay_widget.raise_()

    def center(self):
        qr = self.frameGeometry()
        cp = QtWidgets.QApplication.primaryScreen().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def resizeEvent(self, event):
        # Resize the background label and overlay widget to cover the entire window
        self.background_label.setGeometry(0, 0, self.width(), self.height())
        self.overlay_widget.setGeometry(0, 0, self.width(), self.height())
        super().resizeEvent(event)

    def open_chat(self):
        from ui.chat_interface import ChatInterface  # Import inside method
        self.chat_interface = ChatInterface(self.media_player)
        self.chat_interface.show()
        self.close()

    def open_game_menu(self):
        from ui.game_menu_window import GameMenuWindow  # Import inside method
        self.game_menu_window = GameMenuWindow(self.media_player)
        self.game_menu_window.show()
        self.close()

    def open_settings(self):
        from ui.settings_window import SettingsWindow  # Import inside method
        self.settings_window = SettingsWindow(self.media_player)
        self.settings_window.show()
        self.close()
