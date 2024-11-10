from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QSlider
from PyQt5.QtCore import Qt
from PyQt5 import QtWidgets

class SettingsWindow(QWidget):
    def __init__(self, media_player):
        super().__init__()
        self.media_player = media_player
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Settings')
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
        header_layout.addWidget(self.back_button, alignment=Qt.AlignTop)

        header_label = QLabel("Settings")
        header_label.setAlignment(Qt.AlignCenter)
        header_label.setStyleSheet("font-size: 27px; font-weight: bold; color: #004D40; padding: 12px;")
        header_layout.addWidget(header_label, alignment=Qt.AlignCenter)

        self.main_layout.addLayout(header_layout)

        # Volume slider
        volume_label = QLabel("Music Volume")
        volume_label.setAlignment(Qt.AlignCenter)
        volume_label.setStyleSheet("font-size: 21px; font-weight: bold; color: #004D40;")
        self.main_layout.addWidget(volume_label)

        self.volume_slider = QSlider(Qt.Horizontal)
        self.volume_slider.setMinimum(0)
        self.volume_slider.setMaximum(100)
        self.volume_slider.setValue(self.media_player.volume())
        self.volume_slider.setStyleSheet("""
            QSlider::handle:horizontal {
                background-color: #4DB6AC;
                border: 1px solid #B2DFDB;
                width: 15px;
            }
        """)
        self.volume_slider.valueChanged.connect(self.adjust_volume)
        self.main_layout.addWidget(self.volume_slider)

        self.setLayout(self.main_layout)

    def center(self):
        qr = self.frameGeometry()
        cp = QtWidgets.QApplication.primaryScreen().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def adjust_volume(self, value):
        self.media_player.setVolume(value)

    def go_back(self):
        from ui.start_window import StartWindow  # Import inside method to avoid circular import
        self.start_window = StartWindow(self.media_player)
        self.start_window.show()
        self.close()
