from PySide6.QtWidgets import QPushButton
from PySide6.QtCore import Qt
from pathlib import Path
from PySide6.QtGui import QIcon
from PySide6.QtCore import QSize


class DraggableButton(QPushButton):

    def __init__(self, text, parent=None):
        super().__init__(text, parent)

        icon_path = Path(__file__).resolve().parent.parent / "assets" / "pelican.png"

        self.setText("")
        self.setFixedSize(80, 80)
        self.setIcon(QIcon(str(icon_path)))
        self.setIconSize(QSize(70, 70))

        self.drag_start = None
        self.dragging = False

        self.setStyleSheet("""
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

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.drag_start = event.globalPosition().toPoint()
            self.dragging = False

        super().mousePressEvent(event)

    def mouseMoveEvent(self, event):
        if self.drag_start is None:
            return

        if not (event.buttons() & Qt.MouseButton.LeftButton):
            return

        current_position = event.globalPosition().toPoint()
        difference = current_position - self.drag_start

        if difference.manhattanLength() > 5:
            self.dragging = True

        if self.dragging:
            self.window().move(self.window().pos() + difference)
            self.drag_start = current_position

    def mouseReleaseEvent(self, event):
        was_dragging = self.dragging

        self.drag_start = None
        self.dragging = False

        if was_dragging:
            self.setDown(False)
            event.accept()
            return

        super().mouseReleaseEvent(event)