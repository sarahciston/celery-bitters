import os
from flask import Flask
from flask import render_template
from flask import request
from flask import send_file

import scal_task

import argparse
import io
import json
import sys
from pathlib import Path
from typing import Union

from TTS.config import load_config
from TTS.utils.manage import ModelManager
from TTS.utils.synthesizer import Synthesizer

app = Flask(__name__)

@app.route("/")
def hello():
    name = request.args.get('name', 'John Doe')
    result = scal_task.hello.delay(name)
    result.wait()
    return render_template('index.html', celery=result)

@app.route("/test")
def test():
    info = request.args.get('name', 'default')
    result = scal_task.test.delay(name)
    result.wait()
    return render_template('index.html', celery=result)

## SYNTHESIZER COQUI
def style_wav_uri_to_dict(style_wav: str) -> Union[str, dict]:
    """Transform an uri style_wav, in either a string (path to wav file to be use for style transfer)
    or a dict (gst tokens/values to be use for styling)

    Args:
        style_wav (str): uri

    Returns:
        Union[str, dict]: path to file (str) or gst style (dict)
    """
    if style_wav:
        if os.path.isfile(style_wav) and style_wav.endswith(".wav"):
            return style_wav  # style_wav is a .wav file located on the server

        style_wav = json.loads(style_wav)
        return style_wav  # style_wav is a gst dictionary with {token1_id : token1_weigth, ...}
    return None

@app.route("/synth")
def synth():
    return render_template(
        "synth.html",
        show_details=args.show_details,
        use_multi_speaker=use_multi_speaker,
        speaker_ids=speaker_manager.speaker_ids if speaker_manager is not None else None,
        use_gst=use_gst,
    )

@app.route("/api/tts", methods=["GET"])
def tts():
    text = request.args.get("text")
    speaker_idx = request.args.get("speaker_id", "")
    style_wav = request.args.get("style_wav", "")
    style_wav = style_wav_uri_to_dict(style_wav)
    print(" > Model input: {}".format(text))
    print(" > Speaker Idx: {}".format(speaker_idx))
    wavs = synthesizer.tts(text, speaker_name=speaker_idx, style_wav=style_wav)
    out = io.BytesIO()
    synthesizer.save_wav(wavs, out)
    return send_file(out, mimetype="audio/wav")

## END COQUI

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 3000))
    app.run(host='0.0.0.0', port=port)
