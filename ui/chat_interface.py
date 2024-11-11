# chat_interface.py
from PyQt5.QtWidgets import QLabel, QPushButton, QTextEdit, QLineEdit, QHBoxLayout
from PyQt5.QtCore import Qt, QTimer
from PyQt5 import QtWidgets, QtCore
from models.chatbot_model import generate_response
from ui.base_window import BaseWindow  # Import the BaseWindow

class ChatInterface(BaseWindow):
    def __init__(self, media_player):
        super().__init__(media_player, title="Chatbot Interface", header_text="Chat with Assistant")
        self.init_chat_ui()
        self.typing_timer = QTimer()
        self.typing_timer.timeout.connect(self.show_next_char)
        self.message_buffer = ""
        self.current_message = ""
        self.char_index = 0
        self.conversation = []

        # Start the bot's initial message
        self.start_typing_ai_message()

    def init_chat_ui(self):
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
        self.content_layout.addWidget(self.chat_display)

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

        self.content_layout.addLayout(self.input_layout)

        # Connect Enter key to send message
        self.text_input.returnPressed.connect(self.send_button.click)

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
