import sys

from PySide6.QtWidgets import QApplication

from model.pelican_model import PelicanModel
from view.pelican_window import PelicanWindow
from controller.pelican_controller import PelicanController
from pathlib import Path
from PySide6.QtGui import QIcon


def main():
    app = QApplication(sys.argv)

    model = PelicanModel()
    window = PelicanWindow()

    controller = PelicanController(window, model)

    icon_path = Path(__file__).resolve().parent / "assets" / "pelican.png"

    window.setWindowIcon(QIcon(str(icon_path)))

    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()