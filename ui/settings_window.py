# settings_window.py
from PyQt5.QtWidgets import QLabel, QPushButton, QSlider, QVBoxLayout
from PyQt5.QtCore import Qt
from ui.base_window import BaseWindow  # Import the BaseWindow

class SettingsWindow(BaseWindow):
    def __init__(self, media_player):
        super().__init__(media_player, title="Settings", header_text="Settings")
        self.init_settings_ui()

    def init_settings_ui(self):
        # Volume slider
        volume_label = QLabel("Music Volume")
        volume_label.setAlignment(Qt.AlignCenter)
        volume_label.setStyleSheet("font-size: 21px; font-weight: bold; color: #004D40;")
        self.content_layout.addWidget(volume_label)

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
        self.content_layout.addWidget(self.volume_slider)

    def adjust_volume(self, value):
        self.media_player.setVolume(value)
