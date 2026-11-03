from services.screen_capture import ScreenCapture

capture = ScreenCapture()

filename = capture.capture()

print(f"Screenshot saved: {filename}")