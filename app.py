from flask import Flask, send_file, request, jsonify, redirect, url_for
import hashlib
from TTS.api import TTS
import os

app = Flask(__name__)
tts = TTS(model_name="tts_models/en/jenny/jenny", progress_bar=False)
root = os.getcwd()
dirt = os.path.join(root, "files")
os.mkdir(dirt)



def hashit(input_string):
    input_bytes = input_string.encode('utf-8')
    sha256_hash = hashlib.sha256()
    sha256_hash.update(input_bytes)
    hashed_string = sha256_hash.hexdigest()
    return hashed_string


def voiceit(text, loc):
    tts.tts_to_file(text=text, file_path=os.path.join(dirt, f"{loc}.wav"))


@app.route('/')
def index():
    try:
        phone_number = request.args.get("p")
        text = request.args.get("text")
        # model = request.args.get("v")
        loc = hashit(str(phone_number) + text)
        if not os.path.isfile(os.path.join(dirt, f"{loc}.wav")):
            voiceit(text, loc)
    except:
        return jsonify({"message": "Use the following get parameters",
                        "p": "Phone Number",
                        "text": "Text that need to be converted into speech",
                        "v": "Selected model"})
    else:
        return redirect(url_for("file", h=loc))


@app.route('/file')
def file():
    h = request.args.get("h")
    return send_file(os.path.join(dirt, f"{h}.wav"))


if __name__ == "__main__":
    app.run(debug=False, host='0.0.0.0')
