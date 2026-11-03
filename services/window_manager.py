import pywinctl


class WindowManager:

    def get_open_windows(self):
        windows = []

        for window in pywinctl.getAllWindows():
            title = window.title

            if not title:
                continue

            if window.isMinimized:
                continue

            windows.append({
                "title": title,
                "window": window
            })

        return windows