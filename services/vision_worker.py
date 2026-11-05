from PySide6.QtCore import QThread, Signal
from services.vision_service import VisionService


class VisionWorker(QThread):
    finished = Signal(str)
    failed = Signal(str)

    def __init__(self, image_bytes, question, inspection_text=""):
        super().__init__()
        self.image_bytes = image_bytes
        self.question = question
        self.inspection_text = inspection_text

    def run(self):
        try:
            service = VisionService()
            answer = service.analyze(
                self.image_bytes,
                self.question,
                self.inspection_text
            )
            self.finished.emit(answer or "No response returned.")
        except Exception as error:
            self.failed.emit(str(error))
