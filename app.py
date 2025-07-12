from flask import Flask, request, jsonify
import csv
import os

app = Flask(__name__)
RESULTS_FILE = "results.csv"

# Create results.csv with headers if it doesn't exist
if not os.path.exists(RESULTS_FILE):
    with open(RESULTS_FILE, mode='w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['prolific_pid', 'question_id', 'answer', 'confidence'])

@app.route("/submit", methods=["POST"])
def submit():
    data = request.json

    with open(RESULTS_FILE, mode='a', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        for entry in data.get("responses", []):
            writer.writerow([
                data.get("prolific_pid", "unknown"),
                entry["question_id"],
                entry["answer"],
                entry["confidence"]
            ])
    
    return jsonify({"status": "success"})
