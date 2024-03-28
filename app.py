import ast


def modify_function(filename, class_name, function_name, new_code):
    with open(filename, 'r') as file:
        tree = ast.parse(file.read())

    print(tree.body)
    # Find the specified class in the AST
    for node in tree.body:
        if isinstance(node, ast.ClassDef) and node.name == class_name:
            # Find the specified function inside the class and modify its body
            for body_node in node.body:
                if isinstance(body_node, ast.FunctionDef) and body_node.name == function_name:
                    body_node.body = ast.parse(new_code).body

    # Generate modified code from the AST
    modified_code = ast.unparse(tree)

    # Write the modified code back to the file
    with open(filename, 'w') as file:
        file.write(modified_code)


modify_function("/usr/local/lib64/python3.9/site-packages/TTS/utils/manage.py", "ModelManager", "ask_tos",
                "return True")

from flask import Flask, send_file, request, jsonify
import hashlib
from TTS.api import TTS
import whisper
import os
import torch

app = Flask(__name__)

device = "cuda" if torch.cuda.is_available() else "cpu"
tts = TTS(model_name="tts_models/multilingual/multi-dataset/xtts_v2", progress_bar=False).to(device)
root = os.getcwd()
model = whisper.load_model("base", device=device, download_root=os.path.join(root, "whisper_models"))
os.environ["COQUI_TOS_AGREED"] = "1"
speaker_dir = os.path.join(root, "speakers")
save_dir = os.path.join(root, "files")
if not os.path.isdir(save_dir):
    os.mkdir(save_dir)

print("--running--")


def hashit(input_string):
    input_bytes = input_string.encode('utf-8')
    sha256_hash = hashlib.sha256()
    sha256_hash.update(input_bytes)
    hashed_string = sha256_hash.hexdigest()
    return hashed_string


def voiceit(text, loc, gender, model, lang="en"):
    tts.tts_to_file(text=text, speaker_wav=os.path.join(speaker_dir, gender, f"{model}.wav"),
                    file_path=os.path.join(save_dir, f"{loc}.wav"), language=lang)
    return send_file(os.path.join(save_dir, f"{loc}.wav"))


@app.route('/model')
def models():
    return jsonify({'male': str(len(os.listdir(os.path.join(speaker_dir, "male")))),
                    'female': str(len(os.listdir(os.path.join(speaker_dir, "female"))))})


@app.route('/gpu')
def is_device():
    return device + str(torch.__version__)


@app.route('/voice')
def voice():
    try:
        text = request.args.get("text")
        model = request.args.get("v")
        gender = request.args.get("gender")
        lang = request.args.get("lang")
        loc = hashit(text + gender + str(model))
        if not os.path.isfile(os.path.join("files", f"{loc}.wav")):
            return voiceit(text, loc, gender, model, lang)
        else:
            return send_file(os.path.join(save_dir, f"{loc}.wav"))

    except:
        return jsonify({"text": "Text that need to be converted into speech",
                        "v": "Selected Voice",
                        "gender": "Selected Gender"})


@app.route('/stt', methods=["POST"])
def stt():
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'No file part'})

        file = request.files['file']
        if file.filename == '':
            return jsonify({'error': 'No selected file'})

        file_path = os.path.join(save_dir, file.filename)
        file.save(file_path)

        file_size_bytes = os.path.getsize(file_path)
        file_size_kb = file_size_bytes / 1024
        file_size_mb = file_size_kb / 1024

        if file_size_mb > 24:
            return jsonify({"error": f"File size exceed 25MB ({file_size_mb}MB)"})

        text = model.transcribe(file_path)
        return jsonify({"text": text["text"]})

    except:
        return jsonify({'error': 'unknown'})

@app.route('/favicon.ico')
def icon():
    return send_file(os.path.join(root, "favicon.ico"))


@app.route('/')
def index():
    return send_file(os.path.join(root, "index.html"))


@app.route('/stt', methods=["GET"])
def stt_index():
    return send_file(os.path.join(root, "stt.html"))


if __name__ == "__main__":
    app.run(debug=False, host='0.0.0.0', port=443)
