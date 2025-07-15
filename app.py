from flask import Flask, request, jsonify, send_file, make_response
from flask_cors import CORS
import os
import csv
from datetime import datetime

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

RESULTS_FILE = '/data/results.csv'

# Initialize CSV with headers if it doesn't exist
if not os.path.exists(RESULTS_FILE):
    with open(RESULTS_FILE, mode='w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow([
            'timestamp',
            'filename',
            'utterance',
            'verb',
            'NIA',
            'prolific_pid',
            'question_id',
            'answer',
            'confidence'
        ])

@app.route("/")
def home():
    return "Verb Taxonomy Backend is Running"

@app.route("/submit", methods=["POST"])
def submit():
    data = request.json
    prolific_id = data.get("prolific_pid", "unknown")
    filename = data.get("filename", "unknown_batch")
    responses = data.get("responses", [])

    with open(RESULTS_FILE, mode='a', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        for r in responses:
            question_id = r.get("question_id", "")
            answer = r.get("answer", "")
            confidence = r.get("confidence", "")
            utterance = r.get("utterance", "")
            nia = r.get("nia", "")
            verb = question_id.split("_")[0] if "_" in question_id else ""
            timestamp = datetime.utcnow().isoformat()

            writer.writerow([
                timestamp,
                filename,
                utterance,
                verb,
                nia,
                prolific_id,
                question_id,
                answer,
                confidence
            ])

    return jsonify({"status": "ok"})

@app.route('/download', methods=['GET'])
def download_results():
    if not os.path.exists(RESULTS_FILE):
        return "No results available yet.", 404

    response = make_response(send_file(RESULTS_FILE, as_attachment=True))
    response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '0'
    return response

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
