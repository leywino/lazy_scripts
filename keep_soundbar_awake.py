import time
import numpy as np
import pyaudio
import threading
import sys
from pystray import Icon, MenuItem, Menu
from PIL import Image, ImageDraw

# Audio settings
FREQUENCY = 25000  # Hz (ultrasonic)
DURATION = 1       # seconds
INTERVAL = 300     # 5 minutes
VOLUME = 0.01      # Very quiet
RATE = 44100       # Sample rate

running = True

def play_tone():
    p = pyaudio.PyAudio()
    samples = (VOLUME * np.sin(2 * np.pi * np.arange(RATE * DURATION) * FREQUENCY / RATE)).astype(np.float32)

    stream = p.open(format=pyaudio.paFloat32,
                    channels=1,
                    rate=RATE,
                    output=True)

    stream.write(samples.tobytes())
    stream.stop_stream()
    stream.close()
    p.terminate()

def audio_loop():
    while running:
        play_tone()
        for _ in range(INTERVAL):
            if not running:
                return
            time.sleep(1)

def quit_app(icon, item):
    global running
    running = False
    icon.stop()
    sys.exit()

def create_image():
    image = Image.new('RGB', (64, 64), "white")
    dc = ImageDraw.Draw(image)
    dc.rectangle([16, 24, 28, 40], fill="black")
    dc.polygon([(28, 24), (40, 16), (40, 48), (28, 40)], fill="black")
    return image

def setup_tray():
    menu = Menu(MenuItem('Exit', quit_app))
    icon = Icon("Soundbar Keeper", create_image(), menu=menu)
    threading.Thread(target=audio_loop, daemon=True).start()
    icon.run()

if __name__ == "__main__":
    setup_tray()
