import time
import threading
import numpy as np
import pyaudio
import subprocess
import sys

from flask import Flask, request, render_template_string
from pystray import Icon, MenuItem, Menu
from PIL import Image, ImageDraw

# --- CONFIG ---
FREQUENCY = 25000  # Hz (ultrasonic)
DURATION = 1       # seconds
INTERVAL = 300     # 5 minutes
VOLUME = 0.01      # Very quiet
RATE = 44100       # Sample rate

# --- Globals ---
running = True
timer_thread = None
cancel_timer = threading.Event()

# --- Flask App ---
app = Flask(__name__)

HTML_PAGE = '''
<!DOCTYPE html>
<html>
<head><title>Spotify Sleep Timer</title></head>
<body style="font-family:sans-serif; text-align:center; padding-top:50px;">
    <h2>Spotify Sleep Timer</h2>
    <form method="POST" action="/">
        <label>Minutes to wait before pausing Spotify:</label><br><br>
        <input type="number" name="minutes" min="1" required>
        <br><br>
        <input type="submit" value="Start Timer">
    </form>
    <form method="POST" action="/cancel">
        <input type="submit" value="Cancel Timer" style="margin-top:20px;">
    </form>
    <p>{{ message }}</p>
</body>
</html>
'''

@app.route("/", methods=["GET", "POST"])
def index():
    message = ""
    if request.method == "POST":
        try:
            minutes = int(request.form["minutes"])
            start_timer(minutes)
            message = f"Timer started for {minutes} minute(s)."
        except:
            message = "Invalid input."
    return render_template_string(HTML_PAGE, message=message)

@app.route("/cancel", methods=["POST"])
def cancel():
    stop_timer()
    return render_template_string(HTML_PAGE, message="Timer canceled.")

def pause_spotify():
    subprocess.call(['powershell', '-command', '(New-Object -ComObject WScript.Shell).SendKeys([char]179)'])

def start_timer(minutes):
    global timer_thread, cancel_timer

    def timer():
        print(f"[TIMER] Timer started for {minutes} minutes.")
        cancel_timer.clear()
        for _ in range(minutes * 60):
            if cancel_timer.is_set():
                print("[TIMER] Timer canceled.")
                return
            time.sleep(1)
        print("[TIMER] Time's up. Pausing Spotify.")
        pause_spotify()

    if timer_thread and timer_thread.is_alive():
        print("[TIMER] Another timer is running. Canceling it.")
        cancel_timer.set()
        timer_thread.join()

    timer_thread = threading.Thread(target=timer)
    timer_thread.start()

def stop_timer():
    global cancel_timer
    cancel_timer.set()

# --- Soundbar Tone ---
def play_tone():
    p = pyaudio.PyAudio()
    samples = (VOLUME * np.sin(2 * np.pi * np.arange(RATE * DURATION) * FREQUENCY / RATE)).astype(np.float32)
    stream = p.open(format=pyaudio.paFloat32, channels=1, rate=RATE, output=True)
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

# --- System Tray ---
def quit_app(icon, item):
    global running
    running = False
    cancel_timer.set()
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
    icon = Icon("SoundbarKeeper", create_image(), menu=menu)
    threading.Thread(target=audio_loop, daemon=True).start()
    threading.Thread(target=start_flask_server, daemon=True).start()
    icon.run()

def start_flask_server():
    print("Access Spotify Timer at: http://<your-ip>:5000")
    app.run(host="0.0.0.0", port=5000, debug=False, use_reloader=False)


# --- Start everything ---
if __name__ == "__main__":
    setup_tray()