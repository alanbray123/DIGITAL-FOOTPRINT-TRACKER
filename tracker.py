import win32gui
import time
from datetime import datetime
from dist.database import create_table, insert_log
import threading
import pystray
from PIL import Image, ImageDraw

def get_active_window():
    window = win32gui.GetForegroundWindow()
    return win32gui.GetWindowText(window)

create_table()

def track():
    last_window = ""
    start_time = time.time()

    while True:
        current_window = get_active_window()

        if current_window != last_window and current_window != "":
            end_time = time.time()
            duration = end_time - start_time

            if last_window != "":
                insert_log(
                    f"{last_window} | {round(duration, 2)} sec",
                    datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                )

            start_time = time.time()
            last_window = current_window

        time.sleep(2)

# Create tray icon
def create_image():
    img = Image.new("RGB", (64, 64), color="black")
    draw = ImageDraw.Draw(img)
    draw.rectangle((16, 16, 48, 48), fill="white")
    return img

def on_quit(icon, item):
    icon.stop()
    exit()

def tray():
    icon = pystray.Icon("Tracker")
    icon.icon = create_image()
    icon.title = "Digital Footprint Tracker"
    icon.menu = pystray.Menu(
        pystray.MenuItem("Quit", on_quit)
    )
    icon.run()

# Run tracker in background thread
threading.Thread(target=track, daemon=True).start()

# Run tray icon
tray()