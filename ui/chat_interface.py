from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QTextEdit, QLineEdit
from PyQt5.QtCore import Qt
from PyQt5 import QtWidgets, QtCore
from models.chatbot_model import generate_response

class ChatInterface(QWidget):
    def __init__(self, media_player):
        super().__init__()
        self.media_player = media_player
        self.initUI()
        self.typing_timer = QtCore.QTimer()
        self.typing_timer.timeout.connect(self.show_next_char)
        self.message_buffer = ""
        self.current_message = ""
        self.char_index = 0
        self.conversation = []

        # Start the bot's initial message
        self.start_typing_ai_message()

    def initUI(self):
        self.setWindowTitle('Chatbot Interface')
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

        header_label = QLabel("Chat with Assistant")
        header_label.setAlignment(Qt.AlignCenter)
        header_label.setStyleSheet("font-size: 27px; font-weight: bold; color: #004D40; padding: 10px;")
        header_layout.addWidget(header_label, alignment=Qt.AlignCenter)

        self.main_layout.addLayout(header_layout)

        # Chat display area
        self.chat_display = QTextEdit()
        self.chat_display.setReadOnly(True)
        self.chat_display.setStyleSheet("""
            background-color: #ffffff;
            border: 1px solid #B2DFDB;
            border-radius: 10px;
            padding: 10px;
            color: #004D40;
            font-size: 19px;
        """)
        self.main_layout.addWidget(self.chat_display)

        # Input area
        self.input_layout = QHBoxLayout()

        # Text input field
        self.text_input = QLineEdit()
        self.text_input.setPlaceholderText("Type a message...")
        self.text_input.setStyleSheet("""
            background-color: #ffffff;
            border: 1px solid #80CBC4;
            border-radius: 15px;
            padding: 10px;
            color: #004D40;
            font-size: 19px;
        """)
        self.input_layout.addWidget(self.text_input)

        # Send button
        self.send_button = QPushButton("Send")
        self.send_button.setStyleSheet("""
            background-color: #4DB6AC;
            border-radius: 15px;
            color: white;
            padding: 10px;
            font-weight: bold;
            font-size: 19px;
        """)
        self.send_button.clicked.connect(self.start_typing_user_message)
        self.input_layout.addWidget(self.send_button)

        self.main_layout.addLayout(self.input_layout)

        self.setLayout(self.main_layout)

        # Connect Enter key to send message
        self.text_input.returnPressed.connect(self.send_button.click)

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

    def start_typing_user_message(self):
        # Get the user's message and initiate typing effect
        self.message_buffer = self.text_input.text()
        if self.message_buffer.strip() == "":
            return  # Do not send empty messages
        self.current_message = f"<p style='color: #0078d7; font-size:19px;'><b>You:</b> "
        self.char_index = 0
        self.typing_timer.start(50)
        self.text_input.clear()

    def start_typing_ai_message(self):
        if len(self.conversation) == 0:
            self.message_buffer = "Hello! How can I assist you today? Feel free to ask me anything."
        else:
            last_user_message = self.conversation[-1].split("<b>You:</b>")[-1].split("</p>")[0].strip()
            ai_response = generate_response(last_user_message)
            self.message_buffer = ai_response

        self.current_message = f"<p style='color: #333; font-size:19px;'><b>Assistant:</b> "
        self.char_index = 0
        self.typing_timer.start(50)

    def show_next_char(self):
        if self.char_index < len(self.message_buffer):
            self.current_message += self.message_buffer[self.char_index]
            self.char_index += 1
            self.chat_display.setHtml("".join(self.conversation) + self.current_message + "</p>")
        else:
            self.typing_timer.stop()
            self.conversation.append(self.current_message + "</p>")
            if "<b>Assistant:</b>" in self.current_message:
                return
            if "<b>You:</b>" in self.current_message:
                QtCore.QTimer.singleShot(500, self.start_typing_ai_message)
