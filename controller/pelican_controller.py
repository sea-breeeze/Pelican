from services.screen_capture import ScreenCapture
from services.window_manager import WindowManager
from view.screenshot_preview import ScreenshotPreview
from PySide6.QtWidgets import QDialog
from services.ui_inspector import UIInspector
from view.highlight_overlay import HighlightOverlay
from services.vision_service import VisionService
from services.vision_worker import VisionWorker

class PelicanController:


    def __init__(self, view, model):
        self.view = view
        self.model = model
        self.screen_capture = ScreenCapture()

        self.view.toggle_button.clicked.connect(self.toggle_window)
        self.view.close_button.clicked.connect(self.view.close)

        self.view.chat_button.clicked.connect(self.activate_chat)
        self.view.explore_button.clicked.connect(self.activate_explore)

        self.view.send_button.clicked.connect(self.analyze_screenshot)
        self.view.message_input.returnPressed.connect(self.analyze_screenshot)

        self.view.capture_button.clicked.connect(self.capture_screen)

        self.window_manager = WindowManager()
        self.available_windows = []

        self.view.refresh_button.clicked.connect(self.refresh_windows)
        self.view.window_selector.currentIndexChanged.connect(
            self.select_window
        )

        self.highlight_overlay = HighlightOverlay()
        self.detected_elements = []

        self.view.highlight_button.clicked.connect(
            self.highlight_selected_element
        )

        self.ui_inspector = UIInspector()

        self.view.inspect_button.clicked.connect(
            self.inspect_application
        )

        self.vision_service = VisionService()

        self.refresh_windows()

        self.confirmed_screenshot = None

        self.selected_window = None

        self.api_requests = 0
        self.max_api_requests = 10

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
        self.highlight_overlay.stop_tracking()
        self.selected_window = None
        self.available_windows = self.window_manager.get_open_windows()

        self.view.window_selector.blockSignals(True)
        self.view.window_selector.clear()

        self.view.window_selector.addItem("Select an application")

        for window in self.available_windows:
            self.view.window_selector.addItem(window["title"])

        self.view.window_selector.blockSignals(False)


    
    def select_window(self, index):
        self.confirmed_screenshot = None
        self.highlight_overlay.stop_tracking()
        self.detected_elements = []
        self.view.element_selector.clear()

        if index <= 0:
            self.selected_window = None
            return

        selected = self.available_windows[index - 1]

        self.selected_window = selected["window"]

        self.display_message(
            "Pelican",
            f"Selected application: {selected['title']}"
        )

            
    def highlight_selected_element(self):
        if self.model.current_mode != "explore":
            self.display_message(
                "Pelican",
                "Switch to Explore Mode first."
            )
            return

        index = self.view.element_selector.currentIndex()

        if index <= 0:
            self.display_message(
                "Pelican",
                "Please select a UI element first."
            )
            return

        element = self.detected_elements[index - 1]

        self.highlight_overlay.track_control(
            element["control"]
        )

        self.display_message(
            "Pelican",
            f"Highlighting: {element['name']}"
        )


        
    def inspect_application(self):
        if self.model.current_mode != "explore":
            self.display_message(
                "Pelican",
                "Switch to Explore Mode to inspect applications."
            )
            return

        if self.selected_window is None:
            self.display_message(
                "Pelican",
                "Please select an application first."
            )
            return

        try:
            elements = self.ui_inspector.inspect_window(
                self.selected_window
            )

            if not elements:
                self.display_message(
                    "Pelican",
                    "No UI elements were detected."
                )
                return

            # Show only meaningful elements
            useful_types = {
                "ButtonControl",
                "EditControl",
                "DocumentControl",
                "MenuItemControl",
                "CheckBoxControl",
                "ComboBoxControl"
            }

            useful_elements = [
                element for element in elements
                if element["type"] in useful_types
                and element["name"].strip()
            ]

            self.detected_elements = [
                element for element in useful_elements
                if element["width"] > 0
                and element["height"] > 0
            ]

            self.view.element_selector.clear()
            self.view.element_selector.addItem("Select a UI element")

            for element in self.detected_elements:
                self.view.element_selector.addItem(
                    f"{element['name']} ({element['type']})"
                )

            self.display_message(
                "Pelican",
                f"Found {len(useful_elements)} interactive or useful elements."
            )

            for element in useful_elements[:15]:
                self.display_message(
                    "Pelican",
                    f"{element['type']}: {element['name']}"
                )

        except Exception as error:
            self.display_message(
                "Pelican",
                f"Inspection failed: {error}"
            )

    
    
    def analyze_screenshot(self):
        if self.confirmed_screenshot is None:
            self.display_message(
                "Pelican", "Capture and confirm a screenshot first."
            )
            return

        question = self.view.message_input.text().strip()

        if not question:
            self.display_message(
                "Pelican", "Type a question first."
            )
            return

        if self.vision_service.client is None:
            self.display_message(
                "Pelican", "Meta API is not configured."
            )
            return

        if getattr(self, "vision_worker", None) is not None:
            if self.vision_worker.isRunning():
                return

        self.display_message("You", question)
        self.display_message("Pelican", "Analyzing screenshot...")

        self.view.send_button.setEnabled(False)

        if self.api_requests >= self.max_api_requests:
            self.display_message(
                "Pelican",
                "API request limit reached. Restart Pelican to reset."
            )
            self.view.send_button.setEnabled(False)
            return

        self.api_requests += 1

        inspection_text = ""

        if self.selected_window is not None:
            elements = self.ui_inspector.inspect_window(
                self.selected_window
            )

            inspection_text = "\n".join(
                f"- {element['name']} ({element['type']})"
                for element in elements
                if element["name"]
            )[:4000]
                

        self.vision_worker = VisionWorker(
            self.confirmed_screenshot,
            question,
            inspection_text
        )

        self.vision_worker.finished.connect(self.on_analysis_finished)
        self.vision_worker.failed.connect(self.on_analysis_failed)
        self.vision_worker.start()


    def on_analysis_finished(self, answer):
        self.display_message("Pelican", answer)
        self.view.message_input.clear()
        self.view.send_button.setEnabled(
            self.api_requests < self.max_api_requests
        )

    def on_analysis_failed(self, error):
        self.display_message(
            "Pelican", f"AI request failed: {error}"
        )
        self.view.send_button.setEnabled(
            self.api_requests < self.max_api_requests
        )



