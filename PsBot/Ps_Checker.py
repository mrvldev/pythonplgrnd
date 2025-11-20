import threading
import time
import logging
from datetime import datetime
from zoneinfo import ZoneInfo
from flask import Flask, jsonify, request, render_template
import requests
from bs4 import BeautifulSoup

# ---- Konfiguration ----
URL = "https://www.playstation.com/de-at/games/where-winds-meet/"
INTERVAL = 180  # Sekunden
TIMEZONE = ZoneInfo("Europe/Vienna")  # MEZ/MESZ
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s]: %(message)s")

# ---- Status-Speicher ----
state = {
    "status": "unknown",
    "last_check": None,
    "reason": "Noch nicht gestartet"
}
state_lock = threading.Lock()
checker_running = threading.Event()

# ---- Flask App ----
app = Flask(__name__)

# ---- Funktion für PS Store Check ----
def check_store():
    try:
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
        response = requests.get(URL, headers=headers)
        if response.status_code != 200:
            return "unknown", f"Fehler Status-Code {response.status_code}"

        soup = BeautifulSoup(response.text, "html.parser")
        text = soup.get_text()

        if "Nicht zum Kauf erhältlich" in text:
            return "unavailable", "Noch nicht verfügbar"
        elif "Zur Bibliothek hinzufügen" in text or "Kostenlos" in text:
            return "available", "Spiel ist verfügbar!"
        else:
            return "unknown", "Status unklar"
    except Exception as e:
        return "unknown", f"Fehler beim Abrufen: {e}"

# ---- Checker Thread ----
def checker_loop():
    logging.info(f"Checker-Thread gestartet (INTERVAL={INTERVAL})")
    while True:
        checker_running.wait()  # pausiert, wenn Event nicht gesetzt
        status, reason = check_store()
        with state_lock:
            state["status"] = status
            state["reason"] = reason
            state["last_check"] = datetime.now(TIMEZONE).strftime("%Y-%m-%d %H:%M:%S %Z")
        logging.info(f"Check: {status} — {reason}")
        time.sleep(INTERVAL)

# ---- Flask Routen ----
@app.route("/")
def index():
    return render_template("index.html")

@app.route("/status")
def status():
    with state_lock:
        return jsonify(state)

@app.route("/start", methods=["POST"])
def start():
    checker_running.set()
    return jsonify({"result": "Checker gestartet"})

@app.route("/stop", methods=["POST"])
def stop():
    checker_running.clear()
    return jsonify({"result": "Checker pausiert"})

@app.route("/check_now", methods=["POST"])
def check_now():
    status_val, reason_val = check_store()
    with state_lock:
        state["status"] = status_val
        state["reason"] = reason_val
        state["last_check"] = datetime.now(TIMEZONE).strftime("%Y-%m-%d %H:%M:%S %Z")
    return jsonify(state)

@app.route("/shutdown", methods=["POST"])
def shutdown():
    func = request.environ.get("werkzeug.server.shutdown")
    if func:
        func()
    return "Server wird beendet..."

# ---- Main ----
if __name__ == "__main__":
    thread = threading.Thread(target=checker_loop, daemon=True)
    thread.start()
    checker_running.set()  # ✅ startet direkt
    app.run(debug=False, use_reloader=False)  # WICHTIG: reloader aus
