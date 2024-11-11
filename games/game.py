from PyQt5.QtWidgets import QWidget
from PyQt5 import QtWidgets

class GameWindow(QWidget):
    def __init__(self, media_player):
        super().__init__()
        self.media_player = media_player

    def center(self):
        qr = self.frameGeometry()
        cp = QtWidgets.QApplication.primaryScreen().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def go_back(self):
        from ui.game_menu_window import GameMenuWindow  # Import inside method
        self.game_menu_window = GameMenuWindow(self.media_player)
        self.game_menu_window.show()
        self.close()
