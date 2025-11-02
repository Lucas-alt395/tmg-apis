from flask import Flask, jsonify
import requests
import datetime
import pytz

app = Flask(__name__)

# --- CONFIG ---
GITHUB_USER = "Lucas-alt395"
REPO_PATH = "tmgtv/main/LTV/SD"
TZ = pytz.timezone("Europe/Amsterdam")


@app.route("/")
def home():
    return "1"


# --- LTV Schedule ---
@app.route("/services/tmgtv/ltv/sdget")
def ltv_schedule():
    today = datetime.datetime.now(TZ).strftime("%d.%m.%Y")
    url = f"https://raw.githubusercontent.com/{GITHUB_USER}/{REPO_PATH}/{today}.json"

    try:
        response = requests.get(url)
        response.raise_for_status()
        return jsonify(response.json())
    except requests.exceptions.RequestException as e:
        return jsonify({"error": "Failed to load schedule", "details": str(e)}), 404
    except ValueError:
        return jsonify({"error": "Invalid JSON format"}), 500


# --- TIME SERVICES ---
@app.route("/services/time/time/")
def current_time():
    now = datetime.datetime.now(TZ)
    time_str = now.strftime("%H:%M:%S")  # includes seconds
    return jsonify({"time": time_str})


@app.route("/services/time/minutes/")
def minutes_since_midnight():
    now = datetime.datetime.now(TZ)
    midnight = now.replace(hour=0, minute=0, second=0, microsecond=0)
    minutes = int((now - midnight).total_seconds() // 60)
    return jsonify({"minutes_since_midnight": minutes})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)