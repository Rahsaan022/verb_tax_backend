from flask import Flask, request, jsonify
import os
import csv

app = Flask(__name__)
RESULTS_FILE = "results.csv"

# Initialize CSV with headers if it doesn't exist
if not os.path.exists(RESULTS_FILE):
    with open(RESULTS_FILE, mode='w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['prolific_pid', 'question_id', 'answer', 'confidence'])

@app.route("/")
def home():
    return "Verb Taxonomy Backend is Running"

@app.route("/submit", methods=["POST"])
def submit():
    data = request.json
    prolific_id = data.get("prolific_pid", "unknown")
    responses = data.get("responses", [])

    with open(RESULTS_FILE, mode='a', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        for r in responses:
            writer.writerow([prolific_id, r["question_id"], r["answer"], r["confidence"]])

    return jsonify({"status": "ok"})

from flask import send_file

@app.route("/download", methods=["GET"])
def download():
    if os.path.exists(RESULTS_FILE):
        return send_file(RESULTS_FILE, as_attachment=True)
    else:
        return jsonify({"error": "Results file not found"}), 404

# 🔥 Required for Render — bind to 0.0.0.0 and dynamic port
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
