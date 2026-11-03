import sys

from PySide6.QtWidgets import QApplication

from model.pelican_model import PelicanModel
from view.pelican_window import PelicanWindow
from controller.pelican_controller import PelicanController


def main():
    app = QApplication(sys.argv)

    model = PelicanModel()
    window = PelicanWindow()

    controller = PelicanController(window, model)

    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()