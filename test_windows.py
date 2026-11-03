from services.window_manager import WindowManager

manager = WindowManager()

windows = manager.get_open_windows()

for index, window in enumerate(windows):
    print(f"{index + 1}. {window['title']}")