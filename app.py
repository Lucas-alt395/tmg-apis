from flask import Flask, jsonify
import requests
import datetime

app = Flask(__name__)

GITHUB_USER = "Lucas-alt395"
REPO_PATH = "tmgtv/main/LTV/SD"

@app.route("/")
def home():
    return "1"

@app.route("/services/tmgtv/ltv/sdget")
def ltv_schedule():
    today = datetime.datetime.utcnow().strftime("%d.%m.%Y")
    url = f"https://raw.githubusercontent.com/{GITHUB_USER}/{REPO_PATH}/{today}.json"

    try:
        response = requests.get(url)
        response.raise_for_status()
        return jsonify(response.json())
    except requests.exceptions.RequestException as e:
        return jsonify({"error": "Failed to load schedule", "details": str(e)}), 404
    except ValueError:
        return jsonify({"error": "Invalid JSON format"}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
