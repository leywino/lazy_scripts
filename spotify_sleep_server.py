from flask import Flask, request, render_template_string
import threading
import time
import subprocess

app = Flask(__name__)
timer_thread = None

HTML_PAGE = '''
<!DOCTYPE html>
<html>
<head><title>Spotify Sleep Timer</title></head>
<body style="font-family:sans-serif; text-align:center; padding-top:50px;">
    <h2>Spotify Sleep Timer</h2>
    <form method="POST">
        <label>Minutes to wait before pausing Spotify:</label><br><br>
        <input type="number" name="minutes" min="1" required>
        <br><br>
        <input type="submit" value="Start Timer">
    </form>
    <p>{{ message }}</p>
</body>
</html>
'''

def pause_spotify():
    # Windows media key (Play/Pause)
    subprocess.call(['powershell', '-command', '(New-Object -ComObject WScript.Shell).SendKeys([char]179)'])

def start_timer(minutes):
    def timer():
        print(f"[TIMER] Timer started for {minutes} minute(s).")
        time.sleep(minutes * 60)
        print("[TIMER] Time's up! Pausing Spotify.")
        pause_spotify()
    global timer_thread
    if timer_thread and timer_thread.is_alive():
        print("[TIMER] Previous timer still running. Ignored.")
        return
    timer_thread = threading.Thread(target=timer)
    timer_thread.start()

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

if __name__ == "__main__":
    print("Visit this on your phone: http://<your-ip>:5000")
    app.run(host="0.0.0.0", port=5000)
