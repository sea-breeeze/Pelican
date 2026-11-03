from services.screen_capture import ScreenCapture
from services.window_manager import WindowManager
from view.screenshot_preview import ScreenshotPreview
from PySide6.QtWidgets import QDialog

class PelicanController:


    def __init__(self, view, model):
        self.view = view
        self.model = model
        self.screen_capture = ScreenCapture()

        self.view.toggle_button.clicked.connect(self.toggle_window)
        self.view.close_button.clicked.connect(self.view.close)

        self.view.chat_button.clicked.connect(self.activate_chat)
        self.view.explore_button.clicked.connect(self.activate_explore)

        self.view.send_button.clicked.connect(self.send_message)
        self.view.message_input.returnPressed.connect(self.send_message)

        self.view.capture_button.clicked.connect(self.capture_screen)

        self.window_manager = WindowManager()
        self.available_windows = []

        self.view.refresh_button.clicked.connect(self.refresh_windows)
        self.view.window_selector.currentIndexChanged.connect(
            self.select_window
        )

        self.refresh_windows()

        self.confirmed_screenshot = None

        self.selected_window = None

    def toggle_window(self):
        self.view.set_expanded(not self.view.expanded)

    def activate_chat(self):
        self.model.set_mode("chat")
        self.display_message("Pelican", "Chat Mode activated.")

    def activate_explore(self):
        self.model.set_mode("explore")
        self.display_message("Pelican", "Explore Mode activated.")

    def display_message(self, sender, message):
        self.model.add_message(sender, message)
        self.view.chat_display.append(f"{sender}: {message}")

    def send_message(self):
        message = self.view.message_input.text().strip()

        if not message:
            return

        self.display_message("You", message)
        self.display_message(
            "Pelican",
            "AI connection coming soon!"
        )

        self.view.message_input.clear()

        
    
    def capture_screen(self):
        if self.selected_window is None:
            self.display_message(
                "Pelican",
                "Please select an application first."
            )
            return

        try:
            image_bytes = self.screen_capture.capture(
                self.selected_window
            )

            preview = ScreenshotPreview(image_bytes, self.view)

            result = preview.exec()

            if result == QDialog.DialogCode.Accepted:
                self.confirmed_screenshot = image_bytes

                self.display_message(
                    "Pelican",
                    "Screenshot confirmed and ready for analysis."
                )
            else:
                self.confirmed_screenshot = None

                self.display_message(
                    "Pelican",
                    "Screenshot discarded."
                )

        except Exception as error:
            self.confirmed_screenshot = None

            self.display_message(
                "Pelican",
                f"Screen capture failed: {error}"
            )



    def refresh_windows(self):
        self.selected_window = None
        self.available_windows = self.window_manager.get_open_windows()

        self.view.window_selector.blockSignals(True)
        self.view.window_selector.clear()

        self.view.window_selector.addItem("Select an application")

        for window in self.available_windows:
            self.view.window_selector.addItem(window["title"])

        self.view.window_selector.blockSignals(False)


    
    def select_window(self, index):
        if index <= 0:
            self.selected_window = None
            return

        selected = self.available_windows[index - 1]

        self.selected_window = selected["window"]

        self.display_message(
            "Pelican",
            f"Selected application: {selected['title']}"
        )


