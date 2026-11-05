from PySide6.QtWidgets import (
    QWidget,
    QPushButton,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QTextEdit,
    QComboBox,
)

from PySide6.QtCore import Qt, QRectF
from view.draggable_button import DraggableButton
from PySide6.QtWidgets import QSizeGrip
from PySide6.QtGui import QPainter, QColor, QBrush

class PelicanWindow(QWidget):

    def __init__(self):
        super().__init__()

        self.expanded = False

        self.setWindowTitle("Pelican AI")

        self.setWindowFlags(
            Qt.WindowType.WindowStaysOnTopHint
            | Qt.WindowType.FramelessWindowHint
        )

        self.setAttribute(
            Qt.WidgetAttribute.WA_TranslucentBackground
        )

        # Main layout
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)

        # Header layout
        self.header_layout = QHBoxLayout()

        self.toggle_button = DraggableButton("🐦")
        self.toggle_button.setFixedSize(60, 60)

        self.toggle_button.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                border: none;
                padding: 0px;
            }

            QPushButton:hover {
                background-color: transparent;
                border: none;
            }

            QPushButton:pressed {
                background-color: transparent;
                border: none;
            }
        """)



        self.close_button = QPushButton("✕")
        self.close_button.setFixedSize(35, 35)

        self.inspect_button = QPushButton("Inspect Application")

        self.header_layout.addWidget(self.toggle_button)
        self.header_layout.addStretch()
        self.header_layout.addWidget(self.close_button)

        self.layout.addLayout(self.header_layout)

        # Title
        self.title = QLabel("Hi! I'm Pelican.")
        self.title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.layout.addWidget(self.title)

        # Mode buttons
        self.mode_layout = QHBoxLayout()

        self.chat_button = QPushButton("Chat Mode")
        self.explore_button = QPushButton("Explore Mode")

        self.mode_layout.addWidget(self.chat_button)
        self.mode_layout.addWidget(self.explore_button)

        self.layout.addLayout(self.mode_layout)

        self.mode_layout.setContentsMargins(0, 0, 0, 0)
        self.mode_layout.setSpacing(0)

        # Chat history
        self.chat_display = QTextEdit()

        self.chat_display.setReadOnly(True)
        self.layout.addWidget(self.chat_display)

        # Message input
        self.message_input = QLineEdit()
        self.message_input.setPlaceholderText("Ask Pelican...")
        self.layout.addWidget(self.message_input)

        # Send button
        self.send_button = QPushButton("Analyze with AI")
        self.layout.addWidget(self.send_button)

        # Screenshot capture button
        self.capture_button = QPushButton("📷 Capture Screen")
        self.layout.addWidget(self.capture_button)

        self.window_selector = QComboBox()
        self.window_selector.setPlaceholderText("Select an application")

        self.refresh_button = QPushButton("Refresh Windows")

        self.layout.addWidget(self.inspect_button)

        self.layout.addWidget(self.window_selector)
        self.layout.addWidget(self.refresh_button)

        self.element_selector = QComboBox()
        self.element_selector.setPlaceholderText("Select a UI element")
        self.highlight_button = QPushButton("Highlight Element")
        self.layout.addWidget(self.element_selector)
        self.layout.addWidget(self.highlight_button)
        self.element_selector.hide()



        # Widgets shown only when expanded
        self.panel_widgets = [
            self.window_selector,
            self.refresh_button,
            self.close_button,
            self.title,
            self.chat_display,
            self.message_input,
            self.capture_button,
            self.send_button,
        ]

        self.chat_display.setStyleSheet("""
            QTextEdit {
                background-color: #F3F4F6;
                color: #111827;
                font-size: 15px;
                border: none;
                border-radius: 10px;
                padding: 8px;
            }
        """)

        self.message_input.setStyleSheet("""
            QLineEdit {
                background-color: #F9FAFB;
                color: #111827;
                border: 1px solid #D1D5DB;
                border-radius: 8px;
                padding: 8px;
            }
        """)

        self.send_button.setStyleSheet("""
            QPushButton {
                background-color: #2563EB;
                color: white;
                border: none;
                border-radius: 8px;
                padding: 8px;
            }

            QPushButton:hover {
                background-color: #1D4ED8;
            }
        """)

        self.resize_grip = QSizeGrip(self)
        self.resize_grip.setFixedSize(22, 22)
        self.resize_grip.setStyleSheet("""
            QSizeGrip {
                background: transparent;
            }
        """)

        self.layout.addWidget(
            self.resize_grip,
            alignment=Qt.AlignmentFlag.AlignRight
        )

        self.set_expanded(False)

        # Hide unused mode and inspection controls
        self.chat_button.hide()
        self.explore_button.hide()
        self.element_selector.hide()
        self.highlight_button.hide()
        self.inspect_button.hide()

    def set_expanded(self, expanded):
        self.expanded = expanded

        for widget in self.panel_widgets:
            widget.setVisible(expanded)

        if expanded:
            self.setMinimumSize(350, 450)
            self.resize(500, 650)
        else:
            self.setMinimumSize(350, 450)
            self.resize(500, 650)

        self.update()

    def paintEvent(self, event):
        if not self.expanded:
            return

        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        painter.setPen(Qt.PenStyle.NoPen)
        painter.setBrush(QColor("#FFFFFF"))

        painter.drawRoundedRect(
            QRectF(self.rect()).adjusted(1, 1, -1, -1),
            15,
            15
        )

        painter.end()