import sys
import os
from PyQt5 import QtWidgets
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent, QMediaPlaylist
from PyQt5.QtCore import QUrl

from ui.start_window import StartWindow

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)

    # Initialize media player and playlist
    media_player = QMediaPlayer()
    playlist = QMediaPlaylist()

    # Load a music file
    current_path = os.getcwd()
    music_file = os.path.join(current_path, 'assets', 'resources', 'bgm.mp3')
    if os.path.exists(music_file):
        url = QUrl.fromLocalFile(music_file)
        playlist.addMedia(QMediaContent(url))
        playlist.setPlaybackMode(QMediaPlaylist.Loop)
        media_player.setPlaylist(playlist)
        media_player.setVolume(50)
        media_player.play()
    else:
        print("Music file not found. Music will not play.")

    # Stop music when the app is about to quit
    app.aboutToQuit.connect(media_player.stop)

    start_window = StartWindow(media_player)
    start_window.show()
    sys.exit(app.exec_())
