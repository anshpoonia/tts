from models import STT, TTS, device
from utils import save_file, ROOT, get_speakers
from error import ParameterError, FileSizeError, LanguageError, SpeakerNotFoundError, FileNotSelectedError
from flask import Flask, send_file, request, jsonify, render_template, redirect, abort, send_from_directory
import os

app = Flask(__name__)


stt = STT()
tts = TTS()


@app.route("/", methods=["GET"])
def index():
    return redirect("/tts")


@app.route('/favicon.ico', methods=["GET"])
def icon_handler():
    return send_file(os.path.join(ROOT, "favicon.ico"))


@app.route("/tts", methods=["GET"])
def tts_page_handler():
    return render_template("tts.html")


@app.route("/stt", methods=["GET"])
def stt_page_handler():
    return render_template("stt.html")


@app.route('/gpu', methods=["GET"])
def device_handler():
    return "Server is running on " + device


@app.route("/speakers", methods=["GET"])
def speakers_handler():
    speakers = {'male': str(len(get_speakers("male"))),
                'female': str(len(get_speakers("female")))}
    return jsonify(speakers)


@app.route("/speak", methods=["GET"])
def tts_handler():
    try:
        text = request.args.get("text")
        speaker = request.args.get("speaker")
        tag = request.args.get("tag")
        lang = request.args.get("lang")

        if text is None or speaker is None or tag is None or lang is None:
            raise ParameterError()

        file_path = tts.transform(text=text, tag=tag, speaker=speaker, lang=lang)
        return send_file(file_path)

    except (ParameterError, LanguageError, SpeakerNotFoundError) as e:
        message = {"error": e.message}
        res = jsonify(message)
        res.status = 501
        return abort(res)


@app.route("/add-speaker", methods=["POST"])
def add_speaker_handler():
    try:
        if 'file' not in request.files:
            raise ParameterError()

        file = request.files['file']
        code = tts.new_speaker(file)
        return jsonify({"speaker_code": code})

    except (ParameterError, FileSizeError, FileNotSelectedError) as e:
        message = {"error": e.message}
        return jsonify(message)


@app.route("/write", methods=["POST"])
def stt_handler():
    try:
        if 'file' not in request.files:
            raise ParameterError()

        file = request.files['file']
        file_path = save_file(file)
        text = stt.transform(file_path)
        return jsonify({"text": text})

    except (ParameterError, FileSizeError, FileNotSelectedError) as e:
        message = {"error": e.message}
        return jsonify(message)


if __name__ == "__main__":
    app.run(debug=False, host='0.0.0.0', port=5000)
