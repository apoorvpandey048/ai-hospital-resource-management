"""Flask API endpoints (moved to app/)

Simple demo endpoints that call into the `modules` library.
"""
from flask import Flask, request, jsonify
from modules import bed_allocation, fuzzy_triage, nlp_chatbot

app = Flask(__name__)


@app.route('/allocate', methods=['POST'])
def allocate():
    data = request.json
    patient = data.get('patient')
    beds = data.get('beds')
    bed = bed_allocation.allocate_bed(patient, beds)
    return jsonify({'bed': bed})


@app.route('/priority', methods=['POST'])
def priority():
    data = request.json
    temp = data.get('temp')
    sbp = data.get('sbp')
    pain = data.get('pain')
    score = fuzzy_triage.compute_priority(temp, sbp, pain)
    return jsonify({'priority': score})


@app.route('/chat', methods=['POST'])
def chat():
    data = request.json
    q = data.get('q', '')
    return jsonify({'answer': nlp_chatbot.respond(q)})


if __name__ == '__main__':
    app.run(debug=True)
