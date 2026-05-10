from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import os
import subprocess
from gtts import gTTS
from TTS.api import TTS
import torch

app = Flask(__name__)
CORS(app)

# Load XTTS model for Arabic dialects
device = "cuda" if torch.cuda.is_available() else "cpu"
tts = TTS("tts_models/multilingual/multi-dataset/xtts_v2").to(device)

DIALECT_SPEAKERS = {
    "فصحى": {"بنت": "female_01", "ولد": "male_01", "طفل": "child_01", "رجل": "male_deep", "شاب": "male_young", "عجوز": "male_old"},
    "خليجي": {"بنت": "ar_sa_female", "ولد": "ar_sa_male", "طفل": "ar_sa_child", "رجل": "ar_sa_male_deep", "شاب": "ar_sa_young", "عجوز": "ar_sa_old"},
    "سوري": {"بنت": "ar_sy_female", "ولد": "ar_sy_male", "طفل": "ar_sy_child", "رجل": "ar_sy_male_deep", "شاب": "ar_sy_young", "عجوز": "ar_sy_old"},
    "مصري": {"بنت": "ar_eg_female", "ولد": "ar_eg_male", "طفل": "ar_eg_child", "رجل": "ar_eg_male_deep", "شاب": "ar_eg_young", "عجوز": "ar_eg_old"},
    "بدوي": {"بنت": "ar_bd_female", "ولد": "ar_bd_male", "طفل": "ar_bd_child", "رجل": "ar_bd_male_deep", "شاب": "ar_bd_young", "عجوز": "ar_bd_old"}
}

@app.route('/generate_voice', methods=['POST'])
def generate_voice():
    data = request.json
    text = data['text']
    dialect = data['dialect']
    voice_type = data['voice_type']
    
    speaker = DIALECT_SPEAKERS[dialect][voice_type]
    output_path = f"./temp/voice_{dialect}_{voice_type}.wav"
    
    # Use XTTS for dialect support
    tts.tts_to_file(text=text, speaker_wav=f"./voices/{speaker}.wav", language="ar", file_path=output_path)
    return send_file(output_path, mimetype='audio/wav')

@app.route('/sadtalker', methods=['POST'])
def sadtalker():
    image_path = request.files['image'].save('./temp/source.png')
    audio_path = request.files['audio'].save('./temp/driven.wav')
    
    cmd = [
        'python', 'inference.py',
        '--driven_audio', './temp/driven.wav',
        '--source_image', './temp/source.png',
        '--result_dir', './results',
        '--still', '--preprocess', 'full', '--enhancer', 'gfpgan'
    ]
    subprocess.run(cmd)
    return send_file('./results/source.mp4', mimetype='video/mp4')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
