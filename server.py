from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import os
app = Flask(__name__)
CORS(app)

@app.route('/health')
def health():
    return jsonify({"status": "running", "dialects": ["فصحى","خليجي","سوري","مصري","بدوي"]})

@app.route('/preview_voice', methods=['POST'])
def preview_voice():
    data = request.json
    # Simulate: return a demo audio file
    return send_file('./demo.wav', mimetype='audio/wav')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
