from flask import Flask, request, jsonify
from flask_cors import CORS

import os
import csv

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})
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

from flask import send_file, make_response

@app.route('/download', methods=['GET'])
def download_results():
    if not os.path.exists('results.csv'):
        return "No results available yet.", 404

    response = make_response(send_file('results.csv', as_attachment=True))
    response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '0'
    return response

# 🔥 Required for Render — bind to 0.0.0.0 and dynamic port
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
