
import io
import mss
from PIL import Image


class ScreenCapture:

    def capture(self, window):
        # Get the selected window's position and size
        left = window.left
        top = window.top
        width = window.width
        height = window.height

        if width <= 0 or height <= 0:
            raise ValueError("Selected window has invalid dimensions.")

        # Define the region to capture
        region = {
            "left": left,
            "top": top,
            "width": width,
            "height": height
        }

        # Capture only this screen region
        with mss.mss() as screen:
            screenshot = screen.grab(region)

            image = Image.frombytes(
                "RGB",
                screenshot.size,
                screenshot.rgb
            )

            buffer = io.BytesIO()
            image.save(buffer, format="PNG")

            return buffer.getvalue()
