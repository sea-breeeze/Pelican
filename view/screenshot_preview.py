from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QLabel,
    QPushButton, QHBoxLayout
)
from PySide6.QtGui import QPixmap
from PySide6.QtCore import Qt


class ScreenshotPreview(QDialog):

    def __init__(self, image_bytes, parent=None):
        super().__init__(parent)

        self.setWindowTitle("Pelican - Screenshot Preview")
        self.resize(700, 500)

        layout = QVBoxLayout(self)

        self.image_label = QLabel()
        self.image_label.setAlignment(
            Qt.AlignmentFlag.AlignCenter
        )

        pixmap = QPixmap()
        pixmap.loadFromData(image_bytes)

        self.image_label.setPixmap(
            pixmap.scaled(
                650,
                450,
                Qt.AspectRatioMode.KeepAspectRatio,
                Qt.TransformationMode.SmoothTransformation
            )
        )

        layout.addWidget(self.image_label)
        # Create a horizontal layout for the buttons
        button_layout = QHBoxLayout()

        self.confirm_button = QPushButton("Confirm Screenshot")
        self.discard_button = QPushButton("Discard")

        # Connect buttons to dialog actions
        self.confirm_button.clicked.connect(self.accept)
        self.discard_button.clicked.connect(self.reject)

        # Add buttons side by side
        button_layout.addWidget(self.confirm_button)
        button_layout.addWidget(self.discard_button)

        # Add the button layout below the image
        layout.addLayout(button_layout)
