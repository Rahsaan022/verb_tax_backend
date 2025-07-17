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
    responses = data.get("responses", [])

    with open(RESULTS_FILE, mode='a', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        for r in responses:
            question_id = r.get("question_id", "")
            answer = r.get("answer", "")
            confidence = r.get("confidence", "")
            utterance = r.get("utterance", "unknown")
            nia = r.get("label_true", "unknown")
            filename = r.get("batch_filename", "unknown_batch")
            timestamp = datetime.utcnow().isoformat()

            # Parse structure: [utterance_id]_[verb]_[eval_num]_[tax_q_num]
            q_parts = question_id.split("_")
            if len(q_parts) >= 4:
                evaluation_id = "_".join(q_parts[:-1])     # everything except last
                verb = q_parts[1]
                utt_eval_number = q_parts[2]
                test_taxq_number = q_parts[3]
            else:
                evaluation_id = "unknown_eval"
                verb = "unknown"
                utt_eval_number = "unknown"
                test_taxq_number = "unknown"

            # test_q_number (1–10) expected from frontend
            test_q_number = r.get("test_q_number", "unknown")

            writer.writerow([
                timestamp,
                filename,
                utterance,
                nia,
                prolific_id,
                evaluation_id,
                verb,
                utt_eval_number,
                test_q_number,
                test_taxq_number,
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
