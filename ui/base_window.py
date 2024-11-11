# base_window.py
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLabel
from PyQt5.QtCore import Qt, QSize
from PyQt5 import QtWidgets, QtCore

class BaseWindow(QWidget):
    def __init__(self, media_player, title="Base Window", header_text="Header"):
        super().__init__()
        self.media_player = media_player
        self.title = title
        self.header_text = header_text
        self.initUI()
    
    def initUI(self):
        self.setWindowTitle(self.title)
        self.resize(1000, 800)
        self.center()
        self.setStyleSheet("background-color: #E3F2FD;")
        
        # Main vertical layout
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
        
        header_label = QLabel(self.header_text)
        header_label.setAlignment(Qt.AlignCenter)
        header_label.setStyleSheet("font-size: 27px; font-weight: bold; color: #004D40; padding: 10px;")
        header_layout.addWidget(header_label, alignment=Qt.AlignCenter)
        
        self.main_layout.addLayout(header_layout)
        
        # Placeholder for additional UI components in child classes
        self.content_layout = QVBoxLayout()
        self.main_layout.addLayout(self.content_layout)
        
        self.setLayout(self.main_layout)
    
    def center(self):
        qr = self.frameGeometry()
        cp = QtWidgets.QApplication.primaryScreen().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())
    
    def go_back(self):
        from ui.start_window import StartWindow  # Adjust the import path as necessary
        self.start_window = StartWindow(self.media_player)
        self.start_window.show()
        self.close()
