from PySide6.QtWidgets import QWidget
from PySide6.QtCore import Qt, QRectF
from PySide6.QtGui import QPainter, QColor, QPen
from PySide6.QtCore import Qt, QRectF, QTimer

class HighlightOverlay(QWidget):

    def __init__(self):
        super().__init__()

        self.setWindowFlags(
            Qt.WindowType.FramelessWindowHint
            | Qt.WindowType.WindowStaysOnTopHint
            | Qt.WindowType.Tool
            | Qt.WindowType.WindowTransparentForInput
        )

        self.setAttribute(
            Qt.WidgetAttribute.WA_TranslucentBackground
        )

        self.setAttribute(
            Qt.WidgetAttribute.WA_TransparentForMouseEvents
        )

        self.setAttribute(
            Qt.WidgetAttribute.WA_ShowWithoutActivating
        )

        self.resize(1, 1)

        self.target_control = None

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_target_position)

    def highlight(self, left, top, width, height):
        if width <= 0 or height <= 0:
            self.hide()
            return

        # Add a little padding around the element
        padding = 4

        self.setGeometry(
            int(left - padding),
            int(top - padding),
            int(width + padding * 2),
            int(height + padding * 2)
        )

        self.show()
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        pen = QPen(QColor("#00C896"))
        pen.setWidth(3)

        painter.setPen(pen)
        painter.setBrush(Qt.BrushStyle.NoBrush)

        rectangle = QRectF(self.rect()).adjusted(
            2, 2, -2, -2
        )

        painter.drawRoundedRect(rectangle, 6, 6)
        painter.end()

        
    def track_control(self, control):
        self.target_control = control

        self.update_target_position()
        self.timer.start(200)


    def update_target_position(self):
        if self.target_control is None:
            return

        try:
            rectangle = self.target_control.BoundingRectangle

            width = rectangle.width()
            height = rectangle.height()

            if width <= 0 or height <= 0:
                self.stop_tracking()
                return

            self.highlight(
                rectangle.left,
                rectangle.top,
                width,
                height
            )

        except Exception:
            self.stop_tracking()


    def stop_tracking(self):
        self.timer.stop()
        self.target_control = None
        self.hide()
