from PySide6.QtWidgets import QPushButton
from PySide6.QtCore import Qt


class DraggableButton(QPushButton):

    def __init__(self, text, parent=None):
        super().__init__(text, parent)

        self.drag_start = None
        self.dragging = False

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